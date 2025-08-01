import re
from telegram import Update
from telegram.ext import ContextTypes
from database.db_operations import db_ops
from utils.chart_generator import format_currency

async def budget_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /budget command to set budgets."""
    user_id = update.effective_user.id
    
    # Get user to check currency
    user = await db_ops.get_user(user_id)
    if not user:
        await update.message.reply_text("Please start with /start first!")
        return
    
    # Get the full message text after /budget
    text = ' '.join(context.args)
    
    if not text:
        await update.message.reply_text(
            "Please provide budget details!\n\n"
            "Format: /budget #<category> <amount>\n"
            "Example: /budget #groceries 8000"
        )
        return
    
    # Parse the budget using regex
    # Pattern: #category amount
    pattern = r'^(#\w+)\s+(\d+(?:\.\d+)?)$'
    match = re.match(pattern, text, re.IGNORECASE)
    
    if not match:
        await update.message.reply_text(
            "❌ Invalid format!\n\n"
            "Correct format: /budget #<category> <amount>\n"
            "Examples:\n"
            "• /budget #groceries 8000\n"
            "• /budget #entertainment 2000\n"
            "• /budget #transport 1500"
        )
        return
    
    category = match.group(1).lower()  # Convert to lowercase for consistency
    amount = float(match.group(2))
    
    if amount <= 0:
        await update.message.reply_text("❌ Budget amount must be greater than 0.")
        return
    
    # Set the budget
    success = await db_ops.set_budget(user_id, category, amount)
    
    if success:
        formatted_amount = format_currency(amount, user['currency'])
        await update.message.reply_text(
            f"✅ Budget set: {category} = {formatted_amount}/month"
        )
    else:
        await update.message.reply_text("❌ Failed to set budget. Please try again.")

async def view_budgets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /viewbudgets command."""
    user_id = update.effective_user.id
    
    # Get user to check currency
    user = await db_ops.get_user(user_id)
    if not user:
        await update.message.reply_text("Please start with /start first!")
        return
    
    # Get all budgets
    budgets = await db_ops.get_budgets(user_id)
    
    if not budgets:
        await update.message.reply_text(
            "No budgets set yet.\n\n"
            "Create a budget with: /budget #<category> <amount>\n"
            "Example: /budget #food 5000"
        )
        return
    
    # Get current month spending for each category
    message = "📊 Your Monthly Budgets:\n\n"
    
    for budget in budgets:
        category = budget['category']
        budget_amount = budget['amount']
        
        # Get current spending for this category
        current_spending = await db_ops.get_current_month_spending_by_category(user_id, category)
        
        # Calculate percentage
        percentage = (current_spending / budget_amount) * 100 if budget_amount > 0 else 0
        
        # Format amounts
        spent_formatted = format_currency(current_spending, user['currency'])
        budget_formatted = format_currency(budget_amount, user['currency'])
        
        # Create progress bar
        progress_bar = create_progress_bar(percentage)
        
        # Choose emoji based on percentage
        if percentage >= 100:
            emoji = "🚨"
        elif percentage >= 80:
            emoji = "⚠️"
        elif percentage >= 50:
            emoji = "🟡"
        else:
            emoji = "🟢"
        
        message += f"{emoji} {category}: {spent_formatted} / {budget_formatted} ({percentage:.1f}%)\n"
        message += f"   {progress_bar}\n\n"
    
    await update.message.reply_text(message)

def create_progress_bar(percentage: float, length: int = 10) -> str:
    """Create a visual progress bar."""
    filled = int((percentage / 100) * length)
    if filled > length:
        filled = length
    
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}]"

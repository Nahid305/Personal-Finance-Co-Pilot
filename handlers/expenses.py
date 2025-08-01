import re
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from database.db_operations import db_ops
from utils.chart_generator import format_currency

async def log_expense_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /log and /spent commands."""
    user_id = update.effective_user.id
    
    # Get user to check currency
    user = await db_ops.get_user(user_id)
    if not user:
        await update.message.reply_text("Please start with /start first!")
        return
    
    # Get the full message text
    if update.message.text.startswith('/log'):
        text = update.message.text[4:].strip()
    elif update.message.text.startswith('/spent'):
        text = update.message.text[6:].strip()
    else:
        text = ' '.join(context.args)
    
    if not text:
        await update.message.reply_text(
            "🤔 I need some expense details to help you!\n\n"
            "**Format:** `/log <amount> on #<category> [for <description>]`\n\n"
            "🌟 **Examples:**\n"
            "• `/log 150 on #food for lunch`\n"
            "• `/log 25 on #coffee`\n"
            "• `/log 2500 on #electronics for headphones`\n\n"
            "💡 **Categories use hashtags** like #food, #transport, #fun!\n"
            "Try it now! 😊",
            parse_mode='Markdown'
        )
        return
    
    # Parse the expense using regex
    # Pattern: amount on #category [for description]
    pattern = r'^(\d+(?:\.\d+)?)\s+on\s+(#\w+)(?:\s+for\s+(.+))?$'
    match = re.match(pattern, text, re.IGNORECASE)
    
    if not match:
        await update.message.reply_text(
            "🤖 Hmm, I didn't understand that format!\n\n"
            "**Correct format:** `/log <amount> on #<category> [for <description>]`\n\n"
            "🎯 **Perfect examples:**\n"
            "• `/log 150 on #food for pizza dinner`\n"
            "• `/log 2500 on #electronics for new laptop`\n"
            "• `/log 80 on #transport`\n\n"
            "💡 **Remember:** Categories need the # symbol!\n"
            "Give it another try! 💪",
            parse_mode='Markdown'
        )
        return
    
    amount = float(match.group(1))
    category = match.group(2).lower()  # Convert to lowercase for consistency
    description = match.group(3) if match.group(3) else None
    
    # Log the expense
    success = await db_ops.log_expense(user_id, amount, category, description)
    
    if not success:
        await update.message.reply_text(
            "😔 Oops! Something went wrong saving your expense.\n"
            "Please try again, or contact support if this keeps happening!"
        )
        return
    
    # Format confirmation message
    formatted_amount = format_currency(amount, user['currency'])
    confirmation = f"✅ **Logged successfully!**\n💰 {formatted_amount} on {category}"
    if description:
        confirmation += f"\n📝 {description}"
    
    # Check budget and add warning if necessary
    budget_amount = await db_ops.get_budget_for_category(user_id, category)
    if budget_amount:
        current_spending = await db_ops.get_current_month_spending_by_category(user_id, category)
        percentage = (current_spending / budget_amount) * 100
        
        if percentage >= 100:
            confirmation += f"\n\n🚨 **Budget Alert!** You've exceeded your {category} budget by {percentage-100:.1f}%! 😱"
        elif percentage >= 80:
            confirmation += f"\n\n⚠️ **Heads up!** You've spent {percentage:.1f}% of your {category} budget this month. 🤔"
        else:
            confirmation += f"\n\n📊 Budget status: {percentage:.1f}% of {category} budget used 👍"
    else:
        confirmation += f"\n\n💡 **Tip:** Set a budget for {category} with `/budget {category} <amount>`"
    
    await update.message.reply_text(confirmation, parse_mode='Markdown')

async def delete_transaction_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /delete command."""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "Please provide a transaction ID to delete.\n"
            "Example: /delete 123\n\n"
            "Use /listhistory to see transaction IDs."
        )
        return
    
    try:
        transaction_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid transaction ID. Please provide a number.")
        return
    
    # Delete the transaction
    success = await db_ops.delete_transaction(user_id, transaction_id)
    
    if success:
        await update.message.reply_text(f"✅ Transaction {transaction_id} deleted successfully.")
    else:
        await update.message.reply_text(
            f"❌ Could not delete transaction {transaction_id}. "
            "Please check the ID and try again."
        )

async def list_history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /listhistory command."""
    user_id = update.effective_user.id
    
    # Get user to check currency
    user = await db_ops.get_user(user_id)
    if not user:
        await update.message.reply_text("Please start with /start first!")
        return
    
    # Get limit from args
    limit = 10  # default
    if context.args:
        try:
            limit = int(context.args[0])
            if limit <= 0 or limit > 50:
                await update.message.reply_text("Please provide a limit between 1 and 50.")
                return
        except ValueError:
            await update.message.reply_text("❌ Invalid number. Please provide a valid limit.")
            return
    
    # Get transaction history
    transactions = await db_ops.get_transaction_history(user_id, limit)
    
    if not transactions:
        await update.message.reply_text("No transactions found.")
        return
    
    # Format the message
    message = f"📋 Your Last {len(transactions)} Transactions:\n\n"
    
    for transaction in transactions:
        # Parse the date
        date_obj = datetime.fromisoformat(transaction['date'])
        formatted_date = date_obj.strftime("%d-%b")
        
        # Format amount
        formatted_amount = format_currency(transaction['amount'], user['currency'])
        
        # Create transaction line
        line = f"ID: {transaction['id']} | {formatted_date} | {formatted_amount} | {transaction['category']}"
        
        if transaction['description']:
            line += f" - {transaction['description']}"
        
        message += line + "\n"
    
    message += f"\n💡 Use /delete <ID> to remove a transaction"
    
    await update.message.reply_text(message)

from datetime import datetime, timedelta
from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes
from database.db_operations import db_ops
from utils.chart_generator import generate_pie_chart, format_currency

async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /summary command."""
    user_id = update.effective_user.id
    
    # Get user to check currency
    user = await db_ops.get_user(user_id)
    if not user:
        await update.message.reply_text("Please start with /start first!")
        return
    
    # Determine the time period
    period = 'month'  # default
    if context.args:
        period = context.args[0].lower()
        if period not in ['today', 'week', 'month', 'year']:
            await update.message.reply_text(
                "❌ Invalid period. Use: today, week, month, or year"
            )
            return
    
    # Calculate date range
    now = datetime.now()
    
    if period == 'today':
        start_date = datetime(now.year, now.month, now.day)
        end_date = start_date + timedelta(days=1) - timedelta(seconds=1)
        period_name = "Today"
    elif period == 'week':
        # Start of current week (Monday)
        start_date = now - timedelta(days=now.weekday())
        start_date = datetime(start_date.year, start_date.month, start_date.day)
        end_date = start_date + timedelta(days=7) - timedelta(seconds=1)
        period_name = "This Week"
    elif period == 'month':
        start_date = datetime(now.year, now.month, 1)
        if now.month == 12:
            end_date = datetime(now.year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end_date = datetime(now.year, now.month + 1, 1) - timedelta(seconds=1)
        period_name = "This Month"
    else:  # year
        start_date = datetime(now.year, 1, 1)
        end_date = datetime(now.year + 1, 1, 1) - timedelta(seconds=1)
        period_name = "This Year"
    
    # Get spending data
    spending_by_category = await db_ops.get_spending_by_category(user_id, start_date, end_date)
    total_spending = await db_ops.get_total_spending(user_id, start_date, end_date)
    
    if total_spending == 0:
        await update.message.reply_text(f"No expenses recorded for {period_name.lower()}.")
        return
    
    # Create text summary
    summary_text = f"📊 Spending Summary - {period_name}\n\n"
    summary_text += f"💰 Total Spent: {format_currency(total_spending, user['currency'])}\n\n"
    summary_text += "📈 Category Breakdown:\n"
    
    # Sort categories by spending amount (descending)
    sorted_categories = sorted(spending_by_category.items(), key=lambda x: x[1], reverse=True)
    
    for category, amount in sorted_categories:
        percentage = (amount / total_spending) * 100
        formatted_amount = format_currency(amount, user['currency'])
        summary_text += f"• {category}: {formatted_amount} ({percentage:.1f}%)\n"
    
    # Generate pie chart
    chart_buffer = generate_pie_chart(spending_by_category, user['currency'])
    
    # Send text summary first
    await update.message.reply_text(summary_text)
    
    # Send chart as photo
    chart_buffer.seek(0)
    await update.message.reply_photo(
        photo=chart_buffer,
        caption=f"📊 {period_name} Spending Chart"
    )
    
    chart_buffer.close()

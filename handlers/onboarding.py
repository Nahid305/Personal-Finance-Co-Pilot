from telegram import Update
from telegram.ext import ContextTypes
from database.db_operations import db_ops

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "there"
    
    # Check if user exists
    user = await db_ops.get_user(user_id)
    
    if not user:
        # New user - add to database with default currency
        await db_ops.add_user(user_id, 'INR')
        
        welcome_message = (
            f"🎉 Welcome to Personal Finance Co-Pilot, {user_name}! 🎉\n\n"
            "💰 I'm your friendly expense tracking companion! I'll help you:\n"
            "• 📝 Track expenses in just 3 seconds\n"
            "• 📊 Set and monitor budgets\n"
            "• 📈 Get beautiful spending insights\n"
            "• 🔒 Keep all your data private and secure\n\n"
            
            "� **Quick Start Guide:**\n"
            "1️⃣ Try logging an expense: `/log 50 on #coffee for morning latte`\n"
            "2️⃣ Set a budget: `/budget #coffee 200`\n"
            "3️⃣ View your summary: `/summary`\n\n"
            
            "⚙️ **Setup:**\n"
            f"📍 Your currency is set to **INR** (₹)\n"
            "🌍 Change it anytime: `/setcurrency USD` (or EUR, GBP, etc.)\n\n"
            
            "📚 **Need help?** Type `/help` for all commands\n\n"
            "🎯 **Let's start tracking!** Try your first expense now! �"
        )
    else:
        welcome_message = (
            f"👋 Hey {user_name}, welcome back to Finance Co-Pilot!\n\n"
            f"💳 Your currency: **{user['currency']}**\n"
            f"📊 Ready to log some expenses?\n\n"
            
            "🔥 **Quick Commands:**\n"
            "• `/log 25 on #lunch` - Log an expense\n"
            "• `/summary` - See your spending\n"
            "• `/help` - View all options\n\n"
            
            "💡 **Tip:** The faster you log, the better your insights become!"
        )
    
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    user_name = update.effective_user.first_name or "Friend"
    
    help_text = (
        f"🤖 **Finance Co-Pilot Commands for {user_name}**\n\n"
        
        "💰 **Expense Tracking** (The main thing!):\n"
        "`/log <amount> on #<category> [for <description>]`\n"
        "   💡 Example: `/log 150 on #food for pizza night`\n"
        "`/spent` - Same as /log (shorter to type!)\n"
        "`/listhistory [N]` - Show your last N expenses\n"
        "`/delete <ID>` - Remove a wrong entry\n\n"
        
        "📊 **Budget Management** (Stay on track!):\n"
        "`/budget #<category> <amount>` - Set monthly limit\n"
        "   💡 Example: `/budget #groceries 8000`\n"
        "`/viewbudgets` - See progress on all budgets\n\n"
        
        "📈 **Reports & Insights** (The fun part!):\n"
        "`/summary [period]` - Beautiful charts + breakdown\n"
        "   📅 Periods: today, week, month, year\n"
        "   💡 Try: `/summary week` or just `/summary`\n\n"
        
        "⚙️ **Settings**:\n"
        "`/setcurrency <code>` - USD, EUR, INR, GBP, JPY, CAD, AUD\n\n"
        
        "🎯 **Pro Tips**:\n"
        "• Use hashtags for categories: #food #transport #fun\n"
        "• Descriptions help you remember later\n"
        "• Set budgets to get smart alerts\n"
        "• Check weekly summaries every Sunday\n"
        "• All data stays on YOUR device - completely private!\n\n"
        
        "🚀 **Start with:** `/log 50 on #coffee` and see the magic! ✨"
    )
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def setcurrency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /setcurrency command."""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "there"
    
    if not context.args:
        await update.message.reply_text(
            f"Hey {user_name}! 🌍 Please tell me your preferred currency:\n\n"
            "**Usage:** `/setcurrency <CODE>`\n"
            "**Example:** `/setcurrency USD`\n\n"
            "🌟 **Supported currencies:**\n"
            "💵 USD - US Dollar\n"
            "💶 EUR - Euro\n"
            "₹ INR - Indian Rupee\n"
            "💷 GBP - British Pound\n"
            "¥ JPY - Japanese Yen\n"
            "🍁 CAD - Canadian Dollar\n"
            "🦘 AUD - Australian Dollar\n\n"
            "Pick your favorite! 😊",
            parse_mode='Markdown'
        )
        return
    
    currency = context.args[0].upper()
    
    # List of supported currencies
    supported_currencies = ['INR', 'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD']
    currency_names = {
        'INR': 'Indian Rupee (₹)',
        'USD': 'US Dollar ($)',
        'EUR': 'Euro (€)',
        'GBP': 'British Pound (£)',
        'JPY': 'Japanese Yen (¥)',
        'CAD': 'Canadian Dollar (C$)',
        'AUD': 'Australian Dollar (A$)'
    }
    
    if currency not in supported_currencies:
        await update.message.reply_text(
            f"Oops! 😅 '{currency}' isn't supported yet.\n\n"
            "🌟 **Choose from these currencies:**\n" +
            "\n".join([f"• {code} - {name}" for code, name in currency_names.items()]) +
            "\n\nExample: `/setcurrency USD`",
            parse_mode='Markdown'
        )
        return
    
    # Update user's currency
    success = await db_ops.update_user_currency(user_id, currency)
    
    if success:
        currency_name = currency_names[currency]
        await update.message.reply_text(
            f"🎉 Perfect, {user_name}! \n\n"
            f"Your currency is now set to **{currency_name}**\n\n"
            f"💡 All your expenses will now show in {currency}!\n"
            f"Ready to log some expenses? Try: `/log 50 on #coffee`",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "😔 Something went wrong updating your currency. Please try again!"
        )

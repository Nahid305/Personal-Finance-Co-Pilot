import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN, BOT_NAME, BOT_VERSION
from database.db_setup import create_tables
from handlers.onboarding import start_command, help_command, setcurrency_command
from handlers.expenses import log_expense_command, delete_transaction_command, list_history_command
from handlers.budgets import budget_command, view_budgets_command
from handlers.reports import summary_command

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def print_startup_banner():
    """Print a friendly startup banner."""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  💰 {BOT_NAME}                              ║
║                                                              ║
║  🚀 Version: {BOT_VERSION}                                         ║
║  🤖 Your friendly expense tracking companion!               ║
║                                                              ║
║  ✨ Features Ready:                                          ║
║  • 📝 Quick expense logging                                  ║
║  • 📊 Smart budget management                                ║
║  • 📈 Beautiful visual reports                               ║
║  • 🔒 Complete privacy (local storage only)                 ║
║  • 🌍 Multi-currency support                                ║
║                                                              ║
║  🎯 Bot is starting up... Get ready to track! 💪           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Start the Personal Finance Co-Pilot bot."""
    # Print startup banner
    print_startup_banner()
    
    # Initialize database
    create_tables()
    logger.info("✅ Database initialized successfully")
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('setcurrency', setcurrency_command))
    
    # Expense tracking handlers
    application.add_handler(CommandHandler('log', log_expense_command))
    application.add_handler(CommandHandler('spent', log_expense_command))  # Alias for log
    application.add_handler(CommandHandler('delete', delete_transaction_command))
    application.add_handler(CommandHandler('listhistory', list_history_command))
    
    # Budget management handlers
    application.add_handler(CommandHandler('budget', budget_command))
    application.add_handler(CommandHandler('viewbudgets', view_budgets_command))
    
    # Reports handler
    application.add_handler(CommandHandler('summary', summary_command))
    
    # Error handler
    async def error_handler(update, context):
        """Handle errors."""
        logger.error(f"❌ Update {update} caused error {context.error}")
    
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info(f"🚀 {BOT_NAME} is starting...")
    logger.info("📱 Ready to help users track their expenses!")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()

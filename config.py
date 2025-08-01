import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Config
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Bot Configuration
BOT_NAME = "💰 Personal Finance Co-Pilot"
BOT_USERNAME = "PersonalFinanceCoPlitBot"  # You can set this via BotFather
BOT_VERSION = "1.0.0"
BOT_DESCRIPTION = "Your friendly expense tracking companion! 🚀"

# Personality Settings
BOT_PERSONALITY = {
    'friendly': True,
    'use_emojis': True,
    'casual_tone': True,
    'encouraging': True
}

# Default Settings
DEFAULT_CURRENCY = 'INR'
MAX_HISTORY_LIMIT = 50
DEFAULT_HISTORY_LIMIT = 10

# Supported Currencies with friendly names
SUPPORTED_CURRENCIES = {
    'INR': '₹',
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    'CAD': 'C$',
    'AUD': 'A$'
}

CURRENCY_NAMES = {
    'INR': 'Indian Rupee (₹)',
    'USD': 'US Dollar ($)',
    'EUR': 'Euro (€)',
    'GBP': 'British Pound (£)',
    'JPY': 'Japanese Yen (¥)',
    'CAD': 'Canadian Dollar (C$)',
    'AUD': 'Australian Dollar (A$)'
}

# Sample categories for suggestions
POPULAR_CATEGORIES = [
    '#food', '#transport', '#shopping', '#entertainment', 
    '#bills', '#health', '#education', '#coffee', '#groceries'
]
# 💰 Personal Finance Co-Pilot Bot

<div align="center">

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-Latest-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

**🤖 Your friendly expense tracking companion on Telegram!**

*Track expenses in seconds, manage budgets smartly, and get beautiful insights - all while keeping your data completely private.*

[🚀 Quick Start](#-quick-start) • [📱 Features](#-features) • [🔧 Installation](#-installation) • [📖 Usage](#-usage) • [🤝 Contributing](#-contributing)

</div>

---

## 🌟 Features

### 💰 **Smart Expense Tracking**
- ⚡ **3-Second Logging**: Log expenses with natural language
- 🏷️ **Category System**: Organize with hashtags (#food, #transport, etc.)
- 📝 **Optional Descriptions**: Add context to your expenses
- 🗑️ **Easy Deletion**: Remove incorrect entries by ID

### 📊 **Intelligent Budget Management**
- 💳 **Monthly Budgets**: Set spending limits for any category
- 🚨 **Smart Alerts**: Get warnings at 80% and alerts at 100%
- 📈 **Visual Progress**: See spending progress with beautiful bars
- 🎯 **Real-time Tracking**: Know exactly where you stand

### 📈 **Beautiful Reports & Analytics**
- 🥧 **Pie Charts**: Visual spending breakdowns with Matplotlib
- 📅 **Flexible Periods**: Today, week, month, or year summaries
- 🏆 **Category Analysis**: Understand your spending patterns
- 📊 **Export Ready**: Charts saved as images

### 🔒 **Privacy-First Design**
- 🏠 **Local Storage**: All data in SQLite on your device
- 🚫 **No Cloud**: Your financial data never leaves your device
- 👤 **User Isolation**: Each user's data completely separate
- 🔐 **No Tracking**: Zero analytics or external data sharing

### 🌍 **Multi-Currency Support**
- 💵 USD, 💶 EUR, ₹ INR, 💷 GBP, ¥ JPY, 🍁 CAD, 🦘 AUD
- 🔄 **Easy Switching**: Change currency anytime
- 💱 **Proper Formatting**: Currency symbols and formatting

---

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.10 or higher
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### ⚡ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/personal-finance-copilot.git
   cd personal-finance-copilot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your bot token:
   ```
   TELEGRAM_TOKEN=your_bot_token_here
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

5. **Start using:**
   - Search for your bot on Telegram
   - Send `/start` to begin tracking!

---

## 📱 Usage

### 🎯 **Core Commands**

#### **Getting Started**
```bash
/start          # Initialize your account with a warm welcome
/help           # Comprehensive command guide with examples
/setcurrency    # Set your preferred currency (USD, EUR, INR, etc.)
```

#### **💰 Expense Tracking**
```bash
# Log expenses with natural language
/log 150 on #food for lunch at cafe
/log 2500 on #electronics for new headphones  
/log 80 on #transport

# Alternative command
/spent 45 on #coffee for morning latte

# View and manage history
/listhistory           # Show last 10 transactions
/listhistory 20        # Show last 20 transactions
/delete 123            # Delete transaction with ID 123
```

#### **📊 Budget Management**
```bash
# Set monthly budgets
/budget #groceries 8000
/budget #entertainment 2000
/budget #transport 1500

# View all budgets with progress
/viewbudgets
```

#### **� Reports & Analytics**
```bash
# Get beautiful summaries with charts
/summary              # Current month (default)
/summary week         # This week's spending
/summary today        # Today's expenses
/summary year         # Annual overview
```

### 🏷️ **Category System**

Use hashtags to categorize expenses:
- `#food` - Restaurants, groceries, snacks
- `#transport` - Uber, gas, public transit, parking
- `#shopping` - Clothes, electronics, household items
- `#bills` - Utilities, rent, subscriptions, insurance
- `#entertainment` - Movies, games, concerts, streaming
- `#health` - Medical, pharmacy, gym, wellness
- `#education` - Books, courses, training, workshops
- `#coffee` - Your daily caffeine fix ☕
- `#groceries` - Weekly shopping trips

*Create any category you want - the bot learns from your usage!*

### 💡 **Pro Tips**

1. **⚡ Speed Logging**: The faster you log, the better your insights
2. **🏷️ Consistent Categories**: Use the same category names for better analysis
3. **📊 Set Budgets**: Get smart alerts before overspending
4. **📅 Weekly Reviews**: Check `/summary week` every Sunday
5. **🗑️ Clean Data**: Delete mistakes immediately with `/delete`
6. **📝 Add Context**: Descriptions help you remember later

---

## 🏗️ Project Structure

```
personal-finance-copilot/
│
├── main.py                    # 🚀 Main bot entry point
├── config.py                  # ⚙️ Configuration settings
├── requirements.txt           # 📦 Python dependencies
├── .env.example              # 🔐 Environment template
├── README.md                 # 📖 This file
│
├── database/
│   ├── __init__.py
│   ├── db_setup.py           # 🗄️ SQLite table creation
│   └── db_operations.py      # 📝 Database CRUD operations
│
├── handlers/
│   ├── __init__.py
│   ├── onboarding.py         # 🎯 /start, /help, /setcurrency
│   ├── expenses.py           # 💰 /log, /delete, /listhistory
│   ├── budgets.py            # 📊 /budget, /viewbudgets
│   └── reports.py            # 📈 /summary with charts
│
└── utils/
    ├── __init__.py
    └── chart_generator.py     # 📊 Matplotlib chart creation
```

---

## 🗄️ Database Schema

### **Users Table**
```sql
users (
    user_id INTEGER PRIMARY KEY,        -- Telegram User ID
    currency TEXT DEFAULT 'INR',        -- User's preferred currency
    created_at TIMESTAMP DEFAULT NOW    -- Account creation date
)
```

### **Transactions Table**
```sql
transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique transaction ID
    user_id INTEGER,                       -- Foreign key to users
    amount REAL NOT NULL,                  -- Transaction amount
    category TEXT NOT NULL,                -- Category with # prefix
    description TEXT,                      -- Optional description
    transaction_date TIMESTAMP DEFAULT NOW -- When recorded
)
```

### **Budgets Table**
```sql
budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique budget ID
    user_id INTEGER,                       -- Foreign key to users
    category TEXT NOT NULL,                -- Budget category
    amount REAL NOT NULL,                  -- Monthly budget limit
    UNIQUE(user_id, category)              -- One budget per category per user
)
```

---

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file:
```bash
TELEGRAM_TOKEN=your_telegram_bot_token_here
```

### **Supported Currencies**
```python
SUPPORTED_CURRENCIES = {
    'INR': '₹',     # Indian Rupee
    'USD': '$',     # US Dollar  
    'EUR': '€',     # Euro
    'GBP': '£',     # British Pound
    'JPY': '¥',     # Japanese Yen
    'CAD': 'C$',    # Canadian Dollar
    'AUD': 'A$'     # Australian Dollar
}
```

---

## 🛡️ Privacy & Security

### **🔒 Privacy Guarantees**
- ✅ **Local Storage Only**: All data in SQLite database on your device
- ✅ **No Cloud Services**: Zero external data storage
- ✅ **No Analytics**: No usage tracking or behavioral analysis
- ✅ **User Isolation**: Each user's data completely separate
- ✅ **Open Source**: Full transparency of data handling

### **🔐 Security Features**
- ✅ **No Sensitive Data**: Only expense amounts and categories stored
- ✅ **Local Processing**: All calculations done locally
- ✅ **Minimal Permissions**: Bot only needs message access
- ✅ **No File Access**: Bot cannot access your device files

---

## 🚀 Deployment

### **Local Development**
```bash
git clone https://github.com/yourusername/personal-finance-copilot.git
cd personal-finance-copilot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your bot token
python main.py
```

### **Production Deployment**
1. **VPS/Server**: Deploy on any Linux server with Python 3.10+
2. **Docker**: Use the provided Dockerfile (coming soon)
3. **Heroku**: Deploy with the included Procfile (coming soon)
4. **Railway**: One-click deployment (coming soon)

---

## 🤝 Contributing

We love contributions! Here's how you can help:

### **🐛 Bug Reports**
- Use GitHub Issues
- Include bot version and Python version
- Provide steps to reproduce
- Share relevant logs (remove sensitive data)

### **💡 Feature Requests**
- Open a GitHub Issue with the `enhancement` label
- Describe the use case
- Explain the expected behavior

### **� Pull Requests**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### **📝 Documentation**
- Improve README
- Add code comments
- Write tutorials
- Create examples

---

## 📊 Roadmap

### **🎯 Upcoming Features**
- [ ] 📱 Inline keyboards for better UX
- [ ] 🏦 Multiple account support
- [ ] 📊 Advanced analytics and trends
- [ ] 📤 Export data to CSV/Excel
- [ ] 🔔 Scheduled budget reminders
- [ ] 📸 Receipt photo processing
- [ ] 🎨 Custom chart themes
- [ ] 🌐 Web dashboard

### **🔮 Future Ideas**
- [ ] 🤖 AI-powered expense categorization
- [ ] 📈 Investment tracking
- [ ] 💳 Bank integration (secure, local)
- [ ] 👥 Family shared budgets
- [ ] 🎯 Financial goal setting

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Personal Finance Co-Pilot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- **📱 Telegram Bot API**: For the excellent bot platform
- **🐍 python-telegram-bot**: Amazing Python library
- **📊 Matplotlib**: Beautiful chart generation
- **🗄️ SQLite**: Reliable local database
- **💰 Community**: All the users who make this better

---

## 📞 Support

### **💬 Get Help**
- 📖 **Documentation**: Read this README thoroughly
- 🐛 **Issues**: Check existing GitHub issues
- 💡 **Discussions**: Use GitHub Discussions for questions
- 📧 **Contact**: [your-email@example.com]

### **🚀 Quick Links**
- 🤖 **Bot**: [@Nahid77_bot](https://t.me/Nahid77_bot)
- 📱 **Telegram**: Direct link to bot
- 🔗 **GitHub**: This repository
- 📊 **Demo**: Try it live!

---

<div align="center">

**⭐ If this project helped you, please give it a star! ⭐**

*Made with ❤️ for privacy-conscious financial tracking*

**🚀 Start tracking your expenses today!**

[⬆ Back to Top](#-personal-finance-co-pilot-bot)

</div>

import sqlite3
import os
from datetime import datetime

DATABASE_PATH = 'personal_finance.db'

def create_tables():
    """Create the database tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            currency TEXT NOT NULL DEFAULT 'INR',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Create budgets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            UNIQUE(user_id, category),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()

import sqlite3
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

DATABASE_PATH = 'personal_finance.db'

class DatabaseOperations:
    def __init__(self):
        self.db_path = DATABASE_PATH
    
    async def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False):
        """Execute a database query asynchronously."""
        def _execute():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                if fetch_one:
                    result = cursor.fetchone()
                elif fetch_all:
                    result = cursor.fetchall()
                else:
                    result = cursor.rowcount
                conn.commit()
                return result
            finally:
                conn.close()
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _execute)
    
    async def add_user(self, user_id: int, currency: str = 'INR') -> bool:
        """Add a new user to the database."""
        query = "INSERT OR IGNORE INTO users (user_id, currency) VALUES (?, ?)"
        result = await self.execute_query(query, (user_id, currency))
        return result > 0
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user information."""
        query = "SELECT user_id, currency, created_at FROM users WHERE user_id = ?"
        result = await self.execute_query(query, (user_id,), fetch_one=True)
        if result:
            return {
                'user_id': result[0],
                'currency': result[1],
                'created_at': result[2]
            }
        return None
    
    async def update_user_currency(self, user_id: int, currency: str) -> bool:
        """Update user's currency preference."""
        query = "UPDATE users SET currency = ? WHERE user_id = ?"
        result = await self.execute_query(query, (currency, user_id))
        return result > 0
    
    async def log_expense(self, user_id: int, amount: float, category: str, description: str = None) -> bool:
        """Log a new expense."""
        query = "INSERT INTO transactions (user_id, amount, category, description) VALUES (?, ?, ?, ?)"
        result = await self.execute_query(query, (user_id, amount, category, description))
        return result > 0
    
    async def delete_transaction(self, user_id: int, transaction_id: int) -> bool:
        """Delete a transaction if it belongs to the user."""
        query = "DELETE FROM transactions WHERE id = ? AND user_id = ?"
        result = await self.execute_query(query, (transaction_id, user_id))
        return result > 0
    
    async def get_transaction_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's transaction history."""
        query = '''
            SELECT id, amount, category, description, transaction_date 
            FROM transactions 
            WHERE user_id = ? 
            ORDER BY transaction_date DESC 
            LIMIT ?
        '''
        results = await self.execute_query(query, (user_id, limit), fetch_all=True)
        
        transactions = []
        for row in results:
            transactions.append({
                'id': row[0],
                'amount': row[1],
                'category': row[2],
                'description': row[3],
                'date': row[4]
            })
        return transactions
    
    async def set_budget(self, user_id: int, category: str, amount: float) -> bool:
        """Set or update a budget for a category."""
        query = "INSERT OR REPLACE INTO budgets (user_id, category, amount) VALUES (?, ?, ?)"
        result = await self.execute_query(query, (user_id, category, amount))
        return result > 0
    
    async def get_budgets(self, user_id: int) -> List[Dict]:
        """Get all budgets for a user."""
        query = "SELECT category, amount FROM budgets WHERE user_id = ?"
        results = await self.execute_query(query, (user_id,), fetch_all=True)
        
        budgets = []
        for row in results:
            budgets.append({
                'category': row[0],
                'amount': row[1]
            })
        return budgets
    
    async def get_spending_by_category(self, user_id: int, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """Get spending by category for a date range."""
        query = '''
            SELECT category, SUM(amount) as total
            FROM transactions 
            WHERE user_id = ? AND transaction_date BETWEEN ? AND ?
            GROUP BY category
        '''
        results = await self.execute_query(query, (user_id, start_date.isoformat(), end_date.isoformat()), fetch_all=True)
        
        spending = {}
        for row in results:
            spending[row[0]] = row[1]
        return spending
    
    async def get_total_spending(self, user_id: int, start_date: datetime, end_date: datetime) -> float:
        """Get total spending for a date range."""
        query = '''
            SELECT SUM(amount) 
            FROM transactions 
            WHERE user_id = ? AND transaction_date BETWEEN ? AND ?
        '''
        result = await self.execute_query(query, (user_id, start_date.isoformat(), end_date.isoformat()), fetch_one=True)
        return result[0] if result[0] else 0.0
    
    async def get_current_month_spending_by_category(self, user_id: int, category: str) -> float:
        """Get current month spending for a specific category."""
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = datetime(now.year, now.month + 1, 1) - timedelta(seconds=1) if now.month < 12 else datetime(now.year + 1, 1, 1) - timedelta(seconds=1)
        
        query = '''
            SELECT SUM(amount) 
            FROM transactions 
            WHERE user_id = ? AND category = ? AND transaction_date BETWEEN ? AND ?
        '''
        result = await self.execute_query(query, (user_id, category, start_of_month.isoformat(), end_of_month.isoformat()), fetch_one=True)
        return result[0] if result[0] else 0.0
    
    async def get_budget_for_category(self, user_id: int, category: str) -> Optional[float]:
        """Get budget amount for a specific category."""
        query = "SELECT amount FROM budgets WHERE user_id = ? AND category = ?"
        result = await self.execute_query(query, (user_id, category), fetch_one=True)
        return result[0] if result else None

# Global instance
db_ops = DatabaseOperations()

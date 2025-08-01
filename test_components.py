#!/usr/bin/env python3
"""
Test script for Personal Finance Co-Pilot Bot
Validates all core components without requiring a Telegram token
"""

import asyncio
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(__file__))

async def test_database_operations():
    """Test database operations"""
    print("🗄️ Testing Database Operations...")
    
    try:
        from database.db_setup import create_tables
        from database.db_operations import db_ops
        
        # Create tables
        create_tables()
        print("✅ Database tables created")
        
        # Test user operations
        test_user_id = 12345
        await db_ops.add_user(test_user_id, 'USD')
        user = await db_ops.get_user(test_user_id)
        print(f"✅ User operations: {user['currency']}")
        
        # Test expense logging
        await db_ops.log_expense(test_user_id, 50.0, '#food', 'test meal')
        print("✅ Expense logging")
        
        # Test budget setting
        await db_ops.set_budget(test_user_id, '#food', 500.0)
        print("✅ Budget setting")
        
        # Test transaction history
        history = await db_ops.get_transaction_history(test_user_id, 5)
        print(f"✅ Transaction history: {len(history)} transactions")
        
        print("🗄️ Database operations: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_chart_generation():
    """Test chart generation"""
    print("📊 Testing Chart Generation...")
    
    try:
        from utils.chart_generator import generate_pie_chart, format_currency
        
        # Test currency formatting
        formatted = format_currency(150.50, 'USD')
        print(f"✅ Currency formatting: {formatted}")
        
        # Test chart generation
        test_data = {
            '#food': 150.0,
            '#transport': 80.0,
            '#entertainment': 200.0
        }
        
        chart_buffer = generate_pie_chart(test_data, 'USD')
        print(f"✅ Chart generation: {len(chart_buffer.getvalue())} bytes")
        chart_buffer.close()
        
        print("📊 Chart generation: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"❌ Chart generation test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("⚙️ Testing Configuration...")
    
    try:
        from config import SUPPORTED_CURRENCIES, DEFAULT_CURRENCY
        
        print(f"✅ Default currency: {DEFAULT_CURRENCY}")
        print(f"✅ Supported currencies: {len(SUPPORTED_CURRENCIES)}")
        
        print("⚙️ Configuration: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_handler_imports():
    """Test handler imports"""
    print("🤖 Testing Handler Imports...")
    
    try:
        from handlers.onboarding import start_command, help_command
        from handlers.expenses import log_expense_command
        from handlers.budgets import budget_command
        from handlers.reports import summary_command
        
        print("✅ Onboarding handlers")
        print("✅ Expense handlers")  
        print("✅ Budget handlers")
        print("✅ Report handlers")
        
        print("🤖 Handler imports: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"❌ Handler import test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Personal Finance Co-Pilot Bot - Component Tests")
    print("=" * 50)
    
    tests = [
        ('Configuration', test_configuration),
        ('Handler Imports', test_handler_imports),
        ('Chart Generation', test_chart_generation),
        ('Database Operations', lambda: asyncio.create_task(test_database_operations()))
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutine(test_func()) or hasattr(test_func(), '__await__'):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}\n")
    
    print("🎯 Test Summary")
    print("=" * 50)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Bot is ready for deployment.")
        print("\n📝 Next Steps:")
        print("1. Add your Telegram bot token to .env file")
        print("2. Run: python main.py")
        print("3. Test with your bot on Telegram")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = asyncio.run(main())

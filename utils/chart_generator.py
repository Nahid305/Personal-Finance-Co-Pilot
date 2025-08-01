import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Dict
import io
import os

def generate_pie_chart(spending_data: Dict[str, float], currency: str = 'INR') -> io.BytesIO:
    """
    Generate a pie chart for spending data and return as BytesIO object.
    
    Args:
        spending_data: Dictionary with category as key and amount as value
        currency: Currency symbol to display
    
    Returns:
        BytesIO object containing the chart image
    """
    if not spending_data:
        # Create empty chart
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'No expenses to display', ha='center', va='center', 
                transform=ax.transAxes, fontsize=16)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    else:
        # Extract categories and amounts
        categories = list(spending_data.keys())
        amounts = list(spending_data.values())
        
        # Create the pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Define colors for categories
        colors = plt.cm.Set3(range(len(categories)))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct='%1.1f%%',
                                         startangle=90, colors=colors)
        
        # Customize the appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Add title
        total_amount = sum(amounts)
        currency_symbols = {
            'INR': '₹',
            'USD': '$',
            'EUR': '€',
            'GBP': '£'
        }
        symbol = currency_symbols.get(currency, currency)
        
        ax.set_title(f'Spending Breakdown\nTotal: {symbol}{total_amount:.2f}', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        
        # Add legend with amounts
        legend_labels = [f'{cat}: {symbol}{amt:.2f}' for cat, amt in spending_data.items()]
        ax.legend(wedges, legend_labels, title="Categories", loc="center left", 
                 bbox_to_anchor=(1, 0, 0.5, 1))
    
    # Set the background color
    fig.patch.set_facecolor('white')
    
    # Save to BytesIO
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    img_buffer.seek(0)
    
    # Close the figure to free memory
    plt.close(fig)
    
    return img_buffer

def format_currency(amount: float, currency: str) -> str:
    """Format amount with appropriate currency symbol."""
    currency_symbols = {
        'INR': '₹',
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CAD': 'C$',
        'AUD': 'A$'
    }
    
    symbol = currency_symbols.get(currency.upper(), currency)
    return f'{symbol}{amount:.2f}'

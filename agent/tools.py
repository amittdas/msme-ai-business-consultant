from langchain.tools import tool
from utils.business_analysis import (
    calculate_profit,
    highest_sales,
    highest_profit,
    quarterly_summary
)

@tool
def get_profit(month: str) -> str:
    """
    Returns the profit for a given month.
    Example input: May-23
    """

    profit = calculate_profit(month)

    if profit is None:
        return "Month not found."

    return f"Profit in {month} is ₹{profit:,}"


@tool
def get_highest_sales(dummy: str = "") -> str:
    """
    Returns the month with the highest sales.
    """

    month, sales = highest_sales()

    return f"Highest sales were in {month}: ₹{sales:,}"


@tool
def get_highest_profit(dummy: str = "") -> str:
    """
    Returns the month with the highest profit.
    """

    month, profit = highest_profit()

    return f"Highest profit was in {month}: ₹{profit:,}"


@tool
def get_q1_summary(dummy: str = "") -> str:
    """
    Returns the business summary for Q1.
    """

    summary = quarterly_summary()

    return f"""
Q1 Business Summary

Total Sales: ₹{summary['sales']:,}

Total Expenses: ₹{summary['expenses']:,}

Net Profit: ₹{summary['profit']:,}
"""

from utils.business_analysis import get_dataframe

def generate_recommendations():

    df = get_dataframe()

    recommendations = []

    # Highest inventory
    max_inventory = df.loc[df["InventoryCost"].idxmax()]

    recommendations.append(
        f"Reduce inventory in {max_inventory['Month']} because inventory cost reached ₹{max_inventory['InventoryCost']:,}."
    )

    # Lowest marketing
    min_marketing = df.loc[df["MarketingSpend"].idxmin()]

    recommendations.append(
        f"Marketing spend was lowest in {min_marketing['Month']} (₹{min_marketing['MarketingSpend']:,}). Consider increasing promotions."
    )

    # Highest sales
    max_sales = df.loc[df["Sales"].idxmax()]

    recommendations.append(
        f"Highest sales occurred in {max_sales['Month']}. Study this month's strategy and repeat it."
    )

    # Highest expenses
    max_expense = df.loc[df["Expenses"].idxmax()]

    recommendations.append(
        f"Expenses peaked in {max_expense['Month']}. Review operational costs."
    )

    return recommendations

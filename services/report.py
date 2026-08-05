from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from utils.business_analysis import (
    total_sales,
    total_expenses,
    total_profit,
    highest_sales,
    highest_profit
)

from services.recommendation import generate_recommendations


def generate_pdf():

    doc = SimpleDocTemplate("Business_Report.pdf")

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>MSME Business Analysis Report</b>", styles["Title"])
    )

    story.append(
        Paragraph(f"Total Sales : ₹{total_sales():,}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Total Expenses : ₹{total_expenses():,}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Total Profit : ₹{total_profit():,}", styles["BodyText"])
    )

    month, sales = highest_sales()

    story.append(
        Paragraph(f"Highest Sales : {month} (₹{sales:,})", styles["BodyText"])
    )

    month, profit = highest_profit()

    story.append(
        Paragraph(f"Highest Profit : {month} (₹{profit:,})", styles["BodyText"])
    )

    story.append(
        Paragraph("<br/><b>AI Recommendations</b>", styles["Heading2"])
    )

    for rec in generate_recommendations():

        story.append(
            Paragraph("• " + rec, styles["BodyText"])
        )

    doc.build(story)

    return "Business_Report.pdf"

import os
import shutil
import pandas as pd

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_PATH = os.path.join(BASE_DIR, "data", "business_data.csv")
DB_PATH = os.path.join(BASE_DIR, "chroma_db")


def rebuild_database():

    # Delete old database
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    df = pd.read_csv(CSV_PATH)

    docs = []

    for _, row in df.iterrows():

        text = f"""
Month: {row['Month']}
Sales: {row['Sales']}
Expenses: {row['Expenses']}
Customers: {row['Customers']}
Inventory Cost: {row['InventoryCost']}
Marketing Spend: {row['MarketingSpend']}
"""

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "month": row["Month"]
                }
            )
        )

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=DB_PATH
    )

    return True

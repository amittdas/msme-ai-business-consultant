import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma


# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_PATH = os.path.join(BASE_DIR, "data", "business_data.csv")
DB_PATH = os.path.join(BASE_DIR, "chroma_db")


# -------------------------
# Load CSV
# -------------------------
df = pd.read_csv(CSV_PATH)

documents = []

for _, row in df.iterrows():

    text = f"""
Month: {row['Month']}
Sales: ₹{row['Sales']}
Expenses: ₹{row['Expenses']}
Customers: {row['Customers']}
Inventory Cost: ₹{row['InventoryCost']}
Marketing Spend: ₹{row['MarketingSpend']}
"""

    documents.append(
        Document(
            page_content=text,
            metadata={"month": row["Month"]}
        )
    )


print(f"Loaded {len(documents)} documents")


# -------------------------
# Embedding Model
# -------------------------
embedding_model = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


# -------------------------
# Create ChromaDB
# -------------------------
vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory=DB_PATH
)

print("Embeddings stored successfully!")

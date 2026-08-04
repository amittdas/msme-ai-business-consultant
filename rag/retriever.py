import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

# -------------------------
# Load Embedding Model
# -------------------------
embedding_model = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# -------------------------
# Load Chroma Database
# -------------------------
vectordb = Chroma(
    persist_directory=DB_PATH,
    embedding_function=embedding_model
)

# -------------------------
# Create Retriever
# -------------------------
retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# -------------------------
# Test the Retriever
# -------------------------
query = "What was the profit in May 2023?"

results = retriever.invoke(query)

print("=" * 50)
print("Retrieved Documents")
print("=" * 50)

for i, doc in enumerate(results, start=1):
    print(f"\nDocument {i}")
    print(doc.page_content)

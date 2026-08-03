import os
import re

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

from prompts.prompt import BUSINESS_PROMPT
from utils.business_analysis import (
    calculate_profit,
    highest_sales,
    highest_profit,
    quarterly_summary
)

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

# ----------------------------
# Embedding Model
# ----------------------------
embedding = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# ----------------------------
# Vector Database
# ----------------------------
vectordb = Chroma(
    persist_directory=DB_PATH,
    embedding_function=embedding
)

retriever = vectordb.as_retriever(
    search_kwargs={"k": 3}
)

# ----------------------------
# Llama 3
# ----------------------------
llm = OllamaLLM(
    model="llama3",
    temperature=0.2
)

# ----------------------------
# AI Agent
# ----------------------------
def ask_agent(question):

    q = question.lower()

    # -------- Profit --------
    if "profit" in q:

        months = [
            "Jan-23","Feb-23","Mar-23","Apr-23",
            "May-23","Jun-23","Jul-23","Aug-23",
            "Sep-23","Oct-23"
        ]

        for month in months:

            if month.lower().replace("-", "") in q.replace("-", "") \
                    or month.lower() in q:

                profit = calculate_profit(month)

                if profit is not None:

                    prompt = f"""
You are an AI Business Consultant.

Profit for {month} is ₹{profit:,}.

Explain this in 2-3 professional sentences.
"""

                    return llm.invoke(prompt)

    # -------- Highest Sales --------
    if "highest sales" in q or "maximum sales" in q:

        month, sales = highest_sales()

        prompt = f"""
Highest sales occurred in {month}.

Sales = ₹{sales:,}.

Explain what this means.
"""

        return llm.invoke(prompt)

    # -------- Highest Profit --------
    if "highest profit" in q:

        month, profit = highest_profit()

        prompt = f"""
Highest profit occurred in {month}.

Profit = ₹{profit:,}.

Explain this.
"""

        return llm.invoke(prompt)

    # -------- Quarter Summary --------
    if "q1" in q or "quarter" in q:

        summary = quarterly_summary()

        prompt = f"""
Q1 Summary

Sales = ₹{summary['sales']:,}

Expenses = ₹{summary['expenses']:,}

Profit = ₹{summary['profit']:,}

Write a professional business summary.
"""

        return llm.invoke(prompt)

    # -------- RAG --------
    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = BUSINESS_PROMPT.format(
        context=context,
        question=question
    )

    return llm.invoke(prompt)

import streamlit as st
import plotly.express as px

from agent.business_agent import ask_agent
from ui.sidebar import sidebar

from utils.business_analysis import (
    get_dataframe,
    total_sales,
    total_profit,
    highest_sales,
    highest_profit
)

from services.recommendation import generate_recommendations
from services.report import generate_pdf
from services.forecast import predict_next_month

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="MSME AI Business Consultant",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

sidebar()

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.title("🤖 MSME AI Business Consultant")
st.caption("Generative AI Agent for SME/MSME Business Insights")

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

df = get_dataframe()
df["Profit"] = df["Sales"] - df["Expenses"]

# ----------------------------------------------------
# KPI DASHBOARD
# ----------------------------------------------------

st.header("📊 Business Dashboard")

col1, col2, col3, col4 = st.columns(4)

sales_month, sales = highest_sales()
profit_month, profit = highest_profit()

with col1:
    st.metric(
        "💰 Total Sales",
        f"₹{total_sales():,}"
    )

with col2:
    st.metric(
        "📈 Total Profit",
        f"₹{total_profit():,}"
    )

with col3:
    st.metric(
        "🏆 Highest Sales",
        sales_month,
        f"₹{sales:,}"
    )

with col4:
    st.metric(
        "🥇 Highest Profit",
        profit_month,
        f"₹{profit:,}"
    )

# ----------------------------------------------------
# SALES FORECAST
# ----------------------------------------------------

st.divider()

st.header("📈 AI Sales Forecast")

prediction = predict_next_month()

st.metric(
    "Predicted Next Month Sales",
    f"₹{prediction:,}"
)

st.divider()

# ----------------------------------------------------
# CHARTS
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    sales_chart = px.line(
        df,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales"
    )

    st.plotly_chart(
        sales_chart,
        use_container_width=True
    )

    customer_chart = px.bar(
        df,
        x="Month",
        y="Customers",
        title="Customers"
    )

    st.plotly_chart(
        customer_chart,
        use_container_width=True
    )

with right:

    expense_chart = px.line(
        df,
        x="Month",
        y="Expenses",
        markers=True,
        title="Monthly Expenses"
    )

    st.plotly_chart(
        expense_chart,
        use_container_width=True
    )

    profit_chart = px.bar(
        df,
        x="Month",
        y="Profit",
        title="Monthly Profit"
    )

    st.plotly_chart(
        profit_chart,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# DATASET PREVIEW
# ----------------------------------------------------

with st.expander("📋 View Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# AI RECOMMENDATIONS
# ----------------------------------------------------

st.header("💡 AI Business Recommendations")

recommendations = generate_recommendations()

for rec in recommendations:
    st.success(rec)

st.divider()

# ----------------------------------------------------
# PDF REPORT
# ----------------------------------------------------

st.header("📄 Business Report")

if st.button("Generate PDF Report"):

    pdf = generate_pdf()

    with open(pdf, "rb") as file:

        st.download_button(
            label="⬇ Download Business Report",
            data=file,
            file_name="Business_Report.pdf",
            mime="application/pdf"
        )

st.divider()

# ----------------------------------------------------
# AI CHATBOT
# ----------------------------------------------------

st.header("💬 AI Business Consultant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask anything about your business..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing business..."):

            answer = ask_agent(question)

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

st.divider()

st.caption(
    "Powered by Streamlit • LangChain • Ollama • Llama 3 • ChromaDB • Machine Learning"
)

import streamlit as st
import pandas as pd
import os

from rag.rebuild_db import rebuild_database

DATA_PATH = "data/business_data.csv"


def sidebar():

    st.sidebar.title("⚙️ Settings")

    uploaded = st.sidebar.file_uploader(
        "Upload Business CSV",
        type=["csv"]
    )

    if uploaded is not None:

        df = pd.read_csv(uploaded)

        df.to_csv(DATA_PATH, index=False)

        with st.spinner("Rebuilding AI Database..."):

            rebuild_database()

        st.sidebar.success("Database Updated!")

        st.rerun()

    st.sidebar.divider()

    if st.sidebar.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    st.sidebar.divider()

    st.sidebar.markdown("### About")

    st.sidebar.write(
        "Generative AI Agent for SME/MSME Business Insights"
    )

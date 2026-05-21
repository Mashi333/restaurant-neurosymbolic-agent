import streamlit as st

st.set_page_config(
    page_title="Neurosymbolic Restaurant Assistant",
    page_icon="🍽️",
    layout="wide",
)

st.title("🍽️ Neurosymbolic Restaurant Assistant")
st.markdown("""
Welcome to the RAG + LLM + ASP Restaurant Assistant!

This system uses:
- **LLM**: For intent extraction and natural language generation.
- **RAG**: For retrieving menu items, ingredients, and restaurant policies.
- **ASP (Answer Set Programming)**: For strict constraints (budget, allergies, valid combinations).

👈 Please select a page from the sidebar to interact with the system.
""")

st.info("Start by going to the **Chatbot** to order your food.")

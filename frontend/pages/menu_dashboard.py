import streamlit as st
import json
import os

st.set_page_config(page_title="Menu Dashboard", page_icon="📋", layout="wide")

st.title("📋 Menu Dashboard")
st.markdown("View the current menu and policies available to the RAG system.")

menu_path = os.path.join(os.path.dirname(__file__), '../../data/menu/menu.json')

try:
    with open(menu_path, 'r') as f:
        menu_data = json.load(f)
    
    st.subheader("Current Menu Items")
    st.dataframe(menu_data)
except FileNotFoundError:
    st.warning("Menu data not found. Please check data/menu/menu.json")

st.subheader("Restaurant Policies")
st.info("Policies are loaded into the Vector DB for retrieval.")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Allergy Policy:** Strict separation for peanuts.")
with col2:
    st.markdown("**Discount Policy:** 10% off for students.")

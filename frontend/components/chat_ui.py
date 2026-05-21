import streamlit as st

def display_chat_messages(messages):
    """Renders the chat history."""
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "reasoning" in msg and msg["reasoning"]:
                with st.expander("System Reasoning"):
                    st.json(msg["reasoning"])

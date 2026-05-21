import streamlit as st
import sys
import os

# Ensure the root directory is in the path to import backend modules if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from frontend.components.sidebar import render_sidebar
from frontend.components.chat_ui import display_chat_messages
from frontend.components.state_display import render_state_display
from backend.services.chatbot_service import handle_chat
from conversation.state_manager import state_manager

st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")

render_sidebar()

st.title("💬 Order Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your restaurant assistant. What would you like to order?"}
    ]

col_chat, col_state = st.columns([2, 1])

with col_chat:
    display_chat_messages(st.session_state.messages)
    
    if prompt := st.chat_input("Type your message here..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                user_context = st.session_state.get("user_context", {})
                response, reasoning = handle_chat(prompt, user_context)
                
                st.markdown(response)
                with st.expander("System Reasoning"):
                    st.json(reasoning)
                    
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "reasoning": reasoning
            })

with col_state:
    render_state_display(state_manager.get_state())

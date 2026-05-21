import streamlit as st

def render_state_display(state):
    """Renders the current dialog state and goal."""
    st.markdown("### 🧠 Agent State")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Goal", state.get("current_goal", "Idle"))
    with col2:
        st.metric("Missing Info", len(state.get("missing_slots", [])))
        
    if state.get("extracted_entities"):
        st.markdown("**Extracted Entities:**")
        st.json(state["extracted_entities"])

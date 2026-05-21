import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Settings & Info")
        st.markdown("Use this sidebar to configure user context for testing.")
        
        st.subheader("Current User Context")
        budget = st.slider("Budget ($)", min_value=5, max_value=50, value=20)
        allergies = st.multiselect("Allergies", ["Peanut", "Dairy", "Gluten", "Shellfish"])
        diet = st.selectbox("Dietary Preference", ["None", "Vegetarian", "Vegan"])
        
        st.session_state["user_context"] = {
            "budget": budget,
            "allergies": allergies,
            "diet": diet
        }
        
        st.markdown("---")
        st.caption("RAG + LLM + ASP System")

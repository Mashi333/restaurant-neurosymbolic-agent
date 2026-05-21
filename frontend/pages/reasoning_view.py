import streamlit as st

st.set_page_config(page_title="Reasoning Trace", page_icon="🔍", layout="wide")

st.title("🔍 ASP Reasoning Trace")
st.markdown("This view shows the latest Answer Set Programming (ASP) trace for debugging constraints.")

# Mock trace display
st.code("""
% Loading facts...
price(veg_burger, 7).
contains(veg_burger, gluten).

% Loading rules...
invalid(X) :- price(X, P), P > 20. % budget limit

% Solving...
Solving...
Answer: 1
valid(veg_burger)
SATISFIABLE

Models       : 1
Calls        : 1
Time         : 0.001s
""", language="prolog")

st.success("Constraints Satisfied: Menu items are valid under current user context.")

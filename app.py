import os
import streamlit as st

# PAGE CONFIG
st.set_page_config(page_title="Digital Twin", page_icon="🧠", layout="wide")

st.title("🧠 Your Digital Twin")
st.write("""
Use the left navigation menu to explore:

- 💬 Chat with your Twin  
- 🙂 Track your mood  
- 🔥 Habits tracking  
- 🧠 Long-term memories  
""")

st.markdown("---")

st.header("Welcome!")

st.write("Select a page from the left sidebar to begin.")

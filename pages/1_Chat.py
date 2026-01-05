import streamlit as st
from digital_twin import ai_reply

st.title("💬 Chat with your Digital Twin")

user_input = st.text_input("Type a message:", "")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please type something!")
    else:
        reply = ai_reply(user_input)
        st.success("Twin: " + reply)

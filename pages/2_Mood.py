# mood_page.py
import streamlit as st
from mood_tracker import add_mood, get_today_mood, get_mood_history

st.title("😊 Mood Tracker")

mood = st.selectbox("How do you feel today?", 
                    ["Happy", "Sad", "Tired", "Angry", "Neutral"])

if st.button("Save Mood"):
    add_mood(mood)
    st.success(f"Mood saved: {mood}")

st.subheader("📅 Today’s Mood:")
st.write(get_today_mood())

st.subheader("📖 Mood History:")
history = get_mood_history()
st.write(history)


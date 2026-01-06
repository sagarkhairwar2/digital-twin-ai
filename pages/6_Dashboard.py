import streamlit as st
from journal import load_journal
import pandas as pd

st.title("📊 Digital Twin Dashboard")

journal = load_journal()

# ----------------------------
# MOOD OVER TIME (already working)
# ----------------------------
st.subheader("😊 Mood Over Time")

mood_data = []
for date, data in journal.items():
    if data.get("mood"):
        mood_data.append({"Date": date, "Mood": data["mood"]})

if mood_data:
    df_mood = pd.DataFrame(mood_data)
    st.line_chart(df_mood.set_index("Date"))
else:
    st.info("No mood data yet.")

# ----------------------------
# HABIT PROGRESS (FIXED)
# ----------------------------
st.subheader("🔥 Habit Progress")

habit_counts = {}

for data in journal.values():
    for habit in data.get("habits", []):
        habit_counts[habit] = habit_counts.get(habit, 0) + 1

if habit_counts:
    df_habits = pd.DataFrame.from_dict(
        habit_counts, orient="index", columns=["Times Completed"]
    )
    st.bar_chart(df_habits)
else:
    st.info("No habit data yet.")

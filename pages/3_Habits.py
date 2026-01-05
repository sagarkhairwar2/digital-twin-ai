import streamlit as st
from habit_tracker import add_habit, mark_habit_done, get_habit_stats

st.title("🔥 Habit Tracker")

# Add habit
new_habit = st.text_input("Add a new habit:")

if st.button("Add Habit"):
    add_habit(new_habit)
    st.success(f"Added new habit: {new_habit}")

# Mark habit as done
habit_done = st.text_input("Which habit did you complete today?")

if st.button("Mark Done"):
    mark_habit_done(habit_done)
    st.success(f"Marked {habit_done} as done today.")

# Show stats
st.subheader("📊 Habit Stats")
stats = get_habit_stats()
st.write(stats)

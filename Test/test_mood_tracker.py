# test_mood_tracker.py

from mood_tracker import add_mood, get_today_mood, get_mood_history

# Test adding mood
add_mood("Happy")

# Test reading today’s mood
print("Today’s mood:", get_today_mood())

# Test mood history
print("Mood history:", get_mood_history())

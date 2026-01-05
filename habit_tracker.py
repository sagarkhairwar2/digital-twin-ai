import json
import os
from datetime import datetime

HABIT_FILE = "habits.json"

# ---------------------------
# Load or create habits file
# ---------------------------
def load_habits():
    if not os.path.exists(HABIT_FILE):
        with open(HABIT_FILE, "w") as f:
            json.dump({}, f)
    with open(HABIT_FILE, "r") as f:
        return json.load(f)

def save_habits(data):
    with open(HABIT_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------
# Add a new habit
# ---------------------------
def add_habit(habit_name):
    data = load_habits()
    if habit_name not in data:
        data[habit_name] = {"days_done": [], "streak": 0}
        save_habits(data)
        print(f"Added new habit: {habit_name}")
    else:
        print(f"Habit already exists: {habit_name}")


# ---------------------------
# Mark habit done for today
# ---------------------------
def mark_habit_done(habit_name):
    data = load_habits()
    today = datetime.now().strftime("%Y-%m-%d")

    if habit_name not in data:
        add_habit(habit_name)
        data = load_habits()

    if today not in data[habit_name]["days_done"]:
        data[habit_name]["days_done"].append(today)
        data[habit_name]["streak"] = len(data[habit_name]["days_done"])
        save_habits(data)

    print(f"Marked {habit_name} as done for today.")


# ---------------------------
# Get stats for all habits
# ---------------------------
def get_habit_stats():
    return load_habits()

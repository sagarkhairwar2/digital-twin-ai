# mood_tracker.py

import json
import os
from datetime import datetime

MOOD_FILE = "moods.json"

# ------------------------
# Save a mood entry
# ------------------------
def add_mood(mood: str):
    today = datetime.now().strftime("%Y-%m-%d")
    
    if os.path.exists(MOOD_FILE):
        with open(MOOD_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[today] = mood

    with open(MOOD_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved mood: {mood}")

# ------------------------
# Get today’s mood
# ------------------------
def get_today_mood():
    today = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(MOOD_FILE):
        return None

    with open(MOOD_FILE, "r") as f:
        data = json.load(f)

    return data.get(today, None)

# ------------------------
# Get full mood history
# ------------------------
def get_mood_history():
    if not os.path.exists(MOOD_FILE):
        return {}

    with open(MOOD_FILE, "r") as f:
        return json.load(f)

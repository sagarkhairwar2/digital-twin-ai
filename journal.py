import json
from datetime import datetime

JOURNAL_FILE = "journal.json"

# ----------------------------
# Load existing journal
# ----------------------------
def load_journal():
    try:
        with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# ----------------------------
# Save journal
# ----------------------------
def save_journal(data):
    with open(JOURNAL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ----------------------------
# Add journal entry
# ----------------------------
def add_journal_entry(text, mood=None, habits_done=None):
    journal = load_journal()
    today = str(datetime.now().date())

    if today not in journal:
        journal[today] = {
            "entries": [],
            "mood": mood,
            "habits": habits_done or []
        }

    journal[today]["entries"].append(text)

    save_journal(journal)
    print("📝 Journal updated!")

# ----------------------------
# Read today's journal
# ----------------------------
def get_today_journal():
    journal = load_journal()
    today = str(datetime.now().date())

    return journal.get(today, {"entries": [], "mood": None, "habits": []})

# ----------------------------
# Generate journal summary prompt for AI
# ----------------------------
def build_journal_summary_prompt():
    today_data = get_today_journal()

    entries = "\n".join(today_data["entries"]) or "No entries yet."
    mood = today_data["mood"] or "Unknown"
    habits = ", ".join(today_data["habits"]) or "None"

    prompt = f"""
Summarize today's activity in a motivational tone.

Mood: {mood}
Habits done: {habits}

Events:
{entries}

Write:
- A short summary
- What I did well
- What I can improve
- One line of encouragement
"""
    return prompt

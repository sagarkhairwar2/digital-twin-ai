import os
import streamlit as st
from groq import Groq
import chromadb
from sentence_transformers import SentenceTransformer
from mood_tracker import add_mood, get_today_mood, get_mood_history
from smart_planner import generate_plan
from habit_tracker import add_habit, mark_habit_done, get_habit_stats
from voice import listen, speak
from journal import add_journal_entry, build_journal_summary_prompt




# SHORT TERM MEMORY (Conversation Buffer)

conversation_history = []
MAX_HISTORY = 5   # store last 5 messages

# ----------------------------
# CONFIG
# ----------------------------

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
# Embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent Chroma DB
chroma_client = chromadb.PersistentClient(path="./db")
collection = chroma_client.get_or_create_collection("memory")


# ----------------------------
# EMBEDDINGS
# ----------------------------
def embed(text):
    return embedding_model.encode(text).tolist()


# ----------------------------
# MEMORY STORE (Long-Term)
# ----------------------------
def store_memory(text):
    data = collection.get()
    new_id = str(len(data.get("ids", [])))

    collection.add(
        ids=[new_id],
        documents=[text],
        embeddings=[embed(text)]
    )
    print(f" Stored → {text}")


# ----------------------------
# MEMORY SEARCH (Long-Term)
# ----------------------------
def search_memory(query, k=3):
    results = collection.query(
        query_embeddings=[embed(query)],
        n_results=k
    )
    return results["documents"][0]


# ----------------------------
# SHORT TERM MEMORY BUFFER
# ----------------------------
conversation_history = []
MAX_HISTORY = 5   # keep last 5 messages only


def add_to_history(role, text):
    conversation_history.append({"role": role, "content": text})
    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)


def get_history_text():
    history_strings = []
    for msg in conversation_history:
        prefix = "You said: " if msg["role"] == "user" else "I replied: "
        history_strings.append(prefix + msg["content"])
    return "\n".join(history_strings)
# ----------------------------
# MEMORY IMPORTANCE CLASSIFIER
# ----------------------------
IMPORTANT_KEYWORDS = [
    "my name is",
    "I am",
    "my birthday is",
    "my exam is",
    "I live in",
    "I study at",
    "I prefer",
    "I like",
    "my goal is",
    "my project is",
    "my dream is"
]

def is_important(text):
    text = text.lower()
    for key in IMPORTANT_KEYWORDS:
        if key in text:
            return True
    return False

# ------------------------------------------------
#  NEW: MEMORY EXTRACTION (IMPORTANT INFORMATION)
# ------------------------------------------------
def extract_memory(user_input):
    """
    Ask LLM if the user's message contains important personal info.
    If yes, return ONLY that info (not explanation).
    If no, return "".
    """

    prompt = f"""
You are an information extraction AI.

Extract ONLY important personal facts from the user's message.

Examples:
User: "My name is Sagar Kumar Khairwar" → return "His name is Sagar Kumar Khairwar"
User: "I study at night" → return "He studies at night"
User: "I live in Bilaspur" → return "He lives in Bilaspur"
User: "I feel tired" → return "" (not important fact)
User: "I am preparing for MTech" → return "He is preparing for MTech"

User message: "{user_input}"

Return ONLY the extracted fact, nothing else. 
If no important fact, return "".
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
    # AUTO-JOURNAL ENTRY
    add_journal_entry(
        text=f"You said: {user_input}\nTwin replied: {ai_output}",
        mood=get_today_mood(),
        habits_done=list(get_habit_stats().keys())
    )
# ----------------------------
# AI DIGITAL TWIN REPLY
# ----------------------------
def ai_reply(user_input):
     # AUTO-STORE IMPORTANT MEMORIES
    if is_important(user_input):
        store_memory(user_input)
    

    # 1. Search long-term memory
    memories = search_memory(user_input)
    memory_text = "\n".join(memories)

    # 2. Load personality
    with open("personality_profile.txt", "r", encoding="utf-8") as f:
        PERSONALITY = f.read()

    # 3. Update short-term memory
    conversation_history.append(f"User: {user_input}")
    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)

    # Prepare short-term memory text
    recent_chat = "\n".join(conversation_history)

    # ----- MOOD DETECTION -----
    user_mood = None

    if any(word in user_input.lower() for word in ["happy", "good", "great", "awesome"]):
        user_mood = "Happy"
    elif any(word in user_input.lower() for word in ["sad", "down", "upset", "bad"]):
        user_mood = "Sad"
    elif any(word in user_input.lower() for word in ["tired", "exhausted", "sleepy"]):
        user_mood = "Tired"
    elif any(word in user_input.lower() for word in ["angry", "mad", "frustrated"]):
        user_mood = "Angry"

    # Store mood if detected
    if user_mood:
        add_mood(user_mood)
        """add_journal_entry(
            text=f"Mood detected: {user_mood}",
            mood=user_mood,
            habits_done=[]
        )"""
    

    # 4. System prompt
    system_prompt = f"""
You are my Digital Twin.

PERSONALITY:
{PERSONALITY}

LONG-TERM MEMORY:
{memory_text}

SHORT-TERM MEMORY (recent conversation):
{recent_chat}

TODAY_MOOD: {get_today_mood()}

RULES:
- Respond in my tone and style
- Be friendly and motivating
- Be concise unless asked otherwise
- Use both long-term and short-term memory
"""

    # 5. Model response
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    # Add AI's response to history
    ai_output = response.choices[0].message.content
    conversation_history.append(f"Twin: {ai_output}")
    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)




    return ai_output




# ----------------------------
# TEST SYSTEM
# ----------------------------

if __name__ == "__main__":
    print(" Digital Twin Ready!")

    while True:
        user_msg = input("\nYou: ")
        if user_msg.lower() in ["exit", "quit", "bye"]:
            print(" Goodbye!")
            break
        
        #  2. Smart Planner — insert THIS block here
        elif any(word in user_msg.lower() for word in ["plan", "schedule", "goal", "work", "today"]):
            plan = generate_plan(user_msg, client)
            print(" Your Smart Plan:\n", plan)
            continue 
            # ----------------------------
        # HABIT TRACKING LOGIC
        # ----------------------------

        if "add habit" in user_msg.lower():
            habit = user_msg.lower().replace("add habit", "").strip()
            add_habit(habit)
            print(f"Twin: Bro, I added your new habit: {habit}")
            continue

        if "i did" in user_msg.lower() or "completed" in user_msg.lower():
            habit = user_msg.lower().replace("i did", "").replace("completed", "").strip()
            mark_habit_done(habit)
            print(f"Twin: Yrr! Great job completing your habit: {habit}")
            continue

        if "habit stats" in user_msg.lower() or "my habits" in user_msg.lower():
            stats = get_habit_stats()
            print("Twin: Bro, here are your habit stats:")
            print(stats)
            continue

        reply = ai_reply(user_msg)
        print("\nTwin:", reply)

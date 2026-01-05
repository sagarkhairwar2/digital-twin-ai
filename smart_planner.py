# smart_planner.py

from datetime import datetime
from memory_store import search_memory

# -----------------------------
#  SMART TASK PLANNER LOGIC
# -----------------------------

def generate_plan(user_input, ai_client):
    """
    Creates a smart plan using:
    - User query
    - Personal memories
    - Today's mood
    """

    # 1. Fetch memories related to planning
    memories = search_memory(user_input, k=5)
    memory_text = "\n".join(memories)

    # 2. Build system prompt
    system_prompt = f"""
You are my Digital Twin and a smart planning assistant.

Use:
- My long-term memories
- My habits
- My mood
- My goals

MEMORY ABOUT ME:
{memory_text}

RULES:
• Create a clear step-by-step plan.
• Prioritize tasks based on urgency + energy level.
• Keep the plan realistic.
• If I feel tired → reduce workload.
• If I feel motivated → push harder.
• Use my tone and slang (bro, yrr, etc.).
"""

    # 3. Ask LLM to create the plan
    response = ai_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content

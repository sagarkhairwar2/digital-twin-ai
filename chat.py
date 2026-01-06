
from digital_twin import ai_reply
from voice import listen, speak
from journal import build_journal_summary_prompt


print("🤖 Digital Twin — Text & Voice Mode Active!")
print("Type 'voice' to switch to voice input.")
print("Type 'text' to switch back to text mode.")
print("Type 'exit' to quit.\n")

mode = "text"

while True:
    if mode == "text":
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Twin: Bye! Talk to you later 👋")
            break

        if user_input.lower() == "voice":
            print("🎤 Switching to voice mode…")
            mode = "voice"
            continue
        if user_input.lower() in ["journal", "summary", "day summary"]:
            prompt = build_journal_summary_prompt()
            result = ai_reply(prompt)
            print("\n📘 Daily Journal Summary:\n", result)
            continue

        response = ai_reply(user_input)
        print("Twin:", response)
        print()

    else:  # VOICE MODE
        user_input = listen()

        if user_input.lower() in ["exit", "quit", "bye"]:
            speak("Bye bro! Talk to you later!")
            break

        if "text mode" in user_input.lower():
            speak("Switching to text mode.")
            mode = "text"
            continue

        response = ai_reply(user_input)
        speak(response)

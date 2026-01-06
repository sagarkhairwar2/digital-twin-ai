from journal import get_all_journal_entries, add_journal_entry
import streamlit as st

st.title("📘 Journal")

# Add new entry
new_entry = st.text_area("Write a journal entry")
if st.button("Save Entry") and new_entry.strip():
    add_journal_entry(new_entry)
    st.success("Entry saved!")

st.divider()
st.subheader("📚 Journal History")

journal_data = get_all_journal_entries()

if not journal_data:
    st.info("No journal entries yet.")
else:
    for date, data in reversed(journal_data.items()):
        st.markdown(f"### 📅 {date}")

        # Mood
        if data.get("mood"):
            st.write(f"🙂 Mood: **{data['mood']}**")

        # Habits
        if data.get("habits"):
            st.write("🔥 Habits done:")
            for habit in data["habits"]:
                st.write(f"- {habit}")

        # Entries
        st.write("📝 Entries:")
        for entry in data.get("entries", []):
            st.write(f"- {entry}")

        st.divider()

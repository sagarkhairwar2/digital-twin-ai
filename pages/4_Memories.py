import streamlit as st
from memory_store import search_memory, get_all_memories

st.title("🧠 Memory Search")

query = st.text_input("Search your memories")

if query:
    results = search_memory(query, k=5)
    st.subheader("🔍 Results")
    for mem in results:
        st.write("•", mem)

st.divider()

st.subheader("📚 All Stored Memories")
memories = get_all_memories()

if not memories:
    st.info("No memories stored yet.")
else:
    for m in memories:
        st.write("•", m)

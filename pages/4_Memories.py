import streamlit as st
from memory_store import get_all_memories

st.title("🧠 Long Term Memories")

memories = get_all_memories()

if memories:
    for idx, mem in enumerate(memories):
        st.write(f"**{idx+1}.** {mem}")
else:
    st.info("No memories stored yet.")

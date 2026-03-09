"""Streamlit UI for the Resume RAG Chatbot.

Run with:
    streamlit run week-1/day-5/app.py
"""

from chatbot import ResumeRAGChatbot
import streamlit as st
import sys
import os

# Ensure day-5 is on the path so settings.py resolves correctly
sys.path.insert(0, os.path.dirname(__file__))


st.set_page_config(page_title="Resume RAG Chat", page_icon="💬")
st.title("Resume RAG Chatbot")
st.caption("Ask anything about Noor Ul Amin's profile/resume.")


@st.cache_resource(show_spinner="Loading RAG pipeline…")
def load_chatbot() -> ResumeRAGChatbot:
    return ResumeRAGChatbot()


chatbot = load_chatbot()

# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chatbot.print_retrieved_chunks(prompt)
        answer = st.write_stream(chatbot.stream(prompt))

    st.session_state.messages.append({"role": "assistant", "content": answer})

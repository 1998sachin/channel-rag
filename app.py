from utils.genai import chat_stream
import streamlit as st
import os
from main import get_enhanced_prompt

# Page config and styling
st.set_page_config(
    page_title="X Wisdom",
    page_icon="X",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .main {
        background-color: #1e1e1e;
        padding: 2rem;
        border-radius: 10px;
        color: #ffffff;
    }
    h1 {
        color: #1DA1F2;
        text-align: center;
        font-size: 3rem !important;
        margin-bottom: 2rem !important;
    }
    .stChatMessage {
        background-color: #2d2d2d;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        color: #ffffff;
    }
    p {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title with emoji
st.title("X Wisdom 🧠")

# Subtitle
st.markdown("""
    <p style='text-align: center; color: #cccccc; font-size: 1.2rem; margin-bottom: 2rem;'>
        Discover collective wisdom from my bookmarked Twitter conversations
    </p>
""", unsafe_allow_html=True)

# Initialize messages with system prompt as user message if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "model", 
        "content": "You are a helpful AI assistant. You provide accurate, informative responses while being friendly and conversational."
    }]

# Only display user prompts and assistant responses
for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask anything about life, work, or personal growth..."):
    # Add and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get enhanced prompt but don't display it
    enhanced_prompt = get_enhanced_prompt(prompt, top_k=5)
    messages_with_context = st.session_state.messages.copy()
    messages_with_context.append({"role": "user", "content": enhanced_prompt})

    with st.chat_message("assistant"):
        # Add a spinner while generating response
        with st.spinner("Gathering wisdom from Twitter..."):
            stream = chat_stream(messages_with_context)
            response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

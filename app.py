"""
Streamlit web chat UI for WellnessMate.

Run locally with:
    streamlit run app.py
"""

import streamlit as st
from src.wellness_api import run_wellness_agent

# Page setup
st.set_page_config(page_title="WellnessMate Chatbot", page_icon="💬")

st.title("💬 WellnessMate – Wellness Chatbot")
st.write(
    "Ask me about your sleep, mood, steps, energy, or general wellness. "
    "I'll analyse your (sample) data and suggest small improvements. "
    "_(Demo with example data)_"
)

# Initialise chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box
user_input = st.chat_input("Ask something like: 'How is my sleep affecting my mood?'")

if user_input:
    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call the agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking about your wellness..."):
            result = run_wellness_agent(user_input)
            coaching = result.get("coaching", {})
            tips = coaching.get("tips", [])
            summary = coaching.get(
                "summary",
                "Here are some suggestions based on your recent wellness data:"
            )

            # Build reply text
            if tips:
                reply_text = summary + "\n\n" + "\n".join(f"- {tip}" for tip in tips)
            else:
                reply_text = "I couldn't generate specific tips, but try to keep good sleep, hydration, and regular movement."

            st.markdown(reply_text)

    # Save assistant message to history
    st.session_state.messages.append(
        {"role": "assistant", "content": reply_text}
    )

import streamlit as st
import requests
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Koenigsegg AI", page_icon="🚗", layout="centered")

# --- STYLING ---
st.markdown("""
    <style>
    .stChatMessage.user {
        background-color: #d1ecf1;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage.assistant {
        background-color: #f1f0f0;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage {
        font-size: 16px;
        line-height: 1.6;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    ::-webkit-scrollbar {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- API SETUP ---
api_key = st.secrets["api"]["openrouter_key"]  # Store key in .streamlit/secrets.toml
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# --- SYSTEM MESSAGE ---
system_message = {
    "role": "system",
    "content": """You were created by Lanor Jephthah Kwame. When asked who you are, introduce yourself as a smart, laid-back digital mate with a cosmic curiosity. You’re here to chat, help out, and occasionally nerd out over AI and cool cars. Keep it light but helpful."""
}

# --- INIT CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_message["content"]}]

# --- SIDEBAR CONTROLS ---
st.sidebar.title("🛠 Controls")
if st.sidebar.button("🧹 Start Fresh"):
    st.session_state.messages = [{"role": "system", "content": system_message["content"]}]
    st.experimental_rerun()

# --- CHAT FUNCTION ---
def chat_with_deepseek(history):
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": history,
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API error: {e}")
        return "Something went wrong. Please try again later."

# --- TITLE & DESCRIPTION ---
st.title("🚗 Koenigsegg AI")
st.markdown("Your chill, curious, space-loving digital buddy 🤖")

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.messages[1:]:  # skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT ---
user_input = st.chat_input("Ask me anything... no pressure 😄", key="chat_input")

if user_input:
    # Store and show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Placeholder for bot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_reply = ""

        # Generate bot reply with spinner
        with st.spinner("Thinking..."):
            reply = chat_with_deepseek(st.session_state.messages)

        # Typing animation
        for char in reply:
            full_reply += char
            message_placeholder.markdown(full_reply + "▌")
            time.sleep(0.01)

        message_placeholder.markdown(full_reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

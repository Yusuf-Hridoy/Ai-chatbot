import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage


# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chatbot")
st.caption("Active Mode / Fun Mode Chat Assistant")

# -----------------------
# Initialize Model
# -----------------------
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")


# -----------------------
# Session State Setup
# -----------------------
if "mode_selected" not in st.session_state:
    st.session_state.mode_selected = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -----------------------
# Mode Selection UI
# -----------------------
if not st.session_state.mode_selected:

    st.subheader("Choose Chat Mode")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⚡ Active Mode", use_container_width=True):
            mode = "active"
            st.session_state.messages = [
                SystemMessage(content=mode)
            ]
            st.session_state.mode_selected = True
            st.rerun()

    with col2:
        if st.button("😄 Fun Mode", use_container_width=True):
            mode = "fun"
            st.session_state.messages = [
                SystemMessage(content=mode)
            ]
            st.session_state.mode_selected = True
            st.rerun()

    st.stop()


# -----------------------
# Chat Display
# -----------------------
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])


# -----------------------
# Chat Input
# -----------------------
prompt = st.chat_input("Type your message... (type 0 to stop)")

if prompt:

    # Stop condition
    if prompt == "0":
        st.info("Chat stopped.")
        st.stop()

    # User message
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.session_state.chat_history.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Model response
    response = model.invoke(st.session_state.messages)

    # Save AI response
    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    st.session_state.chat_history.append(
        {"role": "assistant", "content": response.content}
    )

    with st.chat_message("assistant"):
        st.markdown(response.content)
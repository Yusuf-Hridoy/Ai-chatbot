from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Funny AI",
    page_icon="🤡",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Syne', sans-serif;
    }

    /* ---------- page background ---------- */
    .stApp {
        background: #0d0d0d;
        background-image:
            radial-gradient(ellipse 80% 60% at 50% -10%, #1a1a2e 0%, transparent 70%),
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 39px,
                rgba(255,255,255,.03) 39px,
                rgba(255,255,255,.03) 40px
            ),
            repeating-linear-gradient(
                90deg,
                transparent,
                transparent 39px,
                rgba(255,255,255,.03) 39px,
                rgba(255,255,255,.03) 40px
            );
    }

    /* ---------- header ---------- */
    .chat-header {
        text-align: center;
        padding: 2.4rem 0 1.6rem;
    }
    .chat-header h1 {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #ffffff;
        margin: 0;
        line-height: 1.1;
    }
    .chat-header h1 span {
        color: #ff4e50;
    }
    .chat-header p {
        font-family: 'DM Mono', monospace;
        font-size: 0.78rem;
        color: #555;
        margin-top: 0.4rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ---------- chat bubble wrapper ---------- */
    .chat-wrapper {
        max-width: 720px;
        margin: 0 auto;
        padding: 0 1rem 6rem;
    }

    /* ---------- individual bubbles ---------- */
    .bubble-row {
        display: flex;
        margin-bottom: 1.1rem;
        gap: 0.75rem;
        align-items: flex-end;
    }
    .bubble-row.user  { flex-direction: row-reverse; }
    .bubble-row.bot   { flex-direction: row; }

    .avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }
    .avatar.user { background: #ff4e50; }
    .avatar.bot  { background: #1e1e2e; border: 1px solid #333; }

    .bubble {
        max-width: 74%;
        padding: 0.75rem 1.1rem;
        border-radius: 18px;
        font-size: 0.95rem;
        line-height: 1.55;
        word-break: break-word;
    }
    .bubble.user {
        background: #ff4e50;
        color: #fff;
        border-bottom-right-radius: 4px;
    }
    .bubble.bot {
        background: #1a1a2e;
        color: #e0e0e0;
        border: 1px solid #2a2a4a;
        border-bottom-left-radius: 4px;
        font-family: 'DM Mono', monospace;
        font-size: 0.88rem;
    }

    /* ---------- empty state ---------- */
    .empty-state {
        text-align: center;
        padding: 5rem 1rem 3rem;
        color: #333;
    }
    .empty-state .icon { font-size: 3.5rem; margin-bottom: 1rem; }
    .empty-state p {
        font-family: 'DM Mono', monospace;
        font-size: 0.82rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    /* ---------- input area ---------- */
    .stChatInputContainer, [data-testid="stChatInput"] {
        background: #111 !important;
        border-top: 1px solid #222 !important;
    }
    [data-testid="stChatInput"] textarea {
        background: #1a1a1a !important;
        color: #eee !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.9rem !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 12px !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #ff4e50 !important;
        box-shadow: 0 0 0 2px rgba(255,78,80,.15) !important;
    }

    /* hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="chat-header">
        <h1>Funny<span>AI</span> 🤡</h1>
        <p>powered by gemini · always joking</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a funny assistant.")
    ]

# ── Model (cached so it isn't re-created on every rerun) ─────────────────────
@st.cache_resource
def get_model():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

model = get_model()

# ── Render chat history ───────────────────────────────────────────────────────
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

display_messages = [m for m in st.session_state.messages if not isinstance(m, SystemMessage)]

if not display_messages:
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">💬</div>
            <p>say something · i dare you</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    for msg in display_messages:
        if isinstance(msg, HumanMessage):
            st.markdown(
                f"""
                <div class="bubble-row user">
                    <div class="avatar user">🙂</div>
                    <div class="bubble user">{msg.content}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif isinstance(msg, AIMessage):
            st.markdown(
                f"""
                <div class="bubble-row bot">
                    <div class="avatar bot">🤡</div>
                    <div class="bubble bot">{msg.content}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Type a message…"):
    st.session_state.messages.append(HumanMessage(content=prompt))

    with st.spinner(""):
        response = model.invoke(st.session_state.messages)

    st.session_state.messages.append(AIMessage(content=response.content))
    st.rerun()
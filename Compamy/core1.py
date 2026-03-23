from dotenv import load_dotenv, parser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()


from langchain_google_genai import ChatGoogleGenerativeAI

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Movie Info Extractor",
    page_icon="🎬",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d0d;
    color: #f0ece4;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
}

/* Main container */
.block-container {
    max-width: 780px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Header */
.header-area {
    text-align: center;
    margin-bottom: 2.5rem;
}
.header-area h1 {
    font-size: 2.8rem;
    letter-spacing: -0.5px;
    color: #f5c842;
    margin-bottom: 0.3rem;
}
.header-area p {
    color: #a09880;
    font-size: 1rem;
}

/* Textarea */
textarea {
    background-color: #1a1a1a !important;
    color: #f0ece4 !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    resize: vertical !important;
}
textarea:focus {
    border-color: #f5c842 !important;
    box-shadow: 0 0 0 2px rgba(245,200,66,0.15) !important;
}

/* Button */
.stButton > button {
    background-color: #f5c842;
    color: #0d0d0d;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.6rem 2.2rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.1s ease;
    width: 100%;
}
.stButton > button:hover {
    background-color: #e6b800;
    transform: translateY(-1px);
}

/* Result box */
.result-box {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-left: 4px solid #f5c842;
    border-radius: 10px;
    padding: 1.8rem 2rem;
    margin-top: 2rem;
    line-height: 1.8;
    font-size: 0.95rem;
    white-space: pre-wrap;
    color: #e8e2d8;
}

/* Divider */
hr {
    border-color: #222;
    margin: 2rem 0;
}

/* Label */
.stTextArea label {
    color: #a09880 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #f5c842 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-area">
    <h1>🎬 Movie Info Extractor</h1>
    <p>Paste any movie description and get a clean, structured breakdown instantly.</p>
</div>
""", unsafe_allow_html=True)

# ── Model + Prompt (cached) ───────────────────────────────────────────────────
@st.cache_resource
def load_model_and_prompt():
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert information extraction assistant.

Your task is to read the provided paragraph and extract the most useful information about the movie in a clear, well-organized format.

RULES:

* Use only information found in the text.
* Do NOT invent or assume missing details.
* If something is not mentioned, write "Not specified".
* Keep answers concise and factual.
* Write in clean, readable sections.

Extract and present the information using the following format:

Movie Title:
Release Year:
Director:
Country:
Genre:

Main Characters:
(List important characters mentioned)

Cast:
(Actors only if mentioned)

Core Plot:
(Explain the main storyline in 2–3 sentences)

Themes & Social Messages:
(List key themes or ideas explored)

Based on Real Events:
(Yes / No / Not specified)

Awards & Achievements:
(Major awards or recognitions)

Cultural or Commercial Impact:
(Performance, popularity, or significance)

Unique Elements:
(Notable concepts, techniques, or standout ideas)

Quick Summary:
(A short 1–2 sentence summary)

Now extract the information.
"""),
        ("human", "Here is the paragraph:\n{paragraph}")
    ])
    return model, prompt

model, PromptTemplate = load_model_and_prompt()

# ── Input ─────────────────────────────────────────────────────────────────────
para = st.text_area(
    "Your Paragraph",
    placeholder="Paste a movie description, synopsis, or any paragraph about a film here...",
    height=200
)

# ── Extract Button ────────────────────────────────────────────────────────────
if st.button("Extract Movie Info"):
    if not para.strip():
        st.warning("Please enter a paragraph before extracting.")
    else:
        with st.spinner("Extracting movie information..."):
            final_prompt = PromptTemplate.invoke({"paragraph": para})
            response = model.invoke(final_prompt)

        st.markdown("---")
        st.markdown(f'<div class="result-box">{response.content}</div>', unsafe_allow_html=True)
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class MovieInfo(BaseModel):
    title: Optional[str] = None
    release_year: Optional[str] = None
    director: Optional[str] = None
    country: Optional[str] = None
    genre: Optional[str] = None
    main_characters: Optional[List[str]] = None
    cast: Optional[List[str]] = None
    core_plot: Optional[str] = None
    unique_elements: Optional[str] = None
    quick_summary: Optional[str] = None

parser = PydanticOutputParser(pydantic_object=MovieInfo)

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

.block-container {
    max-width: 780px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

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

.result-box {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-left: 4px solid #f5c842;
    border-radius: 10px;
    padding: 1.8rem 2rem;
    margin-top: 0.5rem;
    margin-bottom: 1.2rem;
    line-height: 1.8;
    font-size: 0.95rem;
    white-space: pre-wrap;
    color: #e8e2d8;
}

.info-card {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
}
.info-card .label {
    color: #a09880;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
}
.info-card .value {
    color: #f0ece4;
    font-size: 1rem;
    font-weight: 500;
}

hr {
    border-color: #222;
    margin: 2rem 0;
}

.stTextArea label {
    color: #a09880 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.stSpinner > div {
    border-top-color: #f5c842 !important;
}

.section-label {
    color: #a09880;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
    margin-top: 1.2rem;
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
        ('system', """
         Extract movie information from the paragraph.
         {format_instructions}
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
            final_prompt = PromptTemplate.invoke({
                "paragraph": para,
                "format_instructions": parser.get_format_instructions()
            })
            response = model.invoke(final_prompt)

        try:
            movie = parser.parse(response.content)
        except Exception as e:
            st.error(f"Could not parse response: {e}")
            st.stop()

        st.markdown("---")

        # ── Row 1: Title / Year / Director ───────────────────────────────────
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="info-card">
                <div class="label">🎬 Title</div>
                <div class="value">{movie.title or '—'}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="info-card">
                <div class="label">📅 Year</div>
                <div class="value">{movie.release_year or '—'}</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="info-card">
                <div class="label">🎥 Director</div>
                <div class="value">{movie.director or '—'}</div>
            </div>""", unsafe_allow_html=True)

        # ── Row 2: Genre / Country ────────────────────────────────────────────
        c4, c5 = st.columns(2)
        with c4:
            st.markdown(f"""
            <div class="info-card">
                <div class="label">🎭 Genre</div>
                <div class="value">{movie.genre or '—'}</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""
            <div class="info-card">
                <div class="label">🌍 Country</div>
                <div class="value">{movie.country or '—'}</div>
            </div>""", unsafe_allow_html=True)

        # ── Characters & Cast ─────────────────────────────────────────────────
        if movie.main_characters:
            st.markdown(f"""
            <div class="info-card">
                <div class="label">👥 Main Characters</div>
                <div class="value">{', '.join(movie.main_characters)}</div>
            </div>""", unsafe_allow_html=True)

        if movie.cast:
            st.markdown(f"""
            <div class="info-card">
                <div class="label">🌟 Cast</div>
                <div class="value">{', '.join(movie.cast)}</div>
            </div>""", unsafe_allow_html=True)

        # ── Core Plot ─────────────────────────────────────────────────────────
        if movie.core_plot:
            st.markdown('<div class="section-label">📖 Core Plot</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">{movie.core_plot}</div>', unsafe_allow_html=True)

        # ── Unique Elements ───────────────────────────────────────────────────
        if movie.unique_elements:
            st.markdown('<div class="section-label">✨ Unique Elements</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">{movie.unique_elements}</div>', unsafe_allow_html=True)

        # ── Quick Summary ─────────────────────────────────────────────────────
        if movie.quick_summary:
            st.markdown('<div class="section-label">💡 Quick Summary</div>', unsafe_allow_html=True)
            st.info(movie.quick_summary)
# Gene AI

A Generative AI toolkit powered by Google Gemini and LangChain, featuring chatbots, movie information extraction, and text embeddings.

## Features

### 🤖 Chat Applications
- **Interactive Chatbot** - Console-based chatbot with Active and Fun modes
- **Streamlit Chat UI** - Web-based chat interface with mode selection
- **Styled Chat App** - Custom dark-themed chat experience

### 🎬 Movie Information Extraction
- **CLI Extractor** - Command-line movie info extraction
- **Streamlit Movie Tool** - Web UI with structured card layouts
- Extracts: title, year, director, genre, cast, plot, and more

### 🔢 Text Embeddings
- HuggingFace sentence-transformers integration
- Generate embeddings using `all-MiniLM-L6-v2` model

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.12+ | Language |
| LangChain | LLM application framework |
| Google Gemini | Primary AI model |
| Streamlit | Web UI framework |
| sentence-transformers | Text embeddings |

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd gene-ai
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Add your Google API key to .env:
# GOOGLE_API_KEY=your_api_key_here
```

## Usage

### Chat Applications

**Run the Streamlit Chat UI:**
```bash
streamlit run chatmodel/UiChat.py
```

**Run the Styled Chat App:**
```bash
streamlit run chatmodel/demo.py
```

**Run Console Chatbot:**
```bash
python chatmodel/Chatbot.py
```

### Movie Information Extraction

**Run Streamlit Movie Extractor:**
```bash
streamlit run Compamy/core1.py
```

**Run Enhanced Movie Extractor (Cards):**
```bash
streamlit run Compamy/output.py
```

**Run CLI Movie Extractor:**
```bash
python Compamy/core.py
```

### Text Embeddings

**Generate Embeddings:**
```bash
python embadeModel/embedding.py
```

## Project Structure

```
gene-ai/
├── chatmodel/           # Chat applications
│   ├── Chat.py         # Basic API test
│   ├── Chatbot.py      # Console chatbot
│   ├── UiChat.py       # Streamlit chat UI
│   └── demo.py         # Styled chat app
├── Compamy/            # Movie extraction tools
│   ├── core.py         # CLI extractor
│   ├── core1.py        # Streamlit extractor
│   └── output.py       # Card-based extractor
├── embadeModel/        # Embedding utilities
│   └── embedding.py    # HuggingFace embeddings
├── main.py             # Entry point
├── requirements.txt    # Dependencies
└── pyproject.toml      # Project metadata
```

## API Setup

This project requires a Google Gemini API key:

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Add it to your `.env` file as `GOOGLE_API_KEY`
3. Ensure `.env` is in your `.gitignore`



# AI College FAQ Chatbot 🎓

A professional RAG (Retrieval-Augmented Generation) chatbot designed to answer college-related FAQs using Llama-3.1 and ChromaDB.

## 🚀 Live Deployment
The app is optimized for **Streamlit Cloud**. 
- **Knowledge Base**: 50+ FAQ entries indexed in an in-memory ChromaDB.
- **Auto-Update**: The vector index is built automatically from `data/faqs.csv` on launch.

## ✨ Features
- **Premium UI**: Glassmorphic Streamlit interface with 3D-style interactions and dark mode optimization.
- **RAG Architecture**: Semantic search via ChromaDB and `all-MiniLM-L6-v2` embeddings.
- **Intent Classification**: Specialized logic to handle ambiguous vs. direct college queries.
- **Sentiment Analytics**: Built-in VADER analysis for tracking user feedback.

## 🛠️ Tech Stack
- **LLM**: Meta-Llama-3.1-8B-Instruct (via Hugging Face)
- **Vector DB**: ChromaDB (In-Memory)
- **Frontend**: Streamlit (with custom CSS/Glassmorphism)
- **Analytics**: VADER Sentiment Analysis

## 📦 Local Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Secrets**:
   Create a `.streamlit/secrets.toml` file or a `.env` file:
   ```toml
   HUGGINGFACE_API_TOKEN = "your_hf_token_here"
   ```

3. **Launch**:
   ```bash
   streamlit run app/main.py
   ```

## ☁️ Deployment (Streamlit Cloud)
1. Fork/Push this repo to GitHub.
2. Connect to [Streamlit Cloud](https://share.streamlit.io/).
3. Set Main File Path: `app/main.py`.
4. Add `HUGGINGFACE_API_TOKEN` to **Settings > Secrets**.

## 🎓 Capstone Coverage
- [x] **50+ Q&A Pairs**: implemented in `data/faqs.csv`.
- [x] **Knowledge Map**: Documented in [ARCHITECTURE.md](./ARCHITECTURE.md).
- [x] **Logical Routing**: Intent-based routing logic in `core/intent.py`.
- [x] **Agentic Loop**: Perception (Input) -> Reasoning (Intent/RAG) -> Action (Response).

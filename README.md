# AI College FAQ Chatbot 🎓

A full-stack RAG (Retrieval-Augmented Generation) chatbot designed to answer college-related FAQs using Llama-3.1-8B and ChromaDB.

## Features
- **Premium UI**: Glassmorphic Streamlit interface with 3D-style interactions.
- **RAG Architecture**: Uses ChromaDB for vector retrieval and Sentence-Transformers for embeddings.
- **Intent Classification**: Automatically detects if a query is about admissions, fees, hostel, etc.
- **Admin Panel**: Update FAQs and re-build the knowledge base on the fly.
- **Feedback Dashboard**: Analyze user satisfaction with VADER sentiment analysis.
- **Architecture Documentation**: Detailed knowledge mapping and agent definitions in [ARCHITECTURE.md](./ARCHITECTURE.md).

## 🎓 Capstone Requirements Coverage
- [x] **50+ Q&A Pairs**: implemented in `data/faqs.csv`.
- [x] **Knowledge Map**: Visualized and documented in `ARCHITECTURE.md`.
- [x] **Prompt Design**: Specialized intents and RAG prompts in `core/`.
- [x] **AI Agent Definition**: Perception-Action loop implemented in `app/main.py`.
- [x] **Logical Routing**: Intent-based routing logic in `core/intent.py`.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file in the root directory (refer to `.env.example`):
   ```env
   HUGGINGFACE_API_TOKEN=your_huggingface_token_here
   ```

3. **Build Knowledge Base**:
   Run the indexing script to embed the initial FAQ data in `data/faqs.csv`:
   ```bash
   python scripts/build_index.py
   ```

4. **Launch Application**:
   Start the Streamlit app:
   ```bash
   streamlit run app/main.py
   ```

## Admin Access
- **URL**: Go to the "Admin Panel" in the sidebar.
- **Password**: `admin123`

## Tech Stack
- **LLM**: meta-llama/Llama-3.1-8B-Instruct (HF API)
- **Vector DB**: ChromaDB
- **Frontend**: Streamlit
- **Sentiment**: VADER

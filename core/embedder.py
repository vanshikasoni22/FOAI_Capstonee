import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import os
import streamlit as st

# Use a cached in-memory ChromaDB — cloud-safe, no persistent disk needed
@st.cache_resource(show_spinner="Building knowledge base...")
def get_collection():
    """Build the in-memory ChromaDB index from faqs.csv. Cached for the app session."""
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    csv_path = os.path.join(os.path.dirname(__file__), "../data/faqs.csv")
    df = pd.read_csv(csv_path)
    df['text'] = df['question'] + " " + df['answer']

    # In-memory client — works on any cloud host
    client = chromadb.Client()

    try:
        client.delete_collection(name="college_faqs")
    except Exception:
        pass

    collection = client.create_collection(name="college_faqs")

    documents = df['text'].tolist()
    metadatas = df[['topic', 'question', 'answer']].to_dict('records')
    ids = [str(i) for i in range(len(df))]

    print(f"Embedding {len(documents)} documents...")
    embeddings = model.encode(documents).tolist()

    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("In-memory vector database build complete.")
    return collection


def build_index():
    """Legacy entry point for build_index script — kept for compatibility."""
    get_collection()

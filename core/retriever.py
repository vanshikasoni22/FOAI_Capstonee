from sentence_transformers import SentenceTransformer
import streamlit as st

@st.cache_resource(show_spinner=False)
def _get_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def retrieve(query, collection):
    """Retrieve relevant FAQ chunks from the in-memory ChromaDB collection."""
    model = _get_model()
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    formatted_results = []
    if results['ids'][0]:
        for i in range(len(results['ids'][0])):
            distance = results['distances'][0][i]
            print(f"Match {i+1} Distance: {distance:.4f} - {results['metadatas'][0][i]['question']}")

            if i == 0 and distance > 0.8:
                return "no_match"

            formatted_results.append({
                "topic": results['metadatas'][0][i]['topic'],
                "question": results['metadatas'][0][i]['question'],
                "answer": results['metadatas'][0][i]['answer'],
                "distance": distance
            })

    return formatted_results if formatted_results else "no_match"

import chromadb
from sentence_transformers import SentenceTransformer
import os

# Initialize ChromaDB client
DB_PATH = os.path.join(os.path.dirname(__file__), "../chroma_db")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve(query):
    collection = chroma_client.get_collection(name="college_faqs")
    
    # Embed query
    query_embedding = model.encode(query).tolist()
    
    # Query ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    
    # Format results
    formatted_results = []
    if results['ids'][0]:
        for i in range(len(results['ids'][0])):
            distance = results['distances'][0][i]
            # ChromaDB cosine distance (0 is perfect match, 2 is opposite)
            # If distance > 0.8, it's a weak match
            if i == 0 and distance > 0.8:
                return "no_match"
            
            formatted_results.append({
                "topic": results['metadatas'][0][i]['topic'],
                "question": results['metadatas'][0][i]['question'],
                "answer": results['metadatas'][0][i]['answer'],
                "distance": distance
            })
            
    return formatted_results if formatted_results else "no_match"

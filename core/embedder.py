import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import os

# Initialize ChromaDB client (local persistent)
DB_PATH = os.path.join(os.path.dirname(__file__), "../chroma_db")
chroma_client = chromadb.PersistentClient(path=DB_PATH)

def build_index():
    # Load model
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Load data
    csv_path = os.path.join(os.path.dirname(__file__), "../data/faqs.csv")
    df = pd.read_csv(csv_path)
    
    # Combine question and answer for embedding
    df['text'] = df['question'] + " " + df['answer']
    
    # Get or create collection
    try:
        chroma_client.delete_collection(name="college_faqs")
        print("Deleted existing collection 'college_faqs' for a fresh build.")
    except Exception:
        pass
        
    collection = chroma_client.create_collection(name="college_faqs")
    
    # Prepare data for ChromaDB
    documents = df['text'].tolist()
    metadatas = df[['topic', 'question', 'answer']].to_dict('records')
    ids = [str(i) for i in range(len(df))]
    
    print(f"Embedding {len(documents)} documents...")
    embeddings = model.encode(documents).tolist()
    
    # Add to collection
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("Vector database build complete.")

if __name__ == "__main__":
    build_index()

import sys
import os

# Add project root to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core.embedder import build_index

if __name__ == "__main__":
    print("-" * 30)
    print("AI COLLEGE FAQ CHATBOT")
    print("Building Vector Knowledge Base...")
    print("-" * 30)
    
    try:
        build_index()
        print("\nSuccess: ChromaDB index built and saved in chroma_db/")
    except Exception as e:
        print(f"\nError building index: {e}")
    
    print("-" * 30)

import sys
import os

# Add project root to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core.retriever import retrieve

queries = [
    "What are hostel timings?",
    "How can I apply for admission?",
    "Tell me about fees",
    "When is the next cultural fest?",
    "What is the HOD email?"
]

print("-" * 30)
print("TESTING RETRIEVER")
print("-" * 30)

for q in queries:
    print(f"\nQuery: {q}")
    results = retrieve(q)
    if results == "no_match":
        print("Result: No direct match found.")
    else:
        print(f"Top Match Topic: {results[0]['topic']}")
        print(f"Top Match Question: {results[0]['question']}")
        print(f"Distance: {results[0]['distance']:.4f}")

print("\n" + "-" * 30)

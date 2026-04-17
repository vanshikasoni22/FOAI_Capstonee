import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.retriever import retrieve

def test_query(prompt):
    print(f"\nQuery: {prompt}")
    results = retrieve(prompt)
    if results == "no_match":
        print("Result: NO MATCH")
    else:
        for idx, res in enumerate(results):
            print(f"Match {idx+1}:")
            print(f"  Topic: {res['topic']}")
            print(f"  Question: {res['question']}")
            print(f"  Distance: {res['distance']:.4f}")
            print(f"  Answer: {res['answer'][:100]}...")

if __name__ == "__main__":
    test_query("what are the main gate timings?")
    test_query("how many books can i borrow?")
    test_query("where is the health center?")
    test_query("is there a night canteen?")
    test_query("when is the fee deadline?")

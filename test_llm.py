from core.llm import generate_response

print("Testing generate_response...")
response = generate_response("You are a helpful assistant.", "What is the capital of France?")
print(f"Response: {response}")

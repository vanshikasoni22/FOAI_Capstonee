import requests
import os

token = os.getenv("HUGGINGFACE_API_TOKEN", "") # Use empty or the one in env if any
# Let's see what happens without a token, we might get 401 instead of 404, which proves the URL is correct

urls = [
    "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
    "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta/v1/chat/completions"
]

for url in urls:
    print(f"Testing {url}")
    try:
        response = requests.post(url, headers={"Authorization": f"Bearer {token}"}, json={"inputs": "Hello"})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 30)

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_response(system_prompt, user_message, conversation_history=[]):
    if not HF_TOKEN:
        return "Error: HuggingFace API Token not found in .env"

    # Build messages array (system + last 3 turns + current message)
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add history (last 3 turns = 6 messages if each turn has user/assistant)
    history_to_include = conversation_history[-6:]
    messages.extend(history_to_include)
    
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": messages,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "return_full_text": False
        }
    }

    # Retry logic (3 attempts)
    for attempt in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            # The structure for Chat Completion API usually returns text in 'choices' or directly
            if isinstance(result, list):
                return result[0].get('generated_text', '').strip()
            return result.get('choices', [{}])[0].get('message', {}).get('content', '').strip() or result.get('generated_text', '').strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
            return f"Error connecting to LLM: {str(e)}"
    
    return "Service temporarily unavailable."

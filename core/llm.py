import os
import time
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
# Corrected model repository name
MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"

def generate_response(system_prompt, user_message, conversation_history=[]):
    if not HF_TOKEN or HF_TOKEN == "your_huggingface_token_here":
        return "Error: Please add a valid HuggingFace API Token in your .env file."

    client = InferenceClient(token=HF_TOKEN)

    # Build messages array (system + last 3 turns + current message)
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add history (last 3 turns = 6 messages if each turn has user/assistant)
    history_to_include = conversation_history[-6:]
    messages.extend(history_to_include)
    
    messages.append({"role": "user", "content": user_message})

    # Retry logic (3 attempts)
    for attempt in range(3):
        try:
            response = client.chat_completion(
                model=MODEL_ID,
                messages=messages,
                max_tokens=512,
                temperature=0.7,
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
            
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                return f"Error: Model {MODEL_ID} not found or you don't have access. Please ensure you have accepted the Llama 3.1 license on Hugging Face."
            elif "401" in error_msg or "403" in error_msg:
                return "Error: Invalid Hugging Face token or missing permissions."
            
            return f"Error connecting to LLM: {error_msg}"
    
    return "Service temporarily unavailable."

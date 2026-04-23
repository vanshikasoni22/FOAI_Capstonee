import os
import time

# Try to import streamlit secrets — gracefully fallback if not in a streamlit context
try:
    import streamlit as st
    def _get_token():
        try:
            return st.secrets.get("HUGGINGFACE_API_TOKEN", os.getenv("HUGGINGFACE_API_TOKEN"))
        except Exception:
            return os.getenv("HUGGINGFACE_API_TOKEN")
except ImportError:
    def _get_token():
        return os.getenv("HUGGINGFACE_API_TOKEN")

from dotenv import load_dotenv
load_dotenv()

from huggingface_hub import InferenceClient

MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"

def generate_response(system_prompt, user_message, conversation_history=[]):
    HF_TOKEN = _get_token()

    if not HF_TOKEN or HF_TOKEN == "your_huggingface_token_here":
        return "Error: Please add a valid HuggingFace API Token in Streamlit secrets or your .env file."

    client = InferenceClient(token=HF_TOKEN)

    # Build messages: system + last 3 turns of history + current user message
    messages = [{"role": "system", "content": system_prompt}]
    history_to_include = conversation_history[-6:]
    messages.extend(history_to_include)
    messages.append({"role": "user", "content": user_message})

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
                return (
                    f"Error: Model not found or access denied. "
                    f"Please ensure you have accepted the Llama 3.1 license at "
                    f"https://huggingface.co/{MODEL_ID}"
                )
            elif "401" in error_msg or "403" in error_msg:
                return "Error: Invalid or missing Hugging Face token."

            return f"Error connecting to LLM: {error_msg}"

    return "Service temporarily unavailable. Please try again."

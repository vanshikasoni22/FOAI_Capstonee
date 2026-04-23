import streamlit as st
import pandas as pd
import os
import sys

# Add project root to sys.path to resolve 'core' module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.embedder import get_collection
from core.retriever import retrieve
from core.llm import generate_response
from core.intent import classify_intent
from core.logger import log_unanswered, log_feedback
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

# Page config
st.set_page_config(page_title="College AI FAQ Chatbot", layout="wide")

# Custom CSS for Glassmorphism and "3D" elements
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif;
        background: radial-gradient(circle at top left, #1e293b, #0f172a);
        color: #f8fafc;
    }

    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stChatMessage:hover {
        transform: translateZ(20px) scale(1.02);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Unique bubble styling for Bot and User */
    [data-testid="stChatMessageAssistant"] {
        background: rgba(30, 41, 59, 0.7) !important;
        border-right: 4px solid #38bdf8;
    }
    
    [data-testid="stChatMessageUser"] {
        background: rgba(56, 189, 248, 0.1) !important;
        border-left: 4px solid #38bdf8;
    }

    .sidebar-logo {
        background: linear-gradient(135deg, #38bdf8, #818cf8);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
    }

    .stButton>button {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.3s;
        color: white;
    }
    
    .stButton>button:hover {
        background: #38bdf8;
        transform: translateY(-2px);
    }
    
    /* Feedback Buttons */
    .feedback-btn {
        cursor: pointer;
        padding: 5px 10px;
        font-size: 1.2rem;
        transition: 0.2s;
    }
    .feedback-btn:hover {
        transform: scale(1.2);
    }
</style>
""", unsafe_allow_html=True)

# ─── Build the in-memory ChromaDB index (cached — runs once per session) ───
collection = get_collection()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "stats" not in st.session_state:
    st.session_state.stats = {"questions_asked": 0}

# Sidebar Content
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🎓 COLLEGE FAQ AI</div>', unsafe_allow_html=True)
    
    topic_filter = st.selectbox(
        "Explore by Topic",
        ["All", "Hostel", "Academics", "Library", "Dining", "IT Support", "Medical", "Finance", "Campus Life", "Placements", "General"]
    )
    
    if st.button("Clear Chat 🗑️"):
        st.session_state.messages = []
        st.session_state.stats = {"questions_asked": 0}
        st.rerun()

    st.divider()
    st.markdown(f"### Session Stats")
    st.metric("Questions Asked", st.session_state.stats["questions_asked"])
    
    st.info("Ask anything about the college, from admissions to hostel rules!")

# Main Chat Header
st.title("AI Campus Assistant ✨")
st.caption("Powered by Llama-3.1 & ChromaDB")

# Display Chat History
for index, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Feedback logic for assistant messages
        if message["role"] == "assistant":
            col1, col2, col3 = st.columns([1, 1, 10])
            with col1:
                if st.button("👍", key=f"up_{index}"):
                    st.toast("Thanks for the feedback!", icon="✅")
            with col2:
                if st.button("👎", key=f"down_{index}"):
                    st.toast("Logged for improvement.", icon="📝")

# User Input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.stats["questions_asked"] += 1
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot Processing
    with st.chat_message("assistant"):
        with st.status("Analyzing and searching...", expanded=False) as status:
            # 1. Intent Classification
            intent = classify_intent(prompt)
            st.write(f"Intent classified: **{intent}**")
            
            # 2. Retrieval — pass in-memory collection
            retrieved_chunks = retrieve(prompt, collection)
            
            # 3. Generate response
            response = ""
            if intent == "ambiguous":
                status.update(label="Clarification needed", state="complete")
                response = generate_response(
                    "The user's query is ambiguous. Ask ONE short clarifying question to help them find the right FAQ category.",
                    prompt
                )
            else:
                status.update(label="Generating answer...", state="complete")
                context_str = ""
                if retrieved_chunks != "no_match":
                    context_str = "\n".join([f"- {c['question']}: {c['answer']}" for c in retrieved_chunks])
                else:
                    log_unanswered(prompt)
                
                system_prompt = (
                    "You are a helpful, friendly FAQ assistant for a college. "
                    "Answer the student's question using the provided context if available. "
                    "If the context does not contain the answer or is empty, use your general knowledge about colleges to provide a helpful answer. "
                    "Be concise (2-4 sentences).\n\n"
                    f"Context:\n{context_str}"
                )
                response = generate_response(system_prompt, prompt, st.session_state.messages)

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Note: Added st.rerun() to ensure feedback buttons show up immediately under the new message

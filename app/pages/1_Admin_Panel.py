import streamlit as st
import pandas as pd
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from core.embedder import build_index

# Password Protection
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    st.title("Admin Access")
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if password == "admin123":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    return False

if check_password():
    st.title("⚙️ Admin Panel")
    
    # Path to data
    faq_path = os.path.join(os.path.dirname(__file__), "../../data/faqs.csv")
    unanswered_path = os.path.join(os.path.dirname(__file__), "../../data/unanswered.csv")
    
    tab1, tab2, tab3 = st.tabs(["📚 FAQ Manager", "❓ Unanswered Queries", "🔄 System Maintenance"])
    
    with tab1:
        st.header("Manage Knowledge Base")
        df = pd.read_csv(faq_path)
        
        # Editable dataframe
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        if st.button("Save Changes"):
            edited_df.to_csv(faq_path, index=False)
            st.success("FAQs updated successfully!")
            
        st.divider()
        st.subheader("Add New FAQ")
        with st.form("add_faq"):
            topic = st.selectbox("Topic", ["admissions", "fees", "hostel", "academics", "events", "contacts"])
            question = st.text_area("Question")
            answer = st.text_area("Answer")
            if st.form_submit_button("Add to CSV"):
                new_row = pd.DataFrame([[topic, question, answer]], columns=df.columns)
                new_row.to_csv(faq_path, mode='a', header=False, index=False)
                st.success("New FAQ added!")
    
    with tab2:
        st.header("Queries with No Match")
        if os.path.exists(unanswered_path):
            un_df = pd.read_csv(unanswered_path)
            st.dataframe(un_df.sort_values(by="timestamp", ascending=False), use_container_width=True)
        else:
            st.info("No unanswered queries logged yet.")
            
    with tab3:
        st.header("Re-build Index")
        st.warning("This will re-embed all FAQs and update the vector database. This may take a minute.")
        if st.button("Start Indexing"):
            with st.spinner("Embedding..."):
                build_index()
            st.success("Vector database re-built successfully!")

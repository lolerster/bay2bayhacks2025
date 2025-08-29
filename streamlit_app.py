import streamlit as st
import requests
import json
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Bay2BayHacks2025 - AI Notes App",
    page_icon="📝",
    layout="wide"
)

# Title and description
st.title("📝 AI-Powered Notes App")
st.markdown("**Bay2BayHacks2025** - Create, manage, and get AI insights from your notes!")

# API base URL
API_BASE_URL = "http://localhost:8000"

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["📝 Add Note", "📋 View Notes", "🤖 Summarize Notes", "❓ Ask Questions"]
)

# Initialize session state
if 'notes' not in st.session_state:
    st.session_state.notes = []

# Function to make API calls
def make_api_call(endpoint, method="GET", data=None, show_response=True):
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code == 200:
            result = response.json()
            # Print the return message for debugging/information (only if show_response=True)
            if show_response:
                if isinstance(result, dict) and "message" in result:
                    st.info(f"📢 API Response: {result['message']}")
                elif isinstance(result, str):
                    st.info(f"📢 API Response: {result}")
            return result
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API. Make sure your FastAPI server is running on http://localhost:8000")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

# Page 1: Add Note
if page == "📝 Add Note":
    st.header("📝 Add a New Note")
    
    with st.form("add_note_form"):
        note_content = st.text_area(
            "Note Content:",
            placeholder="Enter your note here...",
            height=150
        )
        
        submitted = st.form_submit_button("💾 Save Note")
        
        if submitted:
            if note_content.strip():
                result = make_api_call("/add_note", method="POST", data={"content": note_content})
                if result:
                    st.balloons()
                    # Clear the form
                    st.rerun()
            else:
                st.error("❌ Note content cannot be empty!")

# Page 2: View Notes
elif page == "📋 View Notes":
    st.header("📋 Your Notes")
    
    # Refresh button
    if st.button("🔄 Refresh Notes"):
        st.rerun()
    
    # Get notes from API
    notes = make_api_call("/get_notes")
    
    if notes:
        if len(notes) == 0:
            st.info("📭 No notes found. Add some notes to get started!")
        else:
            st.success(f"📊 Found {len(notes)} notes")
            
            # Display notes in a nice format
            for i, note in enumerate(notes, 1):
                with st.expander(f"📄 Note #{note[0]} - {note[1][:50]}..."):
                    st.write(f"**ID:** {note[0]}")
                    st.write(f"**Content:** {note[1]}")
                    st.write(f"**Added:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Add delete button with confirmation
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button(f"🗑️ Delete", key=f"delete_{note[0]}"):
                            # Check if this is a confirmation click
                            if st.session_state.get(f"confirm_delete_{note[0]}", False):
                                # Actually delete the note
                                result = make_api_call(f"/delete_note/{note[0]}", method="DELETE")
                                if result:
                                    st.success(f"✅ Note #{note[0]} deleted successfully!")
                                    # Clear the confirmation flag
                                    if f"confirm_delete_{note[0]}" in st.session_state:
                                        del st.session_state[f"confirm_delete_{note[0]}"]
                                    st.rerun()
                            else:
                                # Set confirmation flag for next click
                                st.session_state[f"confirm_delete_{note[0]}"] = True
                                st.rerun()
                    
                    # Show confirmation message if needed
                    if st.session_state.get(f"confirm_delete_{note[0]}", False):
                        st.warning(f"⚠️ Click '🗑️ Delete' again to confirm deletion of Note #{note[0]}")
                        with col1:
                            if st.button(f"✅ Confirm Delete", key=f"confirm_{note[0]}"):
                                result = make_api_call(f"/delete_note/{note[0]}", method="DELETE")
                                if result:
                                    st.success(f"✅ Note #{note[0]} deleted successfully!")
                                    # Clear the confirmation flag
                                    if f"confirm_delete_{note[0]}" in st.session_state:
                                        del st.session_state[f"confirm_delete_{note[0]}"]
                                    st.rerun()

# Page 3: Summarize Notes
elif page == "🤖 Summarize Notes":
    st.header("🤖 AI Note Summarizer")
    st.markdown("Get an AI-powered summary of all your notes!")
    
    if st.button("🧠 Generate Summary"):
        with st.spinner("🤖 AI is analyzing your notes..."):
            summary = make_api_call("/summarize", method="POST", show_response=False)
            
            if summary:
                st.success("✅ Summary generated!")
                st.markdown("---")
                st.markdown("### 📋 Summary:")
                st.write(summary)
                
                # Add some styling
                st.markdown("---")
                st.info("💡 **Tip:** Add more notes to get better summaries!")

# Page 4: Ask Questions
elif page == "❓ Ask Questions":
    st.header("❓ Ask Questions About Your Notes")
    st.markdown("Ask the AI questions about your notes and get intelligent answers!")
    
    with st.form("ask_question_form"):
        question = st.text_input(
            "Your Question:",
            placeholder="e.g., What did I write about groceries?",
            help="Ask any question about your notes"
        )
        
        submitted = st.form_submit_button("🤖 Ask AI")
        
        if submitted:
            if question.strip():
                with st.spinner("🤖 AI is thinking..."):
                    result = make_api_call("/ask", method="POST", data={"query": question}, show_response=False)
                    
                    if result:
                        st.success("✅ Answer generated!")
                        st.markdown("---")
                        st.markdown("### 🤖 AI Answer:")
                        st.write(result)
                        
                        # Add some styling
                        st.markdown("---")
                        st.info("💡 **Tip:** Try asking specific questions for better answers!")
            else:
                st.error("❌ Please enter a question!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ for Bay2BayHacks2025 | Powered by FastAPI + OpenAI + Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Quick Start")
st.sidebar.markdown("1. **Add Note** - Create your first note")
st.sidebar.markdown("2. **View Notes** - See all your notes")
st.sidebar.markdown("3. **Summarize** - Get AI summary")
st.sidebar.markdown("4. **Ask Questions** - Query your notes")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ API Status")
if st.sidebar.button("🔍 Check API"):
    try:
        response = requests.get(f"{API_BASE_URL}/docs")
        if response.status_code == 200:
            st.sidebar.success("✅ API is running")
        else:
            st.sidebar.error("❌ API error")
    except:
        st.sidebar.error("❌ API not reachable")

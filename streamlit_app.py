import streamlit as st
import requests
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

# Initialize session state for editing and delete confirmations
# Note: Session state variables are created dynamically as needed

# Function to make API calls to the FastAPI backend
def make_api_call(endpoint, method="GET", data=None, show_response=True, files=None):
    try:
        url = f"{API_BASE_URL}{endpoint}"
        response = None
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files)
            else:
                response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            st.error(f"❌ Unsupported HTTP method: {method}")
            return None
        
        if response and response.status_code == 200:
            result = response.json()
            # Print the return message for debugging/information (only if show_response=True)
            if show_response:
                if isinstance(result, dict) and "message" in result:
                    st.info(f"📢 API Response: {result['message']}")
                elif isinstance(result, str):
                    st.info(f"📢 API Response: {result}")
            return result
        elif response:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
        else:
            st.error("❌ No response received from API")
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
    
    # File upload section
    st.subheader("📁 Upload File")
    
    # Text file upload
    uploaded_text_file = st.file_uploader(
        "Choose a text file to upload",
        type=['txt', 'md', 'csv', 'json'],
        help="Upload a text file to convert its content into a note",
        key="text_uploader"
    )
    
    # Audio file upload
    uploaded_audio_file = st.file_uploader(
        "Choose an audio file to upload",
        type=['wav', 'mp3', 'm4a', 'ogg'],
        help="Upload an audio file to convert speech to text",
        key="audio_uploader"
    )
    
    # Handle text file upload
    if uploaded_text_file is not None:
        try:
            # Check file size (limit to 5MB for text files)
            if uploaded_text_file.size and uploaded_text_file.size > 5 * 1024 * 1024:
                st.error("❌ File size must be less than 5MB")
            else:
                # Read file content
                try:
                    file_content = uploaded_text_file.read().decode('utf-8')
                    st.success(f"✅ Text file '{uploaded_text_file.name}' uploaded successfully!")
                    st.text_area("File Content Preview:", file_content, height=100, disabled=True)
                except UnicodeDecodeError:
                    st.error("❌ Unable to read file. Please ensure it's a valid text file with UTF-8 encoding.")
                    file_content = None
            
            # Add button to save file content as note
            if st.button("💾 Save Text File as Note", key="save_text"):
                if file_content:
                    result = make_api_call("/add_note", method="POST", data={"content": file_content})
                    if result:
                        st.balloons()
                        st.rerun()
                else:
                    st.error("❌ No valid content to save")
        except Exception as e:
            st.error(f"❌ Error reading text file: {str(e)}")
    
    # Handle audio file upload
    if uploaded_audio_file is not None:
        try:
            st.info(f"🎵 Audio file '{uploaded_audio_file.name}' uploaded!")
            st.audio(uploaded_audio_file, format='audio/wav')
            
            # Show transcribed text if it exists in session state (after page refresh)
            if "transcribed_text" in st.session_state:
                st.success("✅ Transcribed text available!")
                st.text_area("Transcribed Text:", st.session_state.transcribed_text, height=100)
                
                # Add button to save transcribed text as note
                if st.button("💾 Save Transcription as Note", key="save_audio_session"):
                    note_result = make_api_call("/add_note", method="POST", data={"content": st.session_state.transcribed_text}, show_response=True)
                    if note_result:
                        st.success("✅ Transcription saved as note!")
                        st.balloons()
                        # Clear the transcribed text from session state
                        del st.session_state.transcribed_text
                        st.rerun()
                    else:
                        st.error("❌ Failed to save transcription as note")
            
            # Add button to convert audio to text
            if st.button("🎤 Convert Audio to Text", key="convert_audio"):
                with st.spinner("🎤 Converting audio to text using OpenAI Whisper..."):
                    # Send audio file to FastAPI for transcription
                    files = {"audio_file": (uploaded_audio_file.name, uploaded_audio_file.getvalue(), uploaded_audio_file.type)}
                    result = make_api_call("/transcribe_audio", method="POST", files=files, show_response=False)
                    
                    if result and "transcription" in result:
                        transcribed_text = result["transcription"]
                        # Store in session state so it persists after page refresh
                        st.session_state.transcribed_text = transcribed_text
                        st.success("✅ Audio converted to text!")
                        st.text_area("Transcribed Text:", transcribed_text, height=100)
                        st.rerun()
                    else:
                        st.error("❌ Failed to transcribe audio file")
        except Exception as e:
            st.error(f"❌ Error processing audio file: {str(e)}")
    
    st.markdown("---")
    st.subheader("✏️ Manual Note Entry")
    
    with st.form("add_note_form"):
        note_content = st.text_area(
            "Note Content:",
            placeholder="Enter your note here...",
            height=150,
            key="note_content_area"
        )
        
        submitted = st.form_submit_button("💾 Save Note")
        
        if submitted:
            if note_content.strip():
                result = make_api_call("/add_note", method="POST", data={"content": note_content})
                if result:
                    st.balloons()
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
    notes = make_api_call("/get_notes", show_response=False)
    
    if notes:
        if len(notes) == 0:
            st.info("📭 No notes found. Add some notes to get started!")
        else:
            st.success(f"📊 Found {len(notes)} notes")
            
            # Display notes in a nice format
            for i, note in enumerate(notes, 1):
                with st.expander(f"📄 Note #{note[0]} - {note[1][:50]}..."):
                    st.write(f"**ID:** {note[0]}")
                    
                    # Check if this note is being edited
                    is_editing = st.session_state.get(f"editing_{note[0]}", False)
                    
                    if is_editing:
                        # Edit mode
                        edited_content = st.text_area(
                            "Edit Note:",
                            value=note[1],
                            height=150,
                            key=f"edit_text_{note[0]}"
                        )
                        
                        col1, col2, col3 = st.columns([1, 1, 2])
                        with col1:
                            if st.button(f"💾 Save", key=f"save_{note[0]}"):
                                if edited_content.strip():
                                    result = make_api_call(f"/edit_note/{note[0]}", method="PUT", data={"content": edited_content}, show_response=False)
                                    if result:
                                        st.success(f"✅ Note #{note[0]} updated successfully!")
                                        st.session_state[f"editing_{note[0]}"] = False
                                        st.rerun()
                                else:
                                    st.error("❌ Note content cannot be empty!")
                        
                        with col2:
                            if st.button(f"❌ Cancel", key=f"cancel_{note[0]}"):
                                st.session_state[f"editing_{note[0]}"] = False
                                st.rerun()
                    else:
                        # View mode
                        st.write(f"**Content:** {note[1]}")
                        st.write(f"**Added:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns([1, 1, 2])
                        
                        with col1:
                            if st.button(f"✏️ Edit", key=f"edit_{note[0]}"):
                                st.session_state[f"editing_{note[0]}"] = True
                                st.rerun()
                        
                        with col2:
                            if st.button(f"🗑️ Delete", key=f"delete_{note[0]}"):
                                # Two-step delete confirmation: first click sets flag, second click deletes
                                if st.session_state.get(f"confirm_delete_{note[0]}", False):
                                    # Second click: actually delete the note
                                    result = make_api_call(f"/delete_note/{note[0]}", method="DELETE", show_response=False)
                                    if result:
                                        st.success(f"✅ Note #{note[0]} deleted successfully!")
                                        # Clear the confirmation flag
                                        if f"confirm_delete_{note[0]}" in st.session_state:
                                            del st.session_state[f"confirm_delete_{note[0]}"]
                                        st.rerun()
                                else:
                                    # First click: set confirmation flag for next click
                                    st.session_state[f"confirm_delete_{note[0]}"] = True
                                    st.rerun()
                        
                        # Show confirmation UI when delete is pending
                        if st.session_state.get(f"confirm_delete_{note[0]}", False):
                            st.warning(f"⚠️ Click '✅Confirm Delete' to delete the Note #{note[0]}")
                            with col1:
                                if st.button(f"✅ Confirm Delete", key=f"confirm_{note[0]}"):
                                    result = make_api_call(f"/delete_note/{note[0]}", method="DELETE", show_response=False)
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

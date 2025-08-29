import streamlit as st
import requests
import json
from datetime import datetime
import io
import tempfile
import os

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
def make_api_call(endpoint, method="GET", data=None, show_response=True, files=None):
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files)
            else:
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
            # Read file content
            file_content = uploaded_text_file.read().decode('utf-8')
            st.success(f"✅ Text file '{uploaded_text_file.name}' uploaded successfully!")
            st.text_area("File Content Preview:", file_content, height=100, disabled=True)
            
            # Add button to save file content as note
            if st.button("💾 Save Text File as Note", key="save_text"):
                result = make_api_call("/add_note", method="POST", data={"content": file_content})
                if result:
                    st.balloons()
                    st.rerun()
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
    
    # Voice input section
    st.markdown("### 🎤 Voice Input")
    st.markdown("**Note:** Voice input requires microphone permissions and works best in Chrome/Edge browsers.")
    
    # Create a simple voice input with better error handling
    voice_input_html = """
    <div id="voice-input-container">
        <button id="voice-btn" onclick="toggleVoiceInput()" style="
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 0;
        ">🎤 Start Voice Input</button>
        
        <div id="status" style="margin: 10px 0; font-weight: bold; color: #666;">Click the button above to start recording...</div>
        
        <div id="transcript-display" style="
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            min-height: 50px;
            border: 1px solid #ccc;
            font-family: Arial, sans-serif;
            font-size: 14px;
            white-space: pre-wrap;
        ">Your transcribed text will appear here...</div>
        
        <script>
        let recognition = null;
        let isRecording = false;
        let finalTranscript = '';
        
        function toggleVoiceInput() {
            if (!isRecording) {
                startVoiceInput();
            } else {
                stopVoiceInput();
            }
        }
        
        function startVoiceInput() {
            console.log('Starting voice input...');
            
            // Check if speech recognition is supported
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                document.getElementById('status').textContent = '❌ Speech recognition not supported in this browser. Please use Chrome or Edge.';
                document.getElementById('status').style.color = '#ff0000';
                return;
            }
            
            try {
                recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'en-US';
                
                recognition.onstart = function() {
                    console.log('Speech recognition started');
                    isRecording = true;
                    finalTranscript = '';
                    document.getElementById('voice-btn').textContent = '🔴 Stop Recording';
                    document.getElementById('voice-btn').style.backgroundColor = '#ff0000';
                    document.getElementById('status').textContent = '🎤 Listening... Speak now!';
                    document.getElementById('status').style.color = '#00ff00';
                    document.getElementById('transcript-display').textContent = 'Listening...';
                };
                
                recognition.onresult = function(event) {
                    console.log('Speech recognition result received');
                    let interimTranscript = '';
                    
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        const transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {
                            finalTranscript += transcript;
                        } else {
                            interimTranscript += transcript;
                        }
                    }
                    
                    // Display the transcript in real-time
                    const displayText = finalTranscript + interimTranscript;
                    const displayElement = document.getElementById('transcript-display');
                    if (displayElement) {
                        displayElement.textContent = displayText;
                        console.log('Transcript updated:', displayText);
                    }
                    
                    if (finalTranscript) {
                        const statusElement = document.getElementById('status');
                        if (statusElement) {
                            statusElement.textContent = '✅ Transcribed: ' + finalTranscript.substring(0, 50) + '...';
                        }
                    }
                };
                
                recognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                    let errorMessage = '❌ Error: ' + event.error;
                    
                    if (event.error === 'not-allowed') {
                        errorMessage = '❌ Microphone access denied. Please allow microphone permissions.';
                    } else if (event.error === 'no-speech') {
                        errorMessage = '❌ No speech detected. Please try speaking louder.';
                    } else if (event.error === 'network') {
                        errorMessage = '❌ Network error. Please check your internet connection.';
                    }
                    
                    document.getElementById('status').textContent = errorMessage;
                    document.getElementById('status').style.color = '#ff0000';
                    stopVoiceInput();
                };
                
                recognition.onend = function() {
                    console.log('Speech recognition ended');
                    stopVoiceInput();
                };
                
                recognition.start();
                
            } catch (error) {
                console.error('Error starting speech recognition:', error);
                document.getElementById('status').textContent = '❌ Error starting speech recognition: ' + error.message;
                document.getElementById('status').style.color = '#ff0000';
            }
        }
        
                 function stopVoiceInput() {
             console.log('Stopping voice input...');
             if (recognition) {
                 recognition.stop();
             }
             isRecording = false;
             document.getElementById('voice-btn').textContent = '🎤 Start Voice Input';
             document.getElementById('voice-btn').style.backgroundColor = '#ff4b4b';
             
             if (finalTranscript) {
                 document.getElementById('status').textContent = '⏹️ Recording stopped - Ready to save!';
                 document.getElementById('status').style.color = '#ffaa00';
                 
                                                     // Store transcribed text and show save button
                  try {
                      sessionStorage.setItem('transcribedText', finalTranscript);
                      console.log('Transcribed text stored in sessionStorage:', finalTranscript);
                      
                      // Update status to show success
                      document.getElementById('status').textContent = '✅ Text ready! Click "Save Voice Note" to save.';
                      document.getElementById('status').style.color = '#00aa00';
                      
                                             // Show save button
                       const saveButtonDiv = document.createElement('div');
                       saveButtonDiv.innerHTML = '<button id="save-voice-note" onclick="saveVoiceNoteToAPI()" style="background-color: #4caf50; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px 0;"><strong>💾 Save Voice Note</strong></button>';
                       document.getElementById('transcript-display').appendChild(saveButtonDiv);
                      
                  } catch (error) {
                      console.error('Error storing transcribed text:', error);
                      document.getElementById('status').textContent = '❌ Error storing transcribed text';
                      document.getElementById('status').style.color = '#ff0000';
                  }
             } else {
                 document.getElementById('status').textContent = '⏹️ Recording stopped - No text captured';
                 document.getElementById('status').style.color = '#ffaa00';
             }
         }
        
                           // Function to get the transcribed text
          function getTranscribedText() {
              return finalTranscript;
          }
         
         // Initialize when page loads
         window.onload = function() {
             console.log('Voice input component loaded');
             document.getElementById('status').textContent = 'Ready to record. Click "Start Voice Input" to begin.';
         };
        </script>
    </div>
    """
    
    # Display the voice input component
    st.components.v1.html(voice_input_html, height=350)
    
    # Add JavaScript to handle save voice note button
    save_handler_html = """
    <script>
    function saveVoiceNoteToAPI() {
        const text = sessionStorage.getItem('transcribedText');
        if (text) {
            // Make API call to save the note
            fetch('http://localhost:8000/add_note', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: text })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert('✅ Voice note saved successfully!');
                    sessionStorage.removeItem('transcribedText');
                    // Clear the transcript display
                    const transcriptDisplay = document.getElementById('transcript-display');
                    if (transcriptDisplay) {
                        transcriptDisplay.textContent = 'Voice note saved successfully!';
                    }
                    // Update status
                    const statusElement = document.getElementById('status');
                    if (statusElement) {
                        statusElement.textContent = '✅ Voice note saved!';
                        statusElement.style.color = '#00aa00';
                    }
                } else {
                    alert('❌ Error saving voice note');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('❌ Error saving voice note: ' + error.message);
            });
        } else {
            alert('No transcribed text found. Please use voice input first.');
        }
    }
    
    // Listen for button clicks
    window.addEventListener('load', function() {
        // Check if there's text in sessionStorage on page load
        const text = sessionStorage.getItem('transcribedText');
        if (text) {
            console.log('Found transcribed text in sessionStorage on page load');
        }
    });
    </script>
    """
    st.components.v1.html(save_handler_html, height=0)
    
    # Add instructions
    st.markdown("""
    **Instructions:**
    1. Click "🎤 Start Voice Input" (button will turn red)
    2. Allow microphone permissions if prompted
    3. Speak clearly into your microphone
    4. Click "🔴 Stop Recording" when done
    5. The transcribed text will automatically appear in the Note Content box below
    6. Click "💾 Save Note" to save
    """)
    
    # Initialize session state for transcribed text
    if 'voice_transcribed_text' not in st.session_state:
        st.session_state.voice_transcribed_text = ""
    
    with st.form("add_note_form"):
        note_content = st.text_area(
            "Note Content:",
            placeholder="Enter your note here or use voice input above...",
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
                    st.write(f"**Content:** {note[1]}")
                    st.write(f"**Added:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Add delete button with confirmation
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button(f"🗑️ Delete", key=f"delete_{note[0]}"):
                            # Check if this is a confirmation click
                            if st.session_state.get(f"confirm_delete_{note[0]}", False):
                                # Actually delete the note
                                result = make_api_call(f"/delete_note/{note[0]}", method="DELETE", show_response=False)
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

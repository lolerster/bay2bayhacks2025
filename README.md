# Bay2BayHacks2025 - AI-Powered Notes App

A comprehensive notes application built with FastAPI and Streamlit for the Bay2BayHacks2025 hackathon. Create, manage, and get AI-powered insights from your notes with features like file uploads, audio transcription, and intelligent note editing.

## 🚀 Features

### Core Functionality
- **📝 Create Notes** - Manual text entry with rich formatting
- **📋 View & Manage Notes** - Browse all notes with expandable cards
- **✏️ Edit Notes** - In-place editing with real-time updates
- **🗑️ Delete Notes** - Two-step confirmation for safe deletion
- **🔄 Real-time Updates** - Instant feedback and automatic refresh

### File Upload Support
- **📁 Text File Upload** - Support for TXT, MD, CSV, JSON files (up to 5MB)
- **🎵 Audio File Upload** - Convert speech to text using OpenAI Whisper
- **📄 File Preview** - Preview uploaded content before saving
- **🔒 File Validation** - Size limits and encoding validation

### AI-Powered Features
- **🤖 AI Summarization** - Get intelligent summaries of all your notes
- **❓ Smart Q&A** - Ask questions about your notes in natural language
- **🎤 Audio Transcription** - Convert audio files to text automatically
- **🧠 Context-Aware Responses** - AI references specific note IDs

### User Experience
- **🎨 Modern UI** - Clean, responsive Streamlit interface
- **📱 Mobile-Friendly** - Works seamlessly on all devices
- **⚡ Fast Performance** - Optimized API calls and database operations
- **🛡️ Error Handling** - Comprehensive error messages and validation

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLite** - Lightweight, serverless database
- **Pydantic** - Data validation and settings management
- **Uvicorn** - Lightning-fast ASGI server

### Frontend
- **Streamlit** - Beautiful web interface for data apps
- **Requests** - HTTP library for API communication

### AI & External Services
- **OpenAI GPT-4o-mini** - AI summarization and Q&A
- **OpenAI Whisper** - Audio transcription service

### Development Tools
- **python-dotenv** - Environment variable management
- **Context Managers** - Safe database connections

## 📋 Prerequisites

- **Python 3.8+**
- **OpenAI API key** (for AI features)
- **Git** (for cloning)

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Bay2BayHacks2025
```

### 2. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Get your OpenAI API key from:** https://platform.openai.com/api-keys

### 5. Run the application

#### Start the FastAPI backend:
```bash
uvicorn app:app --reload
```

#### In a new terminal, start the Streamlit frontend:
```bash
streamlit run streamlit_app.py
```

## 🌐 Access Points

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Streamlit Frontend**: http://localhost:8501

## 📚 API Endpoints

### Core Note Operations
```http
# Add a new note
POST /add_note
Content-Type: application/json
{
    "content": "Your note content here"
}

# Get all notes
GET /get_notes

# Edit a note
PUT /edit_note/{note_id}
Content-Type: application/json
{
    "content": "Updated note content"
}

# Delete a note
DELETE /delete_note/{note_id}
```

### AI Features
```http
# Summarize all notes
POST /summarize

# Ask questions about notes
POST /ask
Content-Type: application/json
{
    "query": "What did I write about groceries?"
}

# Transcribe audio file
POST /transcribe_audio
Content-Type: multipart/form-data
audio_file: [audio file]
```

### API Information
```http
# Get API information
GET /
```

## 🎨 Streamlit Frontend Features

### 📝 Add Note Page
- **Manual Entry** - Rich text area for note creation
- **File Upload** - Drag & drop text files (TXT, MD, CSV, JSON)
- **Audio Upload** - Upload audio files for transcription
- **File Preview** - Preview content before saving
- **Size Validation** - 5MB limit for text files, 25MB for audio

### 📋 View Notes Page
- **Expandable Cards** - Clean note display with previews
- **Edit Mode** - In-place editing with save/cancel options
- **Delete Confirmation** - Two-step deletion for safety
- **Real-time Updates** - Automatic refresh after changes
- **Note ID Display** - Easy reference for note management

### 🤖 AI Features
- **One-Click Summarization** - Generate AI summaries instantly
- **Natural Language Q&A** - Ask questions about your notes
- **Context-Aware Responses** - AI references specific note IDs
- **Audio Transcription** - Convert speech to text automatically

### 🎯 User Experience
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Loading Indicators** - Visual feedback during operations
- **Error Messages** - Clear, helpful error notifications
- **Success Feedback** - Confirmation messages and animations

## 📁 Project Structure

```
Bay2BayHacks2025/
├── app.py                 # FastAPI backend application
├── streamlit_app.py       # Streamlit frontend interface
├── requirements.txt       # Python dependencies
├── notes.db              # SQLite database (auto-created)
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY` - Your OpenAI API key (required for AI features)

### Database
- **Auto-created** - SQLite database (`notes.db`) is created automatically
- **Persistent** - Data persists between application restarts
- **Secure** - Database file is ignored by Git

### File Upload Limits
- **Text Files**: 5MB maximum
- **Audio Files**: 25MB maximum (OpenAI Whisper limit)
- **Supported Formats**: TXT, MD, CSV, JSON, WAV, MP3, M4A, OGG

## 🧪 Testing the Application

### Using the Streamlit Frontend (Recommended)
1. Open http://localhost:8501 in your browser
2. Navigate through the sidebar to test different features:
   - **Add Note**: Try manual entry and file uploads
   - **View Notes**: Test editing and deletion
   - **Summarize**: Generate AI summaries
   - **Ask Questions**: Query your notes with natural language

### Using the API Directly
```bash
# Add a note
curl -X POST "http://localhost:8000/add_note" \
     -H "Content-Type: application/json" \
     -d '{"content": "Buy groceries tomorrow"}'

# Get all notes
curl -X GET "http://localhost:8000/get_notes"

# Edit a note (replace {note_id} with actual ID)
curl -X PUT "http://localhost:8000/edit_note/{note_id}" \
     -H "Content-Type: application/json" \
     -d '{"content": "Updated grocery list"}'

# Delete a note (replace {note_id} with actual ID)
curl -X DELETE "http://localhost:8000/delete_note/{note_id}"

# Summarize notes
curl -X POST "http://localhost:8000/summarize"

# Ask a question
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What did I write about groceries?"}'
```

### Using Swagger UI
1. Open http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out" to test the endpoint
4. Enter your data and click "Execute"

## 🔒 Security & Best Practices

### Security Features
- **Environment Variables** - Secure API key management
- **SQL Parameterization** - Prevents injection attacks
- **Input Validation** - Pydantic models for data validation
- **File Type Validation** - Secure file upload handling
- **Size Limits** - Prevents resource exhaustion

### Code Quality
- **Error Handling** - Comprehensive try-catch blocks
- **Database Connections** - Context managers for safe connections
- **Session State Management** - Proper Streamlit state handling
- **Clean Code** - Well-documented and maintainable codebase

## 🚀 Deployment

### Local Development
```bash
# Backend
uvicorn app:app --reload

# Frontend (in separate terminal)
streamlit run streamlit_app.py
```

### Production
```bash
# Backend
uvicorn app:app --host 0.0.0.0 --port 8000

# Frontend
streamlit run streamlit_app.py --server.port 8501
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - For the excellent web framework
- **Streamlit** - For the beautiful frontend framework
- **OpenAI** - For the AI capabilities (GPT-4o-mini and Whisper)
- **Bay2BayHacks2025** - For the hackathon opportunity

## 📞 Support & Troubleshooting

### Common Issues
1. **API Connection Error** - Ensure FastAPI server is running on port 8000
2. **OpenAI API Error** - Check your API key in the `.env` file
3. **File Upload Issues** - Verify file size and format restrictions
4. **Database Errors** - Check file permissions for `notes.db`

### Getting Help
1. Check the [API documentation](http://localhost:8000/docs)
2. Try the [Streamlit frontend](http://localhost:8501)
3. Review console error messages
4. Ensure all dependencies are installed correctly

---

**Happy coding! 🎉**

*Built with ❤️ for Bay2BayHacks2025*

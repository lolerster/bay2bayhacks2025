# Bay2BayHacks2025 - AI-Powered Notes API

A FastAPI-based notes application with OpenAI integration for the Bay2BayHacks2025 hackathon. This project allows users to create, retrieve, and get AI-powered summaries of their notes.

## 🚀 Features

- **FastAPI REST API** for managing notes
- **SQLite database** for data persistence
- **OpenAI GPT-4o-mini integration** for AI-powered note summarization
- **Environment variable management** for secure API key handling
- **Simple and clean API endpoints**
- **Automatic API documentation** with Swagger UI
- **🎨 Streamlit MVP Frontend** - Beautiful web interface for easy testing

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit (Python)
- **Database**: SQLite
- **AI**: OpenAI GPT-4o-mini
- **Environment**: python-dotenv
- **Server**: Uvicorn

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Git

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Bay2BayHacks2025
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up environment variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Get your OpenAI API key from:** https://platform.openai.com/api-keys

### 6. Run the application

#### Option A: Easy Launcher (Recommended)
```bash
python run_app.py
```
Choose option 3 to run both backend and frontend.

#### Option B: Manual Start
**Start the FastAPI backend:**
```bash
uvicorn app:app --reload
```

**In a new terminal, start the Streamlit frontend:**
```bash
streamlit run streamlit_app.py
```

## 🌐 Access Points

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Streamlit Frontend**: http://localhost:8501

## 📚 API Endpoints

### Add a Note
```http
POST /add_note
Content-Type: application/json

{
    "content": "Your note content here"
}
```

### Get All Notes
```http
GET /get_notes
```

### Summarize Notes
```http
POST /summarize
```

### Ask Questions
```http
POST /ask
Content-Type: application/json

{
    "query": "What did I write about groceries?"
}
```

### Interactive API Documentation
```http
GET /docs
```
Visit http://localhost:8000/docs for interactive Swagger UI documentation.

## 🎨 Streamlit Frontend Features

The Streamlit MVP provides a beautiful web interface with:

- **📝 Add Notes** - Easy note creation with text area
- **📋 View Notes** - Browse all your notes in expandable cards
- **🤖 AI Summarizer** - One-click AI-powered note summarization
- **❓ Ask Questions** - Query your notes with natural language
- **🔄 Real-time Updates** - Instant feedback and refresh capabilities
- **📱 Responsive Design** - Works on desktop and mobile

## 📁 Project Structure

```
Bay2BayHacks2025/
├── app.py              # Main FastAPI application
├── streamlit_app.py    # Streamlit frontend
├── run_app.py          # Easy launcher script
├── requirements.txt    # Python dependencies
├── notes.db           # SQLite database (auto-created, ignored by git)
├── venv/              # Virtual environment (ignored by git)
├── .env               # Environment variables (ignored by git)
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
└── README.md          # This file
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Database
- The SQLite database (`notes.db`) is automatically created on first run
- Database file is ignored by Git for security

## 🧪 Testing the Application

### Using the Streamlit Frontend (Recommended)
1. Open http://localhost:8501 in your browser
2. Navigate through the sidebar to test different features
3. Add notes, view them, and try the AI features

### Using curl

**Add a note:**
```bash
curl -X POST "http://localhost:8000/add_note" \
     -H "Content-Type: application/json" \
     -d '{"content": "Buy groceries tomorrow"}'
```

**Get all notes:**
```bash
curl -X GET "http://localhost:8000/get_notes"
```

**Summarize notes:**
```bash
curl -X POST "http://localhost:8000/summarize"
```

**Ask a question:**
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What did I write about groceries?"}'
```

### Using the Swagger UI
1. Open http://localhost:8000/docs in your browser
2. Click on any endpoint to expand it
3. Click "Try it out" to test the endpoint
4. Enter your data and click "Execute"

## 🔒 Security Features

- **Environment variables** for sensitive data
- **SQL parameterization** to prevent injection attacks
- **Input validation** using Pydantic models
- **API key validation** on startup

## 🚀 Deployment

### Local Development
```bash
python run_app.py
```

### Production
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
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

- FastAPI for the excellent web framework
- Streamlit for the beautiful frontend framework
- OpenAI for the AI capabilities
- Bay2BayHacks2025 organizers for the hackathon opportunity

## 📞 Support

If you encounter any issues or have questions:
1. Check the [API documentation](http://localhost:8000/docs)
2. Try the [Streamlit frontend](http://localhost:8501)
3. Review the error messages in the console
4. Ensure your OpenAI API key is correctly set in the `.env` file
5. Make sure all dependencies are installed

---

**Happy coding! 🎉**

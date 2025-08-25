# Bay2BayHacks2025 - AI-Powered Notes API

A FastAPI-based notes application with OpenAI integration for the Bay2BayHacks2025 hackathon. This project allows users to create, retrieve, and get AI-powered summaries of their notes.

## 🚀 Features

- **FastAPI REST API** for managing notes
- **SQLite database** for data persistence
- **OpenAI GPT-4o-mini integration** for AI-powered note summarization
- **Environment variable management** for secure API key handling
- **Simple and clean API endpoints**
- **Automatic API documentation** with Swagger UI

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
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
```bash
uvicorn app:app --reload
```

The API will be available at: http://localhost:8000

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

### Interactive API Documentation
```http
GET /docs
```
Visit http://localhost:8000/docs for interactive Swagger UI documentation.

## 📁 Project Structure

```
Bay2BayHacks2025/
├── app.py              # Main FastAPI application
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

## 🧪 Testing the API

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
uvicorn app:app --reload --host 0.0.0.0 --port 8000
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
- OpenAI for the AI capabilities
- Bay2BayHacks2025 organizers for the hackathon opportunity

## 📞 Support

If you encounter any issues or have questions:
1. Check the [API documentation](http://localhost:8000/docs)
2. Review the error messages in the console
3. Ensure your OpenAI API key is correctly set in the `.env` file
4. Make sure all dependencies are installed

---

**Happy coding! 🎉**

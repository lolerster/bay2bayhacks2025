# Bay2BayHacks2025 - Notes API

A FastAPI-based notes application with OpenAI integration for the Bay2BayHacks2025 hackathon.

## Features

- FastAPI REST API for managing notes
- SQLite database for data persistence
- OpenAI integration for AI-powered features
- Simple and clean API endpoints

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Bay2BayHacks2025
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

6. **Run the application**
   ```bash
   uvicorn app:app --reload
   ```

## API Endpoints

- `POST /add_note` - Add a new note
- `GET /docs` - Interactive API documentation (Swagger UI)

## Project Structure

```
Bay2BayHacks2025/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── notes.db           # SQLite database (ignored by git)
├── venv/              # Virtual environment (ignored by git)
└── README.md          # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

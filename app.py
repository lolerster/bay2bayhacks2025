import openai
from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application instance
app = FastAPI()

# OpenAI API key for authentication
# Get API key from environment variable for security
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Database setup
conn = sqlite3.connect('notes.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
''')
conn.commit()

# API modeels
class Note(BaseModel):
    content: str

class Query(BaseModel):
    query: str

# Endpoints
@app.post("/add_note")
def add_note(note: Note):
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (note.content))
    conn.commit()
    return {"message": "Note added successfully"}

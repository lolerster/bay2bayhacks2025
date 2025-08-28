from openai import OpenAI
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
if not OPENAI_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=OPENAI_KEY)

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

# API models
class Note(BaseModel):
    content: str

class Query(BaseModel):
    query: str

# Root endpoint
@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "message": "Bay2BayHacks2025 - AI Notes API",
        "version": "1.0.0",
        "endpoints": {
            "add_note": "POST /add_note",
            "get_notes": "GET /get_notes", 
            "summarize": "POST /summarize",
            "ask": "POST /ask"
        },
        "docs": "/docs",
        "status": "running"
    }

# Endpoints
@app.post("/add_note")
def add_note(note: Note):
    try:
        cur = conn.cursor()  # create a new cursor per request
        cur.execute("INSERT INTO notes (content) VALUES (?)", (note.content,))
        conn.commit()
        return {"message": "Note added successfully"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/get_notes")
def get_notes():
    cursor.execute("SELECT * FROM notes")
    return cursor.fetchall()

@app.post("/summarize")
def summarize():
    cursor.execute("SELECT * FROM notes")
    all_notes = " ".join([note[1] for note in cursor.fetchall()])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Concisely summarize the following notes."},
            {"role": "user", "content": all_notes}
        ]
    )
    return response.choices[0].message.content

@app.post("/ask")
def ask(query: Query):
    cursor.execute("SELECT content FROM notes WHERE content LIKE ?", (f"%{query.query}%",))
    match = " ".join([content[0] for content in cursor.fetchall()])
    if not match:
        return "No matching notes found."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer the user's question based on the provided notes."},
            {"role": "user", "content": f"Notes: {match}\nQuestion: {query.query}"}
        ]
    )
    return response.choices[0].message.content

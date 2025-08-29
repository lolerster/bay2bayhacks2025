from openai import OpenAI
from fastapi import FastAPI, HTTPException
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

@app.delete("/delete_note/{note_id}")
def delete_note(note_id: int):
    with sqlite3.connect("notes.db") as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Note not found")
    return {"message": f"Note {note_id} deleted successfully"}
    
@app.get("/get_notes")
def get_notes():
    cursor.execute("SELECT * FROM notes")
    return cursor.fetchall()

@app.post("/summarize")
def summarize():
    try:
        cursor.execute("SELECT * FROM notes")
        all_notes = " ".join([note[1] for note in cursor.fetchall()])
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Concisely summarize the following notes."},
                {"role": "user", "content": all_notes}
            ]
        )
    except Exception as e:
        return {"error": str(e)}
    return response.choices[0].message.content

@app.post("/ask")
def ask(query: Query):
    try:
        # Input validation
        if not query.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        
        # Search for relevant notes using multiple strategies
        relevant_notes = []
        
        # Strategy 1: Direct keyword matching
        cursor.execute("SELECT id, content FROM notes WHERE content LIKE ?", (f"%{query.query}%",))
        keyword_matches = cursor.fetchall()
        relevant_notes.extend(keyword_matches)
        
        # Strategy 2: Get all notes if no keyword matches found
        if not relevant_notes:
            cursor.execute("SELECT * FROM notes")
            relevant_notes = cursor.fetchall()
        
        if not relevant_notes:
            return "No notes found to answer your question. Please add some notes first."
        
        # Prepare context with note IDs for better traceability
        context_parts = []
        for note_id, content in relevant_notes:
            context_parts.append(f"Note #{note_id}: {content}")
        
        context = "\n\n".join(context_parts)
        
        # Limit context length to avoid token limits (roughly 3000 characters)
        if len(context) > 3000:
            context = context[:3000] + "... (truncated)"
        
        # Enhanced prompt for better responses
        system_prompt = """You are a helpful AI assistant that answers questions based on the user's notes. 
        Follow these guidelines:
        1. Only answer based on the provided notes
        2. If the information isn't in the notes, say so clearly
        3. Be concise but informative
        4. If multiple notes are relevant, synthesize the information
        5. Reference note IDs when possible (e.g., "According to Note #3...")
        6. If no relevant notes are found, suggest what kind of information might help"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Notes:\n{context}\n\nQuestion: {query.query}"}
            ],
            max_tokens=500,  # Limit response length
            temperature=0.3   # Lower temperature for more focused answers
        )
        
        return response.choices[0].message.content
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

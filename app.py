from openai import OpenAI
from fastapi import FastAPI, HTTPException, UploadFile, File
import sqlite3
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import io

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
            "ask": "POST /ask",
            "transcribe_audio": "POST /transcribe_audio"
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
        return {"message": "Note added successfully", "id": cur.lastrowid}
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
        
        # Get all notes
        cursor.execute("SELECT * FROM notes")
        all_notes = cursor.fetchall()
        
        if not all_notes:
            return "No notes found to answer your question. Please add some notes first."
        
        # Prepare context with note IDs for better traceability
        context_parts = []
        for note_id, content in all_notes:
            context_parts.append(f"Note #{note_id}: {content}")
        
        context = "\n\n".join(context_parts)
        
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

@app.post("/transcribe_audio")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """Transcribe audio file using OpenAI Whisper API"""
    try:
        # Check file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read the uploaded file
        audio_content = await audio_file.read()
        
        # Create a file-like object from the audio content
        audio_file_obj = io.BytesIO(audio_content)
        audio_file_obj.name = audio_file.filename
        
        # Use OpenAI Whisper API for transcription
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file_obj
        )
        
        return {"transcription": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")

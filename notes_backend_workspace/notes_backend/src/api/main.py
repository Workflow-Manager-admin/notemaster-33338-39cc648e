from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .models import Note, NoteCreate, NoteUpdate
from .note_service import create_note, get_notes, get_note, update_note, delete_note

app = FastAPI(
    title="Notes API",
    description="Handles server-side logic for notes management.",
    version="1.0.0",
    openapi_tags=[
        {'name': 'notes', 'description': 'Endpoints to manage notes'},
        {'name': 'health', 'description': 'Healthcheck endpoint'},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"], summary="Health check", description="Returns API health status")
def health_check():
    """Health check endpoint for API and load balancers."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.post(
    "/notes",
    response_model=Note,
    status_code=201,
    summary="Create a new note",
    description="Creates a new note and stores it in Supabase.",
    tags=["notes"],
)
def api_create_note(note: NoteCreate):
    """Create a new note."""
    try:
        return create_note(note)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating note: {e}")


# PUBLIC_INTERFACE
@app.get(
    "/notes",
    response_model=List[Note],
    summary="List all notes",
    description="Returns a list of all notes in Supabase.",
    tags=["notes"],
)
def api_get_notes():
    """List all notes."""
    try:
        return get_notes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching notes: {e}")


# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=Note,
    summary="Get a note by ID",
    description="Fetch a single note by its unique ID.",
    tags=["notes"],
)
def api_get_note(note_id: str):
    """Fetch a note by ID."""
    note = get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=Note,
    summary="Update a note",
    description="Update the title and/or content of an existing note.",
    tags=["notes"],
)
def api_update_note(note_id: str, note_data: NoteUpdate):
    """Update a note by ID."""
    note = update_note(note_id, note_data)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found or update failed")
    return note


# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    response_model=dict,
    summary="Delete a note",
    description="Delete a note by its unique ID.",
    tags=["notes"],
)
def api_delete_note(note_id: str):
    """Delete a note by ID."""
    success = delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}

# note_service.py
from typing import List, Optional
from datetime import datetime
from .supabase import get_supabase_client
from .models import Note, NoteCreate, NoteUpdate
from uuid import uuid4

SUPABASE_TABLE = "notes"


# PUBLIC_INTERFACE
def create_note(note: NoteCreate) -> Note:
    """
    Create a note in Supabase.
    """
    client = get_supabase_client()
    new_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    response = client.table(SUPABASE_TABLE).insert({
        "id": new_id,
        "title": note.title,
        "content": note.content,
        "created_at": now,
        "updated_at": now,
    }).execute()
    if response.error:
        raise Exception(response.error.message)
    inserted = response.data[0]
    return Note(
        id=inserted["id"],
        title=inserted["title"],
        content=inserted["content"],
        created_at=datetime.fromisoformat(inserted["created_at"].replace('Z', '')),
        updated_at=datetime.fromisoformat(inserted["updated_at"].replace('Z', '')),
    )


# PUBLIC_INTERFACE
def get_notes() -> List[Note]:
    """
    Get a list of all notes from Supabase.
    """
    client = get_supabase_client()
    response = client.table(SUPABASE_TABLE).select("*").order("created_at", desc=False).execute()
    if response.error:
        raise Exception(response.error.message)
    notes = []
    for record in response.data:
        notes.append(
            Note(
                id=record["id"],
                title=record["title"],
                content=record["content"],
                created_at=datetime.fromisoformat(record["created_at"].replace('Z', '')),
                updated_at=datetime.fromisoformat(record["updated_at"].replace('Z', '')),
            )
        )
    return notes


# PUBLIC_INTERFACE
def get_note(note_id: str) -> Optional[Note]:
    """
    Get a single note by ID.
    """
    client = get_supabase_client()
    response = client.table(SUPABASE_TABLE).select("*").eq("id", note_id).single().execute()
    if response.error:
        return None
    record = response.data
    if not record:
        return None
    return Note(
        id=record["id"],
        title=record["title"],
        content=record["content"],
        created_at=datetime.fromisoformat(record["created_at"].replace('Z', '')),
        updated_at=datetime.fromisoformat(record["updated_at"].replace('Z', '')),
    )


# PUBLIC_INTERFACE
def update_note(note_id: str, note_data: NoteUpdate) -> Optional[Note]:
    """
    Update a note in Supabase.
    """
    client = get_supabase_client()
    note_dict = {k: v for k, v in note_data.dict().items() if v is not None}
    if not note_dict:
        return get_note(note_id)  # No update performed
    note_dict["updated_at"] = datetime.utcnow().isoformat()
    response = client.table(SUPABASE_TABLE).update(note_dict).eq("id", note_id).execute()
    if response.error or not response.data:
        return None
    updated_record = response.data[0]
    return Note(
        id=updated_record["id"],
        title=updated_record["title"],
        content=updated_record["content"],
        created_at=datetime.fromisoformat(updated_record["created_at"].replace('Z', '')),
        updated_at=datetime.fromisoformat(updated_record["updated_at"].replace('Z', '')),
    )


# PUBLIC_INTERFACE
def delete_note(note_id: str) -> bool:
    """
    Delete a note by ID.
    """
    client = get_supabase_client()
    response = client.table(SUPABASE_TABLE).delete().eq("id", note_id).execute()
    if response.error:
        return False
    return response.count > 0 or (isinstance(response.data, list) and len(response.data) > 0)

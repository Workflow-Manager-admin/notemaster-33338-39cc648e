# models.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# PUBLIC_INTERFACE
class NoteCreate(BaseModel):
    """Pydantic schema for note creation"""
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content/body of the note")


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Pydantic schema for updating a note"""
    title: Optional[str] = Field(None, description="Updated title of the note")
    content: Optional[str] = Field(None, description="Updated content/body of the note")


# PUBLIC_INTERFACE
class Note(BaseModel):
    """Pydantic schema for returned notes"""
    id: str = Field(..., description="ID of the note")
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content/body of the note")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

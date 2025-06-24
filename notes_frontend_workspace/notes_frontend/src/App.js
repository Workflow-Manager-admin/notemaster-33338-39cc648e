import React, { useEffect, useState } from 'react';
import './App.css';

// PUBLIC_INTERFACE
function App() {
  // State
  const [notes, setNotes] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [editingNote, setEditingNote] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Backend API base URL (adjust if hosted elsewhere)
  const API_BASE = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  // Load notes on mount
  useEffect(() => {
    fetchNotes();
  }, []);

  // PUBLIC_INTERFACE
  async function fetchNotes() {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_BASE}/notes/`);
      if (!res.ok) throw new Error('Failed to load notes');
      const data = await res.json();
      setNotes(data);
    } catch (err) {
      setError('Error loading notes');
    } finally {
      setLoading(false);
    }
  }

  // PUBLIC_INTERFACE
  async function handleSelectNote(id) {
    setSelectedId(id);
    setEditingNote(null);
  }

  // PUBLIC_INTERFACE
  function handleCreateNew() {
    setSelectedId(null);
    setEditingNote({ title: '', content: '' });
  }

  // PUBLIC_INTERFACE
  async function handleDeleteNote(id) {
    setLoading(true);
    setError('');
    try {
      await fetch(`${API_BASE}/notes/${id}`, { method: 'DELETE' });
      setNotes(n => n.filter(note => note.id !== id));
      setSelectedId(null);
      setEditingNote(null);
    } catch {
      setError('Failed to delete note');
    } finally {
      setLoading(false);
    }
  }

  // PUBLIC_INTERFACE
  function handleEditNote(note) {
    setEditingNote({ ...note });
  }

  // PUBLIC_INTERFACE
  async function handleSaveNote(note) {
    setLoading(true);
    setError('');
    try {
      let updated;
      if (note.id) {
        const res = await fetch(`${API_BASE}/notes/${note.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(note),
        });
        if (!res.ok) throw new Error();
        updated = await res.json();
        setNotes(ns => ns.map(n => n.id === updated.id ? updated : n));
      } else {
        const res = await fetch(`${API_BASE}/notes/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(note),
        });
        if (!res.ok) throw new Error();
        updated = await res.json();
        setNotes(ns => [...ns, updated]);
      }
      setEditingNote(null);
      setSelectedId(updated.id);
    } catch {
      setError('Failed to save note');
    } finally {
      setLoading(false);
    }
  }

  // PUBLIC_INTERFACE
  function getSelectedNote() {
    return notes.find(n => n.id === selectedId);
  }

  // Core layout 
  return (
    <div className="notemaster-app light">
      <Sidebar
        notes={notes}
        selectedId={selectedId}
        onSelect={handleSelectNote}
        onNew={handleCreateNew}
        loading={loading}
      />
      <main className="main-area">
        <Header />
        <div className="main-content">
          {error && <div className="alert error">{error}</div>}
          {loading && <div className="loader">Loading...</div>}
          {!loading && editingNote !== null ? (
            <NoteEditor
              note={editingNote}
              onSave={handleSaveNote}
              onCancel={() => setEditingNote(null)}
            />
          ) : !loading && selectedId != null ? (
            <NoteViewer
              note={getSelectedNote()}
              onEdit={() => handleEditNote(getSelectedNote())}
              onDelete={() => handleDeleteNote(selectedId)}
            />
          ) : (
            <WelcomePanel />
          )}
        </div>
      </main>
    </div>
  );
}

// PUBLIC_INTERFACE
function Sidebar({ notes, selectedId, onSelect, onNew, loading }) {
  return (
    <nav className="sidebar">
      <div className="sidebar-header">
        <span className="logo-symbol">✦</span>
        <span className="sidebar-title">Notes</span>
      </div>
      <button className="btn-accent btn-block" onClick={onNew} disabled={loading}>
        + New Note
      </button>
      <ul className="note-list">
        {notes.length === 0 && <li className="note-list-empty">No notes</li>}
        {notes.map(note => (
          <li
            className={`note-list-item${note.id === selectedId ? ' selected' : ''}`}
            key={note.id}
            onClick={() => onSelect(note.id)}
          >
            <div className="note-title">{note.title || <em>(Untitled)</em>}</div>
            <div className="note-snippet">
              {note.content?.slice(0, 36)}
              {note.content && note.content.length > 36 ? '…' : ''}
            </div>
          </li>
        ))}
      </ul>
    </nav>
  );
}

// PUBLIC_INTERFACE
function Header() {
  return (
    <header className="main-header">
      <div className="brand">
        <span className="logo-symbol">✦</span>
        <span className="brand-title">notemaster</span>
      </div>
      <span className="brand-secondary">by KAVIA</span>
    </header>
  );
}

// PUBLIC_INTERFACE
function WelcomePanel() {
  return (
    <div className="welcome-panel">
      <h1 className="welcome-title">Welcome!</h1>
      <div className="welcome-desc">
        Select a note to view, or create a new note to get started.
      </div>
    </div>
  );
}

// PUBLIC_INTERFACE
function NoteViewer({ note, onEdit, onDelete }) {
  if (!note) return <div className="note-message">Note not found.</div>;
  return (
    <div className="note-view">
      <h2 className="note-view-title">{note.title}</h2>
      <pre className="note-view-content">{note.content}</pre>
      <div className="note-view-actions">
        <button className="btn-primary" onClick={onEdit}>Edit</button>
        <button className="btn-danger" onClick={onDelete}>Delete</button>
      </div>
    </div>
  );
}

// PUBLIC_INTERFACE
function NoteEditor({ note, onSave, onCancel }) {
  const [title, setTitle] = useState(note.title);
  const [content, setContent] = useState(note.content || '');

  // Sync edit state if swapped notes
  useEffect(() => {
    setTitle(note.title || '');
    setContent(note.content || '');
  }, [note]);

  // PUBLIC_INTERFACE
  function handleSubmit(e) {
    e.preventDefault();
    if (title.trim() === '' && content.trim() === '') return;
    onSave({ ...note, title, content });
  }

  return (
    <form className="note-editor" onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={e => setTitle(e.target.value)}
        className="input title"
        placeholder="Note title"
        maxLength={100}
        autoFocus
      />
      <textarea
        value={content}
        onChange={e => setContent(e.target.value)}
        className="input content"
        placeholder="Write your note..."
        rows={8}
      />
      <div className="editor-actions">
        <button className="btn-primary" type="submit">
          {note?.id ? 'Save Changes' : 'Create Note'}
        </button>
        <button className="btn" type="button" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
}

export default App;

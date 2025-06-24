# Supabase Integration for Notes Backend

This backend uses Supabase as a hosted PostgreSQL database for storing notes.

## Supabase Setup

1. The Supabase project must have a `notes` table with the following schema:

| Column     | Type (PostgreSQL)   | Required | Description         |
|------------|--------------------|----------|---------------------|
| id         | uuid (primary key) | Yes      | Note ID (UUID)      |
| title      | text               | Yes      | Note title          |
| content    | text               | Yes      | Note content/body   |
| created_at | timestamptz        | Yes      | When note was created|
| updated_at | timestamptz        | Yes      | Last update time    |

2. Copy the values for `SUPABASE_URL`, `SUPABASE_KEY`, and `SUPABASE_DB_URL` from your Supabase dashboard into the `.env` file.

## How It Is Used

- The backend reads configuration from the `.env` file at startup.
- All SQL/database operations (insert, select, update, delete) use Supabase's REST API via the `supabase-py` client.
- If your Supabase schema/table structure is different, update the fields in `note_service.py`.

## Required Env Vars

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_DB_URL` (for reference, mostly used for direct PG connections if needed)

No secrets should be hardcoded in code. All secrets must be in the `.env` file.

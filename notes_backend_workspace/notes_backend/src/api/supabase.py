# supabase.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


# PUBLIC_INTERFACE
def get_supabase_client() -> Client:
    """Get the Supabase client using environment variables."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in the environment.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

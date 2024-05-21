import os

from gotrue.types import AuthResponse, SignInWithEmailAndPasswordCredentials
from supabase import Client, create_client

url = os.getenv("SUPABASE_URL")
if not url:
    raise ValueError("No Supabase URL found in environment. Please set SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
if not key:
    raise ValueError("No Supabase key found in environment. Please set SUPABASE_KEY")

supabase: Client = create_client(url, key)

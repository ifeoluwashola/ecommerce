import os
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

url: str = SUPABASE_URL
key: str = SUPABASE_KEY
service_key: str = SUPABASE_SERVICE_KEY
supabase: Client = create_client(url, key)
service_client: Client = create_client(url, service_key)
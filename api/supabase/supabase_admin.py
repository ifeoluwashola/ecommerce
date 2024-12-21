from supabase import create_client
from supabase.lib.client_options import ClientOptions

from .supabase_client import service_key, url


supabase = create_client(url, service_key, options=ClientOptions(auto_refresh_token=False, persist_session=False,))

# Access auth admin api
admin_auth_client = supabase.auth.admin

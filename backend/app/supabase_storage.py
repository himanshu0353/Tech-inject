import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
BUCKET_NAME = os.getenv("SUPABASE_STORAGE_BUCKET", "component-bundles")

supabase_client: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Warning: Failed to initialize Supabase Client: {e}")

def upload_component_files(slug: str, files: dict[str, str]):
    """
    Uploads source code files for a component to private Supabase Storage bucket.
    Structure: component-bundles/<slug>/<filename>
    """
    if not supabase_client:
        return

    for filename, content in files.items():
        storage_path = f"{slug}/{filename}"
        content_bytes = content.encode("utf-8")
        
        try:
            supabase_client.storage.from_(BUCKET_NAME).upload(
                path=storage_path,
                file=content_bytes,
                file_options={"upsert": "true", "content-type": "text/plain"}
            )
        except Exception as e:
            print(f"Error uploading {storage_path} to Supabase Storage: {e}")

def get_component_files(slug: str, files_manifest: list[str]) -> dict[str, str]:
    """
    Downloads source files from private Supabase Storage bucket for authorized requests.
    """
    if not supabase_client:
        return {}

    result = {}
    for filename in files_manifest:
        storage_path = f"{slug}/{filename}"
        try:
            data = supabase_client.storage.from_(BUCKET_NAME).download(storage_path)
            result[filename] = data.decode("utf-8")
        except Exception as e:
            print(f"Error downloading {storage_path} from Supabase Storage: {e}")
    return result

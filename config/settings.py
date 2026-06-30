import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    firecrawl_api_key: str = os.getenv("FIRECRAWL_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_anon_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "512"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "64"))


settings = Settings()

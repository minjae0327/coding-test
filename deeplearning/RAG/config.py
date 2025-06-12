"""----------------------------------------------------
config.py  – centralised settings (env‑vars > defaults)
----------------------------------------------------"""
import os

REDIS_URL         = os.getenv("REDIS_URL", "redis://localhost:6379/0")
UPLOAD_FOLDER     = os.getenv("UPLOAD_FOLDER", "uploads")
CACHE_FOLDER      = os.getenv("CACHE_FOLDER", "rag_cache")
ALLOWED_LLM       = {"ollama": "gemma3:4b", "openai": "gpt-4o-mini"}
DEFAULT_LLM_KEY   = os.getenv("DEFAULT_LLM", "ollama")  # "ollama"|"openai"

for _dir in (UPLOAD_FOLDER, CACHE_FOLDER):
    os.makedirs(_dir, exist_ok=True)
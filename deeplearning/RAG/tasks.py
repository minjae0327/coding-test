"""----------------------------------------------------
tasks.py – Celery background job for heavy‑weight build
----------------------------------------------------"""
from __future__ import annotations
import os, pickle, gc
from celery import Celery
from celery.utils.log import get_task_logger
from pathlib import Path
from config import REDIS_URL, CACHE_FOLDER, ALLOWED_LLM, DEFAULT_LLM_KEY
from run_rag import RAGApp

celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)
log = get_task_logger(__name__)

@celery.task(bind=True)
def build_rag_task(self, pdf_path: str, session_id: str, llm_key: str | None = None) -> str:
    """Parse PDF → build FAISS & reranker → stash to disk.
    Returns path to pickled file that Flask can later load."""
    llm_key = llm_key or DEFAULT_LLM_KEY
    llm_name = ALLOWED_LLM.get(llm_key, ALLOWED_LLM[DEFAULT_LLM_KEY])
    log.info(f"[T:{self.request.id}] Building RAG for session {session_id} with LLM={llm_name} …")

    rag = RAGApp(pdf_path=pdf_path, llm_name=llm_name)
    cache_dir = Path(CACHE_FOLDER) / session_id
    cache_dir.mkdir(parents=True, exist_ok=True)
    dump_path = cache_dir / "rag.pkl"
    # dill can serialise torch modules; fallback to pickle if dill not installed
    try:
        import dill as _pkl
    except ImportError:
        _pkl = pickle
    with open(dump_path, "wb") as f:
        _pkl.dump(rag, f)
    log.info(f"[T:{self.request.id}] RAG built → {dump_path}")
    # Explicitly free GPU mem inside worker after serialisation
    del rag
    gc.collect()
    return str(dump_path)
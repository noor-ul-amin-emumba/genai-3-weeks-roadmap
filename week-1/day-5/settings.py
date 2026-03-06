"""Configuration for the Day-5 LangChain RAG project.

This module keeps all tunable values in one place so beginners can
experiment without hunting across multiple files.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

# Load environment variables from day-5/.env if it exists.
load_dotenv(ENV_PATH)

# File + persistence paths
RESUME_FILE = os.getenv("RESUME_FILE", "Noor_Ul_Amin_CV.pdf")
RESUME_PATH = BASE_DIR / RESUME_FILE
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = os.getenv("RAG_COLLECTION", "profile-rag")

# Model choices
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Chunking + retrieval settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
TOP_K = int(os.getenv("TOP_K", "4"))

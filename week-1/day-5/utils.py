"""Small helper utilities used by the RAG scripts."""

from __future__ import annotations

from pathlib import Path


def require_file(path: Path) -> None:
    """Raise a clear error if an expected file does not exist."""
    if not path.exists():
        raise FileNotFoundError(
            f"Expected file not found: {path}\n"
            "Update RESUME_FILE in .env or place the file in day-5."
        )

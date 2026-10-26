"""
Database configuration helpers.
"""
from __future__ import annotations
from pathlib import Path
from app.core.config.settings import get_settings

def get_database_url() -> str:
    """Get the configured database URL, resolving relative SQLite paths to backend/."""
    url = get_settings().DATABASE_URL
    if "sqlite+aiosqlite:///" in url and not url.startswith("sqlite+aiosqlite:////"):
        # Handle relative paths like sqlite+aiosqlite:///./cliniq.db or sqlite+aiosqlite:///cliniq.db
        sub = url.replace("sqlite+aiosqlite:///", "")
        if sub.startswith("./"):
            sub = sub[2:]
        backend_dir = Path(__file__).resolve().parents[3]
        db_path = (backend_dir / sub).resolve()
        return f"sqlite+aiosqlite:///{db_path.as_posix()}"
    return url

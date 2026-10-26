"""
General helper utilities.
"""
from __future__ import annotations
import uuid
import re
from typing import Any
from datetime import datetime, timezone

def utcnow() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)

def generate_uuid() -> str:
    """Generate a string UUID."""
    return str(uuid.uuid4())

def slugify(text: str) -> str:
    """Convert text to a slugified string."""
    return re.sub(r'[^\w\-]', '', text.lower().replace(' ', '-'))

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length."""
    return text[:max_length] + '...' if len(text) > max_length else text

def format_dt(dt: Any, fmt: str = "%Y-%m-%d") -> str:
    """Safely format a datetime or date or ISO string to a given format without throwing AttributeError."""
    if dt is None:
        return ""
    if hasattr(dt, "strftime"):
        return dt.strftime(fmt)
    s = str(dt).strip()
    if not s:
        return ""
    if fmt == "%Y-%m-%d" and len(s) >= 10:
        return s[:10]
    try:
        clean_s = s.replace("Z", "+00:00").split(".")[0]
        d_obj = datetime.fromisoformat(clean_s)
        return d_obj.strftime(fmt)
    except Exception:
        return s[:10] if len(s) >= 10 else s

def parse_dt(dt: Any) -> datetime:
    """Safely parse a datetime object or string to a datetime object."""
    if dt is None:
        return datetime.now(timezone.utc)
    if isinstance(dt, datetime):
        return dt
    s = str(dt).strip()
    try:
        clean_s = s.replace("Z", "+00:00").split(".")[0]
        return datetime.fromisoformat(clean_s)
    except Exception:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(s[:19], fmt)
            except Exception:
                pass
    return datetime.now(timezone.utc)

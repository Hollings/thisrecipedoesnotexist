"""Utility helpers for the Python backend."""
from __future__ import annotations

import os
import random
import re
from datetime import datetime, timedelta
from typing import Iterable

import bcrypt

# Re-use the existing hashed password from the Laravel app so API clients keep working.
PASSWORD_HASH = os.getenv(
    "TRDNE_ADMIN_PASSWORD_HASH",
    "$2y$10$y/TJW50eL4loeni.h7ddv.isQZ8SDutOuhst8XGyDm2cuCxRHpb1q",
)

_BOT_USER_AGENT_RE = re.compile(r"bot|crawl|slurp|spider|mediapartners", re.IGNORECASE)
_VOWELS = "aeiou"


def is_search_bot(user_agent: str | None) -> bool:
    """Rudimentary crawler detection to avoid incrementing view counters."""
    return bool(user_agent and _BOT_USER_AGENT_RE.search(user_agent))


def humanize_timespan(moment: datetime | None, reference: datetime | None = None) -> str:
    """Produce a small "diff for humans" string similar to Carbon."""
    if moment is None:
        return "unknown"
    reference = reference or datetime.utcnow()
    delta: timedelta = reference - moment
    seconds = int(delta.total_seconds())
    if seconds < 0:
        return "in the future"
    intervals: list[tuple[str, int]] = [
        ("year", 60 * 60 * 24 * 365),
        ("month", 60 * 60 * 24 * 30),
        ("day", 60 * 60 * 24),
        ("hour", 60 * 60),
        ("minute", 60),
        ("second", 1),
    ]
    for label, size in intervals:
        count = seconds // size
        if count:
            suffix = "s" if count != 1 else ""
            return f"{count} {label}{suffix} ago"
    return "just now"


def verify_password(raw_password: str) -> bool:
    """Check a plaintext password against the stored bcrypt hash."""
    try:
        return bcrypt.checkpw(raw_password.encode("utf-8"), PASSWORD_HASH.encode("utf-8"))
    except ValueError:
        # bcrypt raises ValueError if the stored hash format is invalid
        return False


def anonymise_username(name: str) -> str:
    """Substitute vowels to mimic the original randomisation behaviour."""
    def _swap(ch: str) -> str:
        if ch.lower() in _VOWELS:
            replacement = random.choice(_VOWELS)
            return replacement.upper() if ch.isupper() else replacement
        return ch

    return "".join(_swap(ch) for ch in name)


def choice_or_none(items: Iterable) -> object | None:
    """Return a random item or None if the iterable is empty."""
    items = list(items)
    return random.choice(items) if items else None

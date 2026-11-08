"""Shared date helper: the cookbook's "today" is always the owner's local date (US Eastern)."""
from datetime import datetime
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo('America/New_York')


def today_iso() -> str:
    return datetime.now(TIMEZONE).date().isoformat()

"""Shared utils."""
from datetime import datetime, timedelta
from typing import Optional


def birthdate_to_age(birth_date: datetime, session_date: datetime) -> Optional[int]:
    """Calculates age in seconds given birthday and date of session."""
    age = session_date.date() - birth_date.date()
    age_in_seconds = age / timedelta(seconds=1)
    if age_in_seconds < 0:
        return None

    return int(age_in_seconds)

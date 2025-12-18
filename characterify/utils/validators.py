from __future__ import annotations

import re


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match((email or "").strip().lower()))


def validate_password(password: str, min_length: int = 8) -> tuple[bool, str]:
    if not password:
        return False, "Password tidak boleh kosong."
    if len(password) < min_length:
        return False, f"Password minimal {min_length} karakter."
    # lightweight checks: at least one digit, one letter
    has_digit = any(ch.isdigit() for ch in password)
    has_alpha = any(ch.isalpha() for ch in password)
    if not (has_digit and has_alpha):
        return False, "Password sebaiknya mengandung huruf dan angka."
    return True, ""

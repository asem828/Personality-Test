from __future__ import annotations

import base64
import hashlib
import hmac
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from characterify.db.database import Database
from characterify.db.repositories import UserRepository
from characterify.services.security import SecurityService
from characterify.utils.validators import is_valid_email, validate_password


class AuthError(Exception):
    pass


@dataclass
class AuthService:
    """Authentication + account utilities."""

    db: Database
    security: SecurityService

    def __post_init__(self) -> None:
        self.users = UserRepository(self.db)

    @staticmethod
    def _pbkdf2(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)

    def hash_password(self, password: str) -> tuple[str, str]:
        salt = os.urandom(16)
        dk = self._pbkdf2(password, salt)
        return base64.b64encode(dk).decode("utf-8"), base64.b64encode(salt).decode("utf-8")

    def verify_password(self, password: str, password_hash: str, password_salt: str) -> bool:
        try:
            salt = base64.b64decode(password_salt.encode("utf-8"))
            expected = base64.b64decode(password_hash.encode("utf-8"))
        except Exception:
            return False
        actual = self._pbkdf2(password, salt)
        return hmac.compare_digest(actual, expected)

    def register(self, name: str, email: str, password: str, confirm_password: str) -> int:
        name = (name or "").strip()
        email = (email or "").strip().lower()

        if not name:
            raise AuthError("Nama tidak boleh kosong.")
        if not is_valid_email(email):
            raise AuthError("Format email tidak valid.")

        ok, msg = validate_password(password)
        if not ok:
            raise AuthError(msg)
        if password != confirm_password:
            raise AuthError("Konfirmasi password tidak sama.")

        if self.users.get_by_email(email):
            raise AuthError("Email sudah terdaftar. Silakan login.")

        pw_hash, pw_salt = self.hash_password(password)
        user_id = self.users.create(name=name, email=email, password_hash=pw_hash, password_salt=pw_salt)
        return user_id

    def login(self, email: str, password: str) -> int:
        email = (email or "").strip().lower()
        if not is_valid_email(email):
            raise AuthError("Email tidak valid.")
        row = self.users.get_by_email(email)
        if not row:
            raise AuthError("Akun tidak ditemukan.")
        if not self.verify_password(password, row["password_hash"], row["password_salt"]):
            raise AuthError("Password salah.")
        return int(row["id"])

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        return self.users.get_by_id(user_id)

    def update_profile(self, user_id: int, name: str, email: str) -> None:
        name = (name or "").strip()
        email = (email or "").strip().lower()
        if not name:
            raise AuthError("Nama tidak boleh kosong.")
        if not is_valid_email(email):
            raise AuthError("Format email tidak valid.")
        # email uniqueness check (except self)
        existing = self.users.get_by_email(email)
        if existing and int(existing["id"]) != int(user_id):
            raise AuthError("Email sudah digunakan oleh akun lain.")
        self.users.update_profile(user_id=user_id, name=name, email=email)

    def update_password(self, user_id: int, current_password: str, new_password: str, confirm: str) -> None:
        row = self.users.get_by_id(user_id)
        if not row:
            raise AuthError("User tidak ditemukan.")
        if not self.verify_password(current_password, row["password_hash"], row["password_salt"]):
            raise AuthError("Password saat ini salah.")
        ok, msg = validate_password(new_password)
        if not ok:
            raise AuthError(msg)
        if new_password != confirm:
            raise AuthError("Konfirmasi password baru tidak sama.")
        pw_hash, pw_salt = self.hash_password(new_password)
        self.users.update_password(user_id=user_id, password_hash=pw_hash, password_salt=pw_salt)

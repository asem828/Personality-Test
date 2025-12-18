from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from characterify.utils.paths import AppPaths


@dataclass
class SecurityService:
    """Handles lightweight local encryption for sensitive fields (e.g., local secrets).

    Uses Fernet symmetric encryption. The key is stored locally in the user's
    home directory (offline-first).
    """

    paths: AppPaths

    def _get_fernet(self):
        try:
            from cryptography.fernet import Fernet
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "cryptography belum terpasang. Install: pip install cryptography"
            ) from exc

        key = self.get_or_create_key()
        return Fernet(key)

    def get_or_create_key(self) -> bytes:
        if self.paths.key_path.exists():
            return self.paths.key_path.read_bytes()

        try:
            from cryptography.fernet import Fernet
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "cryptography belum terpasang. Install: pip install cryptography"
            ) from exc

        key = Fernet.generate_key()
        self.paths.key_path.write_bytes(key)
        return key

    def encrypt(self, plaintext: str) -> str:
        if not plaintext:
            return ""
        f = self._get_fernet()
        token: bytes = f.encrypt(plaintext.encode("utf-8"))
        return token.decode("utf-8")

    def decrypt(self, token: str) -> str:
        if not token:
            return ""
        f = self._get_fernet()
        plaintext: bytes = f.decrypt(token.encode("utf-8"))
        return plaintext.decode("utf-8")

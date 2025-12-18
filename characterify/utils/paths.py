from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppPaths:
    """Common file-system paths used by the application."""

    base_dir: Path = Path.home() / ".characterify"

    @property
    def db_path(self) -> Path:
        return self.base_dir / "characterify.db"

    @property
    def logs_dir(self) -> Path:
        return self.base_dir / "logs"

    @property
    def exports_dir(self) -> Path:
        return self.base_dir / "exports"

    @property
    def temp_dir(self) -> Path:
        return self.base_dir / "tmp"

    @property
    def key_path(self) -> Path:
        return self.base_dir / "key.key"

    def ensure(self) -> None:
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

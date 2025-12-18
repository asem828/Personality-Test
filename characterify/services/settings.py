from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from characterify.db.database import Database
from characterify.db.repositories import UserRepository
from characterify.services.security import SecurityService
from characterify.utils.paths import AppPaths


DEFAULT_SETTINGS: Dict[str, Any] = {
    "theme": "dark",
    "language": "id",
    "notifications": {
        "retest_reminder_days": 30,
        "enabled": False,
    },
}


@dataclass
class SettingsService:
    db: Database
    security: SecurityService
    paths: AppPaths

    def __post_init__(self) -> None:
        self.users = UserRepository(self.db)
        self._global_config_path = self.paths.base_dir / "app_config.json"

    # ---------------------------
    # Global config (pre-login)
    # ---------------------------
    def load_global_config(self) -> Dict[str, Any]:
        if not self._global_config_path.exists():
            return {"theme": "dark", "language": "id"}
        try:
            return json.loads(self._global_config_path.read_text(encoding="utf-8"))
        except Exception:
            return {"theme": "dark", "language": "id"}

    def save_global_config(self, config: Dict[str, Any]) -> None:
        try:
            self._global_config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    # ---------------------------
    # Per-user settings
    # ---------------------------
    def get_user_settings(self, user_id: int) -> Dict[str, Any]:
        row = self.users.get_by_id(user_id)
        if not row:
            return dict(DEFAULT_SETTINGS)
        raw = row.get("settings_json") or "{}"
        try:
            data = json.loads(raw)
        except Exception:
            data = {}
        merged = dict(DEFAULT_SETTINGS)
        # deep-ish merge
        for k, v in data.items():
            if isinstance(v, dict) and isinstance(merged.get(k), dict):
                merged[k] = {**merged[k], **v}
            else:
                merged[k] = v
        return merged

    def save_user_settings(self, user_id: int, settings: Dict[str, Any]) -> None:
        raw = json.dumps(settings, ensure_ascii=False)
        self.users.update_settings_json(user_id=user_id, settings_json=raw)

    def get_theme(self, user_id: Optional[int] = None) -> str:
        if user_id:
            return self.get_user_settings(user_id).get("theme", "dark")
        return self.load_global_config().get("theme", "dark")

    def set_theme(self, user_id: Optional[int], theme: str) -> None:
        theme = theme if theme in ("dark", "light") else "dark"
        if user_id:
            settings = self.get_user_settings(user_id)
            settings["theme"] = theme
            self.save_user_settings(user_id, settings)
        global_cfg = self.load_global_config()
        global_cfg["theme"] = theme
        self.save_global_config(global_cfg)

    def get_language(self, user_id: Optional[int] = None) -> str:
        if user_id:
            return self.get_user_settings(user_id).get("language", "id")
        return self.load_global_config().get("language", "id")

    def set_language(self, user_id: Optional[int], lang: str) -> None:
        lang = lang if lang in ("id", "en") else "id"
        if user_id:
            settings = self.get_user_settings(user_id)
            settings["language"] = lang
            self.save_user_settings(user_id, settings)
        global_cfg = self.load_global_config()
        global_cfg["language"] = lang
        self.save_global_config(global_cfg)

    # ---------------------------
    # Theme application
    # ---------------------------
    def apply_theme(self, app, theme: str) -> None:
        """Load QSS and apply to QApplication."""
        qss_file = self._get_qss_path(theme)
        if qss_file and qss_file.exists():
            qss = qss_file.read_text(encoding="utf-8")
            app.setStyleSheet(qss)
        else:
            app.setStyleSheet("")

    def _get_qss_path(self, theme: str) -> Optional[Path]:
        here = Path(__file__).resolve()
        # .../characterify/services/settings.py -> .../characterify/assets/qss
        assets_qss = here.parent.parent / "assets" / "qss"
        if theme == "light":
            return assets_qss / "light.qss"
        return assets_qss / "dark.qss"

    # ---------------------------
    # Language application (optional QTranslator)
    # ---------------------------
    def apply_language(self, app, lang: str) -> None:
        """Install Qt translator if a compiled `.qm` exists.

        Notes:
            The UI in this project primarily uses explicit `t(ctx, id, en)`
            (see `characterify/utils/i18n.py`) so language switching works
            even without Qt Linguist tools.

            If you compile the provided `.ts` into a `.qm`, this method will
            load it so you can also translate Qt native strings.
        """

        lang = lang if lang in ("id", "en") else "id"
        try:
            from PySide6.QtCore import QTranslator
        except Exception:
            return

        # Keep translator alive on this service instance
        if not hasattr(self, "_translator"):
            self._translator = None  # type: ignore[attr-defined]

        # Remove existing
        try:
            if self._translator is not None:  # type: ignore[attr-defined]
                app.removeTranslator(self._translator)  # type: ignore[attr-defined]
        except Exception:
            pass

        if lang != "en":
            self._translator = None  # type: ignore[attr-defined]
            return

        qm = (Path(__file__).resolve().parent.parent / "assets" / "i18n" / "characterify_en.qm")
        if not qm.exists():
            self._translator = None  # type: ignore[attr-defined]
            return

        tr = QTranslator()
        if tr.load(str(qm)):
            try:
                app.installTranslator(tr)
                self._translator = tr  # type: ignore[attr-defined]
            except Exception:
                self._translator = None  # type: ignore[attr-defined]
        else:
            self._translator = None  # type: ignore[attr-defined]

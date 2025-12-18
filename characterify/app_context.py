from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from characterify.db.database import Database
from characterify.services.auth import AuthService
from characterify.services.pdf_report import PdfReportService
from characterify.services.scoring import ScoringService
from characterify.services.security import SecurityService
from characterify.services.settings import SettingsService


@dataclass
class AppContext:
    """Holds app-wide state and services.

    The context is created once in `characterify.main` and passed to the UI.
    """

    db: Database
    auth: AuthService
    scoring: ScoringService
    pdf: PdfReportService
    security: SecurityService
    settings: SettingsService

    current_user_id: Optional[int] = None

    def is_authenticated(self) -> bool:
        return self.current_user_id is not None

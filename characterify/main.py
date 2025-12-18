from __future__ import annotations

import os
import sys


def main() -> int:
    """App entrypoint. Returns exit code."""

    try:
        from PySide6.QtGui import QFont
        from PySide6.QtWidgets import QApplication
    except Exception as exc:  # pragma: no cover
        print("PySide6 belum terpasang. Install dulu:")
        print("  pip install -r requirements.txt")
        print(f"\nError: {exc}")
        return 1

    from characterify.app_context import AppContext
    from characterify.db.database import Database
    from characterify.services.auth import AuthService
    from characterify.services.pdf_report import PdfReportService
    from characterify.services.scoring import ScoringService
    from characterify.services.security import SecurityService
    from characterify.services.settings import SettingsService
    from characterify.services.telemetry import TelemetryService
    from characterify.ui.main_window import MainWindow
    from characterify.utils.paths import AppPaths

    # High DPI
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
    os.environ.setdefault("QT_SCALE_FACTOR_ROUNDING_POLICY", "PassThrough")

    app = QApplication(sys.argv)
    app.setApplicationName("Characterify")

    # Font (fallback if not available)
    app.setFont(QFont("Segoe UI", 10))

    paths = AppPaths()
    paths.ensure()

    telemetry = TelemetryService(paths)
    telemetry.install_exception_hook()

    db = Database(paths.db_path)
    db.initialize()

    security = SecurityService(paths)
    settings = SettingsService(db=db, security=security, paths=paths)

    auth = AuthService(db=db, security=security)
    scoring = ScoringService()
    pdf = PdfReportService(paths=paths)
    ctx = AppContext(
        db=db,
        auth=auth,
        scoring=scoring,
        pdf=pdf,
        security=security,
        settings=settings,
    )

    # Apply global preferences (pre-login)
    global_cfg = settings.load_global_config()
    settings.apply_theme(app, theme=str(global_cfg.get("theme", "dark")))
    settings.apply_language(app, lang=str(global_cfg.get("language", "id")))

    window = MainWindow(ctx=ctx, telemetry=telemetry)
    window.resize(1240, 760)
    window.show()

    return app.exec()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

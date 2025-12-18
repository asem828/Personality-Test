from __future__ import annotations

import logging
import sys
import traceback
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler

from characterify.utils.paths import AppPaths


@dataclass
class TelemetryService:
    """Local-only telemetry: structured logging + friendly error dialog.

    The app is offline-first; we only write logs to a local file.
    """

    paths: AppPaths

    def __post_init__(self) -> None:
        self.logger = logging.getLogger("characterify")
        self.logger.setLevel(logging.INFO)

        log_file = self.paths.logs_dir / "app.log"
        handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        fmt = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)

        if not any(isinstance(h, RotatingFileHandler) for h in self.logger.handlers):
            self.logger.addHandler(handler)

        # Also log to stderr during development
        stream = logging.StreamHandler()
        stream.setFormatter(fmt)
        if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            self.logger.addHandler(stream)

    def install_exception_hook(self) -> None:
        """Install a global exception hook that logs and shows an error dialog."""

        def _hook(exc_type, exc, tb):
            try:
                self.logger.error("Unhandled exception", exc_info=(exc_type, exc, tb))
            except Exception:
                pass

            # Try to show a GUI dialog if Qt is available
            try:
                from PySide6.QtWidgets import QMessageBox

                msg = "\n".join(traceback.format_exception(exc_type, exc, tb))
                box = QMessageBox()
                box.setIcon(QMessageBox.Critical)
                box.setWindowTitle("Characterify - Error")
                box.setText("Terjadi error yang tidak terduga. Detail sudah dicatat di log.")
                box.setDetailedText(msg)
                box.exec()
            except Exception:
                # Fallback: print to stderr
                traceback.print_exception(exc_type, exc, tb)

        sys.excepthook = _hook

    def log_event(self, name: str, **data) -> None:
        payload = ", ".join([f"{k}={v}" for k, v in data.items()])
        self.logger.info(f"EVENT {name} | {payload}")

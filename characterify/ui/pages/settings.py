from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from characterify.app_context import AppContext
from characterify.db.repositories import TestHistoryRepository, TestSessionRepository
from characterify.services.history import HistoryService
from characterify.ui.widgets.common import Card, H1, H2, Muted
from characterify.ui.widgets.dialogs import ask_yes_no, show_error, show_info


class SettingsPage(QWidget):
    def __init__(self, ctx: AppContext, on_theme_changed: Callable[[str], None]) -> None:
        super().__init__()
        self.ctx = ctx
        self.on_theme_changed = on_theme_changed

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        root.addWidget(H1("Settings"))
        root.addWidget(Muted("Tema, bahasa, dan pengelolaan data."))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        root.addWidget(scroll, 1)

        body = QWidget()
        scroll.setWidget(body)
        layout = QVBoxLayout(body)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Appearance
        appearance = Card()
        appearance.body.addWidget(H2("Appearance"))
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignTop)
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(10)

        self.theme = QComboBox()
        self.theme.addItems(["dark", "light"])
        self.theme.currentTextChanged.connect(self._theme_changed)
        form.addRow("Theme", self.theme)

        self.lang = QComboBox()
        self.lang.addItems(["id", "en"])
        self.lang.currentTextChanged.connect(self._lang_changed)
        form.addRow("Language", self.lang)

        appearance.body.addLayout(form)
        layout.addWidget(appearance)

        # Data management
        data = Card()
        data.body.addWidget(H2("Data"))
        data.body.addWidget(Muted("Export atau bersihkan data history di perangkat ini."))

        row2 = QHBoxLayout()
        btn_json = QPushButton("Export History JSON")
        btn_json.clicked.connect(self._export_json)
        row2.addWidget(btn_json)

        btn_csv = QPushButton("Export History CSV")
        btn_csv.clicked.connect(self._export_csv)
        row2.addWidget(btn_csv)

        row2.addStretch(1)
        data.body.addLayout(row2)

        row3 = QHBoxLayout()
        btn_clear = QPushButton("Clear History")
        btn_clear.setObjectName("DangerButton")
        btn_clear.clicked.connect(self._clear_history)
        row3.addWidget(btn_clear)

        btn_clear_sessions = QPushButton("Clear Saved Sessions")
        btn_clear_sessions.clicked.connect(self._clear_sessions)
        row3.addWidget(btn_clear_sessions)

        row3.addStretch(1)
        data.body.addLayout(row3)
        layout.addWidget(data)

        # Notifications (stored only)
        notif = Card()
        notif.body.addWidget(H2("Notifikasi (Offline)"))
        notif.body.addWidget(Muted("Pengingat tes ulang disimpan sebagai preferensi. (Tidak mengirim notifikasi ke server)"))

        form3 = QFormLayout()
        self.notif_enabled = QCheckBox("Aktifkan pengingat")
        form3.addRow("", self.notif_enabled)

        self.retest_days = QSpinBox()
        self.retest_days.setRange(7, 365)
        self.retest_days.setValue(30)
        form3.addRow("Ingatkan setiap (hari)", self.retest_days)

        notif.body.addLayout(form3)

        btn_save_notif = QPushButton("Simpan Preferensi")
        btn_save_notif.setObjectName("PrimaryButton")
        btn_save_notif.clicked.connect(self._save_notif)
        notif.body.addWidget(btn_save_notif)
        layout.addWidget(notif)

        layout.addStretch(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._load()

    def _require_user(self) -> Optional[int]:
        if not self.ctx.current_user_id:
            show_error(self, "Not Logged In", "Silakan login.")
            return None
        return self.ctx.current_user_id

    def _load(self) -> None:
        uid = self.ctx.current_user_id
        theme = self.ctx.settings.get_theme(uid)
        self.theme.setCurrentText(theme)

        lang = self.ctx.settings.get_language(uid)
        self.lang.setCurrentText(lang)

        if uid:
            settings = self.ctx.settings.get_user_settings(uid)
            notif = settings.get("notifications", {})
            self.notif_enabled.setChecked(bool(notif.get("enabled", False)))
            self.retest_days.setValue(int(notif.get("retest_reminder_days", 30)))

    # --- handlers
    def _theme_changed(self, theme: str) -> None:
        uid = self.ctx.current_user_id
        self.ctx.settings.set_theme(uid, theme)
        self.on_theme_changed(theme)

    def _lang_changed(self, lang: str) -> None:
        uid = self.ctx.current_user_id
        self.ctx.settings.set_language(uid, lang)
        # Apply optional Qt translator (if `.qm` exists)
        try:
            from PySide6.QtWidgets import QApplication
            self.ctx.settings.apply_language(QApplication.instance(), lang=lang)
        except Exception:
            pass

        # Refresh visible texts
        try:
            w = self.window()
            if hasattr(w, "retranslate_ui"):
                w.retranslate_ui()  # type: ignore
        except Exception:
            pass

        show_info(self, "Language", "Bahasa tersimpan." if lang != "en" else "Language saved.")

    def _export_json(self) -> None:
        uid = self._require_user()
        if not uid:
            return
        hs = HistoryService(self.ctx.db, self.ctx.settings.paths)
        path = hs.export_json(uid)
        show_info(self, "Export JSON", f"File tersimpan di:\n{path}")

    def _export_csv(self) -> None:
        uid = self._require_user()
        if not uid:
            return
        hs = HistoryService(self.ctx.db, self.ctx.settings.paths)
        path = hs.export_csv(uid)
        show_info(self, "Export CSV", f"File tersimpan di:\n{path}")

    def _clear_history(self) -> None:
        uid = self._require_user()
        if not uid:
            return
        if not ask_yes_no(self, "Clear History", "Hapus semua history tes? Tindakan ini tidak bisa dibatalkan."):
            return
        TestHistoryRepository(self.ctx.db).clear_all(uid)
        show_info(self, "Clear History", "History berhasil dihapus.")

    def _clear_sessions(self) -> None:
        uid = self._require_user()
        if not uid:
            return
        if not ask_yes_no(self, "Clear Sessions", "Hapus semua saved session (progress) tes?"):
            return
        # Clear sessions for each test type
        repo = TestSessionRepository(self.ctx.db)
        for t in self.ctx.scoring.get_tests():
            repo.delete(uid, t.id)
        show_info(self, "Clear Sessions", "Saved sessions berhasil dihapus.")

    def _save_notif(self) -> None:
        uid = self._require_user()
        if not uid:
            return
        settings = self.ctx.settings.get_user_settings(uid)
        settings["notifications"] = {
            "enabled": self.notif_enabled.isChecked(),
            "retest_reminder_days": self.retest_days.value(),
        }
        self.ctx.settings.save_user_settings(uid, settings)
        show_info(self, "Notifikasi", "Preferensi tersimpan.")

from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from characterify.app_context import AppContext
from characterify.ui.widgets.common import Card, H1, H2, Muted
from characterify.ui.widgets.dialogs import show_error, show_info


class AccountSettingsPage(QWidget):
    def __init__(self, ctx: AppContext, on_back: Callable[[], None]) -> None:
        super().__init__()
        self.ctx = ctx
        self.on_back = on_back

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        header = QHBoxLayout()
        header.addWidget(H1("Account Settings"))
        header.addStretch(1)
        btn_back = QPushButton("← Back")
        btn_back.clicked.connect(self.on_back)
        header.addWidget(btn_back)
        root.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        root.addWidget(scroll, 1)

        body = QWidget()
        scroll.setWidget(body)
        layout = QVBoxLayout(body)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Profile
        profile = Card()
        profile.body.addWidget(H2("Profil"))
        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(10)

        self.name = QLineEdit()
        form.addRow("Nama", self.name)

        self.email = QLineEdit()
        form.addRow("Email", self.email)

        profile.body.addLayout(form)

        btn_save = QPushButton("Simpan Profil")
        btn_save.setObjectName("PrimaryButton")
        btn_save.clicked.connect(self._save_profile)
        profile.body.addWidget(btn_save)
        layout.addWidget(profile)

        # Password
        pw = Card()
        pw.body.addWidget(H2("Ganti Password"))
        form2 = QFormLayout()
        form2.setHorizontalSpacing(18)
        form2.setVerticalSpacing(10)

        self.current_pw = QLineEdit()
        self.current_pw.setEchoMode(QLineEdit.Password)
        form2.addRow("Password saat ini", self.current_pw)

        self.new_pw = QLineEdit()
        self.new_pw.setEchoMode(QLineEdit.Password)
        form2.addRow("Password baru", self.new_pw)

        self.confirm_pw = QLineEdit()
        self.confirm_pw.setEchoMode(QLineEdit.Password)
        form2.addRow("Konfirmasi", self.confirm_pw)

        pw.body.addLayout(form2)

        btn_save_pw = QPushButton("Update Password")
        btn_save_pw.setObjectName("PrimaryButton")
        btn_save_pw.clicked.connect(self._save_password)
        pw.body.addWidget(btn_save_pw)

        layout.addWidget(pw)
        layout.addStretch(1)

    def load(self) -> None:
        uid = self.ctx.current_user_id
        if not uid:
            return
        user = self.ctx.auth.get_user(uid) or {}
        self.name.setText(user.get("name", ""))
        self.email.setText(user.get("email", ""))

    def _save_profile(self) -> None:
        uid = self.ctx.current_user_id
        if not uid:
            return
        try:
            self.ctx.auth.update_profile(uid, self.name.text(), self.email.text())
            show_info(self, "Profil", "Profil berhasil diperbarui.")
        except Exception as exc:
            show_error(self, "Gagal", str(exc))

    def _save_password(self) -> None:
        uid = self.ctx.current_user_id
        if not uid:
            return
        try:
            self.ctx.auth.update_password(uid, self.current_pw.text(), self.new_pw.text(), self.confirm_pw.text())
            show_info(self, "Password", "Password berhasil diperbarui.")
            self.current_pw.clear()
            self.new_pw.clear()
            self.confirm_pw.clear()
        except Exception as exc:
            show_error(self, "Gagal", str(exc))

from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from characterify.app_context import AppContext
from characterify.ui.widgets.common import Card, H1, Muted
from characterify.ui.widgets.dialogs import show_error, show_info


class LoginPage(QWidget):
    def __init__(self, ctx: AppContext, on_login: Callable[[int], None], go_register: Callable[[], None]) -> None:
        super().__init__()
        self.ctx = ctx
        self.on_login = on_login
        self.go_register = go_register

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        card = Card()
        card.setFixedWidth(440)
        root.addWidget(card, alignment=Qt.AlignCenter)

        card.body.addWidget(H1("Login"))
        card.body.addWidget(Muted("Masuk untuk melihat dashboard dan history tes Anda."))

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        card.body.addWidget(self.email)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        card.body.addWidget(self.password)

        self.btn_login = QPushButton("Login")
        self.btn_login.setObjectName("PrimaryButton")
        self.btn_login.clicked.connect(self._login)
        card.body.addWidget(self.btn_login)

        row = QHBoxLayout()
        row.addWidget(Muted("Belum punya akun?"))
        btn = QPushButton("Register")
        btn.setFlat(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.go_register)
        row.addWidget(btn)
        row.addStretch(1)
        card.body.addLayout(row)

    def _login(self) -> None:
        try:
            user_id = self.ctx.auth.login(self.email.text(), self.password.text())
            show_info(self, "Login Berhasil", "Selamat datang di Characterify!")
            self.on_login(user_id)
        except Exception as exc:
            show_error(self, "Login Gagal", str(exc))


class RegisterPage(QWidget):
    def __init__(self, ctx: AppContext, go_login: Callable[[], None]) -> None:
        super().__init__()
        self.ctx = ctx
        self.go_login = go_login

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        card = Card()
        card.setFixedWidth(520)
        root.addWidget(card, alignment=Qt.AlignCenter)

        card.body.addWidget(H1("Register"))
        card.body.addWidget(Muted("Buat akun untuk menyimpan hasil tes dan bookmark artikel."))

        self.name = QLineEdit()
        self.name.setPlaceholderText("Nama")
        card.body.addWidget(self.name)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        card.body.addWidget(self.email)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password (min 8, huruf + angka)")
        self.password.setEchoMode(QLineEdit.Password)
        card.body.addWidget(self.password)

        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText("Konfirmasi Password")
        self.confirm.setEchoMode(QLineEdit.Password)
        card.body.addWidget(self.confirm)

        btn = QPushButton("Buat Akun")
        btn.setObjectName("PrimaryButton")
        btn.clicked.connect(self._register)
        card.body.addWidget(btn)

        row = QHBoxLayout()
        row.addWidget(Muted("Sudah punya akun?"))
        btn2 = QPushButton("Login")
        btn2.setFlat(True)
        btn2.setCursor(Qt.PointingHandCursor)
        btn2.clicked.connect(self.go_login)
        row.addWidget(btn2)
        row.addStretch(1)
        card.body.addLayout(row)

    def _register(self) -> None:
        try:
            _user_id = self.ctx.auth.register(
                self.name.text(), self.email.text(), self.password.text(), self.confirm.text()
            )
            show_info(self, "Register Berhasil", "Akun berhasil dibuat. Silakan login.")
            self.go_login()
        except Exception as exc:
            show_error(self, "Register Gagal", str(exc))

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QMenu, QPushButton, QWidget

from characterify.utils.i18n import t


class TopBar(QFrame):
    logoutRequested = Signal()
    dashboardRequested = Signal()
    accountRequested = Signal()
    searchChanged = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("TopBar")
        self.setFixedHeight(64)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 10, 18, 10)
        layout.setSpacing(12)

        self.title = QLabel("Beranda")
        self.title.setStyleSheet("font-size: 14pt; font-weight: 800;")
        layout.addWidget(self.title)

        layout.addStretch(1)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Cari…")
        self.search.setMaximumWidth(360)
        self.search.textChanged.connect(self.searchChanged.emit)
        layout.addWidget(self.search)

        self.user_button = QPushButton("Akun")
        self.user_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.user_button)

        menu = QMenu(self)
        act_dash = menu.addAction("Dashboard")
        act_account = menu.addAction("Pengaturan Akun")
        menu.addSeparator()
        act_logout = menu.addAction("Keluar")

        act_dash.triggered.connect(self.dashboardRequested.emit)
        act_account.triggered.connect(self.accountRequested.emit)
        act_logout.triggered.connect(self.logoutRequested.emit)

        self.user_button.setMenu(menu)

        # Try to use a modern icon (FontAwesome via qtawesome) if available
        self._apply_user_icon()

        # Initial translation for title/search/menu
        # MainWindow will call retranslate_ui(ctx) after ctx exists / language changes.
        self.retranslate_ui(ctx=None)

    def _apply_user_icon(self) -> None:
        try:
            import qtawesome as qta  # type: ignore
            self.user_button.setIcon(qta.icon("fa5s.user-circle", color="#B3B3B3"))
        except Exception:
            pass

    def retranslate_ui(self, ctx) -> None:
        """Update texts based on current language.

        Args:
            ctx: AppContext (can be None during early init)
        """
        # Placeholder and menu items
        self.search.setPlaceholderText(t(ctx, "Cari…", "Search…") if ctx else "Search…")
        # Menu labels
        m = self.user_button.menu()
        if m:
            acts = m.actions()
            if len(acts) >= 1:
                acts[0].setText(t(ctx, "Dashboard", "Dashboard") if ctx else "Dashboard")
            if len(acts) >= 2:
                acts[1].setText(t(ctx, "Pengaturan Akun", "Account Settings") if ctx else "Account Settings")
            # actions[2] is separator
            if len(acts) >= 4:
                acts[3].setText(t(ctx, "Keluar", "Logout") if ctx else "Logout")

    def set_title(self, title: str) -> None:
        self.title.setText(title)

    def set_user_label(self, label: str) -> None:
        self.user_button.setText(label or "Akun")

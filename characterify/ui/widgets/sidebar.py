from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget


@dataclass(frozen=True)
class NavItem:
    key: str
    label: str
    icon_name: str = ""  # e.g. "fa5s.home"
    emoji_fallback: str = ""


def _qta_icon(icon_name: str, color: str):
    """Return a qtawesome icon, or None if qtawesome is unavailable."""
    if not icon_name:
        return None
    try:
        import qtawesome as qta  # type: ignore
        return qta.icon(icon_name, color=color)
    except Exception:
        return None


class Sidebar(QFrame):
    """Spotify-like left navigation sidebar."""
    navigated = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(240)

        self._buttons: Dict[str, QPushButton] = {}
        self._items: Tuple[List[NavItem], List[NavItem]] = ([], [])
        self._active_key: str = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 16, 14, 16)
        layout.setSpacing(10)

        self.brand = QLabel("Characterify")
        self.brand.setStyleSheet("font-size: 14pt; font-weight: 800;")
        layout.addWidget(self.brand)
        layout.addSpacing(6)

        self.group1_label = QLabel("MENU")
        self.group1_label.setStyleSheet("color: #B3B3B3; font-size: 8.5pt; font-weight: 700;")
        layout.addWidget(self.group1_label)

        self.group1_container = QWidget()
        self._g1_layout = QVBoxLayout(self.group1_container)
        self._g1_layout.setContentsMargins(0, 0, 0, 0)
        self._g1_layout.setSpacing(4)
        layout.addWidget(self.group1_container)

        self.group2_label = QLabel("PREFERENCES")
        self.group2_label.setStyleSheet("color: #B3B3B3; font-size: 8.5pt; font-weight: 700;")
        layout.addWidget(self.group2_label)

        self.group2_container = QWidget()
        self._g2_layout = QVBoxLayout(self.group2_container)
        self._g2_layout.setContentsMargins(0, 0, 0, 0)
        self._g2_layout.setSpacing(4)
        layout.addWidget(self.group2_container)

        layout.addStretch(1)
        self.footer = QLabel("© Characterify")
        self.footer.setStyleSheet("color: #6F6F6F; font-size: 8pt;")
        layout.addWidget(self.footer)

    @property
    def active_key(self) -> str:
        return self._active_key

    def set_items(self, group1: List[NavItem], group2: List[NavItem]) -> None:
        self._items = (list(group1), list(group2))
        self._rebuild_buttons()

    def _rebuild_buttons(self) -> None:
        # Clear existing
        for lay in (self._g1_layout, self._g2_layout):
            while lay.count():
                it = lay.takeAt(0)
                w = it.widget()
                if w:
                    w.deleteLater()

        self._buttons.clear()

        g1, g2 = self._items
        for item in g1:
            self._add_button(self._g1_layout, item)
        for item in g2:
            self._add_button(self._g2_layout, item)

        if self._active_key:
            self.set_active(self._active_key)

    def _add_button(self, layout: QVBoxLayout, item: NavItem) -> None:
        icon = _qta_icon(item.icon_name, color="#B3B3B3")
        text = item.label
        if icon is None and item.emoji_fallback:
            text = f"{item.emoji_fallback} {item.label}".strip()

        btn = QPushButton(text)
        btn.setObjectName("NavButton")
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setProperty("nav_key", item.key)
        btn.setProperty("icon_name", item.icon_name)
        btn.setProperty("emoji_fallback", item.emoji_fallback)

        if icon is not None:
            btn.setIcon(icon)
            btn.setIconSize(QSize(18, 18))

        btn.clicked.connect(lambda _=False, k=item.key: self.navigated.emit(k))
        layout.addWidget(btn)
        self._buttons[item.key] = btn

    def set_active(self, key: str) -> None:
        self._active_key = key
        for k, btn in self._buttons.items():
            active = (k == key)
            btn.setChecked(active)

            icon_name = str(btn.property("icon_name") or "")
            if icon_name:
                color = "#1DB954" if active else "#B3B3B3"
                icon = _qta_icon(icon_name, color=color)
                if icon is not None:
                    btn.setIcon(icon)
                    btn.setIconSize(QSize(18, 18))

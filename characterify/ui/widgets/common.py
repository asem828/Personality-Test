from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Card(QFrame):
    """A modern card container."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        self.setContentsMargins(0, 0, 0, 0)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        self._layout = layout

    @property
    def body(self) -> QVBoxLayout:
        return self._layout


class H1(QLabel):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("H1")
        self.setWordWrap(True)


class H2(QLabel):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("H2")
        self.setWordWrap(True)


class Muted(QLabel):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("Muted")
        self.setWordWrap(True)


class Badge(QLabel):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("Badge")


class LikertScale(QWidget):
    """1-5 scale with radio buttons."""

    valueChanged = Signal(int)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self._group = QButtonGroup(self)
        self._group.setExclusive(True)

        self._buttons: list[QRadioButton] = []
        for i in range(1, 6):
            rb = QRadioButton(str(i))
            rb.setCursor(Qt.PointingHandCursor)
            self._group.addButton(rb, i)
            self._buttons.append(rb)
            layout.addWidget(rb)

        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self._group.idClicked.connect(self._on_clicked)

    def _on_clicked(self, _id: int) -> None:
        self.valueChanged.emit(self.value())

    def set_value(self, v: int) -> None:
        btn = self._group.button(int(v))
        if btn:
            btn.setChecked(True)

    def value(self) -> int:
        return int(self._group.checkedId() or 0)

    def is_answered(self) -> bool:
        return self.value() > 0


class QuestionBlock(Card):
    """Card styled question with likert scale."""

    def __init__(self, number: int, text: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        header = QLabel(f"{number}. {text}")
        header.setWordWrap(True)
        header.setStyleSheet("font-weight: 600;")
        self.body.addWidget(header)

        scale = LikertScale()
        self.body.addWidget(scale)
        self.scale = scale

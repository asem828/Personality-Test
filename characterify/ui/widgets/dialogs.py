from __future__ import annotations

from typing import Optional, Tuple

from PySide6.QtWidgets import QInputDialog, QMessageBox, QWidget


def show_error(parent: QWidget, title: str, message: str) -> None:
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Critical)
    box.setWindowTitle(title)
    box.setText(message)
    box.exec()


def show_info(parent: QWidget, title: str, message: str) -> None:
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Information)
    box.setWindowTitle(title)
    box.setText(message)
    box.exec()


def ask_yes_no(parent: QWidget, title: str, message: str) -> bool:
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Question)
    box.setWindowTitle(title)
    box.setText(message)
    box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    box.setDefaultButton(QMessageBox.No)
    return box.exec() == QMessageBox.Yes


def prompt_text(parent: QWidget, title: str, label: str, default: str = "") -> Tuple[Optional[str], bool]:
    text, ok = QInputDialog.getText(parent, title, label, text=default)
    if not ok:
        return None, False
    return text, True

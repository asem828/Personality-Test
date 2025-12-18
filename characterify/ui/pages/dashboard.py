from __future__ import annotations

from datetime import datetime
from typing import Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from characterify.app_context import AppContext
from characterify.db.repositories import TestHistoryRepository, TestSessionRepository
from characterify.ui.widgets.common import Badge, Card, H1, H2, Muted
from characterify.ui.widgets.dialogs import ask_yes_no, show_error, show_info
from characterify.utils.i18n import t


class DashboardPage(QWidget):
    def __init__(
        self,
        ctx: AppContext,
        on_open_history: Callable[[int], None],
        on_resume_session: Callable[[str], None],
    ) -> None:
        super().__init__()
        self.ctx = ctx
        self.on_open_history = on_open_history
        self.on_resume_session = on_resume_session

        self.history_repo = TestHistoryRepository(ctx.db)
        self.session_repo = TestSessionRepository(ctx.db)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        root.addWidget(H1("Dashboard"))
        root.addWidget(Muted("Profil, history tes, dan progress yang tersimpan."))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        root.addWidget(scroll, 1)

        body = QWidget()
        scroll.setWidget(body)
        self.body_layout = QVBoxLayout(body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(12)

        # Profile + sessions cards
        self.profile_card = Card()
        self.sessions_card = Card()
        self.body_layout.addWidget(self.profile_card)
        self.body_layout.addWidget(self.sessions_card)

        # History table card
        self.history_card = Card()
        self.body_layout.addWidget(self.history_card)

        self.body_layout.addStretch(1)

        self._build_history_ui()
        self.refresh()

    def _build_history_ui(self) -> None:
        self.history_card.body.addWidget(H2("Riwayat Tes"))

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Tanggal", "Test", "Result", "ID"])
        self.table.setColumnHidden(3, True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.doubleClicked.connect(self._open_selected)

        self.history_card.body.addWidget(self.table)

        row = QHBoxLayout()
        btn_view = QPushButton("Lihat Detail Hasil")
        btn_view.clicked.connect(self._open_selected)
        row.addWidget(btn_view)

        btn_pdf = QPushButton("Export PDF")
        btn_pdf.clicked.connect(self._pdf_selected)
        row.addWidget(btn_pdf)

        btn_delete = QPushButton("Hapus")
        btn_delete.setObjectName("DangerButton")
        btn_delete.clicked.connect(self._delete_selected)
        row.addWidget(btn_delete)

        row.addStretch(1)
        self.history_card.body.addLayout(row)

    @staticmethod
    def _clear_layout(layout: QLayout) -> None:
        """Safely remove and delete all child widgets/layouts from a layout.

        This prevents "overlapping" duplicates when we rebuild cards multiple times.
        """

        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                break
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
                continue
            child = item.layout()
            if child is not None:
                DashboardPage._clear_layout(child)

                # Detach the layout from its parent to allow GC.
                try:
                    child.setParent(None)
                except Exception:
                    pass

    def refresh(self) -> None:
        uid = self.ctx.current_user_id
        if not uid:
            return
        user = self.ctx.auth.get_user(uid) or {}

        # Profile card
        self._clear_layout(self.profile_card.body)

        self.profile_card.body.addWidget(H2("Profil"))

        form = QWidget()
        grid = QGridLayout(form)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)
        grid.setColumnStretch(1, 1)

        def add_row(row: int, label: str, value: str) -> None:
            k = QLabel(label)
            k.setStyleSheet("font-weight: 600;")
            v = QLabel(value)
            v.setTextInteractionFlags(Qt.TextSelectableByMouse)
            v.setWordWrap(True)
            v.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            grid.addWidget(k, row, 0)
            grid.addWidget(v, row, 1)

        add_row(0, "Nama", str(user.get("name", "-")))
        add_row(1, "Email", str(user.get("email", "-")))
        add_row(2, "Join", str(user.get("created_at", "-")))

        # Stats
        history = self.history_repo.list_by_user(uid)
        add_row(3, "Total Tes", str(len(history)))

        self.profile_card.body.addWidget(form)

        # Sessions card
        self._clear_layout(self.sessions_card.body)

        self.sessions_card.body.addWidget(H2("Saved Sessions"))
        self.sessions_card.body.addWidget(Muted("Progress tes yang Anda simpan untuk dilanjutkan nanti."))

        any_session = False
        for t in self.ctx.scoring.get_tests():
            sess = self.session_repo.get(uid, t.id)
            if not sess:
                continue
            any_session = True
            answers = self.ctx.db.loads(sess.get("answers_json") or "{}") or {}
            answered = sum(1 for _, v in answers.items() if int(v) > 0)
            total = len(t.questions)

            roww = QWidget()
            row = QHBoxLayout(roww)
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(10)
            row.addWidget(Badge(t.title))
            row.addWidget(Muted(f"Progress: {answered}/{total}"))

            btn = QPushButton("Resume")
            btn.setObjectName("PrimaryButton")
            btn.clicked.connect(lambda _=False, tid=t.id: self.on_resume_session(tid))
            row.addWidget(btn)
            row.addStretch(1)
            self.sessions_card.body.addWidget(roww)

        if not any_session:
            self.sessions_card.body.addWidget(Muted("Tidak ada sesi tersimpan."))

        # Fill table
        self._load_table(history)

    def _load_table(self, history_rows) -> None:
        self.table.setRowCount(0)
        for row in history_rows:
            r = self.table.rowCount()
            self.table.insertRow(r)

            dt = row.get("created_at", "")
            test_id = row.get("test_type", "")
            result = row.get("result_type", "")

            # convert test_id to nice title
            t = next((x for x in self.ctx.scoring.get_tests() if x.id == test_id), None)
            test_title = t.title if t else test_id

            self.table.setItem(r, 0, QTableWidgetItem(dt))
            self.table.setItem(r, 1, QTableWidgetItem(test_title))
            self.table.setItem(r, 2, QTableWidgetItem(result))
            self.table.setItem(r, 3, QTableWidgetItem(str(row.get("id"))))

        self.table.resizeColumnsToContents()

    def _selected_history_id(self) -> Optional[int]:
        items = self.table.selectedItems()
        if not items:
            return None
        # Hidden column index 3
        row = items[0].row()
        hid = self.table.item(row, 3)
        if not hid:
            return None
        try:
            return int(hid.text())
        except Exception:
            return None

    def _open_selected(self) -> None:
        hid = self._selected_history_id()
        if hid is None:
            show_error(self, "Pilih Item", "Pilih salah satu history terlebih dahulu.")
            return
        self.on_open_history(hid)

    def _delete_selected(self) -> None:
        uid = self.ctx.current_user_id
        if not uid:
            return
        hid = self._selected_history_id()
        if hid is None:
            show_error(self, "Pilih Item", "Pilih salah satu history terlebih dahulu.")
            return
        if not ask_yes_no(self, "Hapus", "Hapus history yang dipilih?"):
            return
        self.history_repo.delete(hid, uid)
        show_info(self, "Hapus", "History berhasil dihapus.")
        self.refresh()

    def _pdf_selected(self) -> None:
        uid = self.ctx.current_user_id
        if not uid:
            return
        hid = self._selected_history_id()
        if hid is None:
            show_error(self, "Pilih Item", "Pilih salah satu history terlebih dahulu.")
            return
        row = self.history_repo.get(hid, uid)
        if not row:
            show_error(self, "Tidak Ditemukan", "History tidak ditemukan.")
            return
        payload = self.ctx.db.loads(row["score_json"])
        payload["test_id"] = row["test_type"]
        payload["result_type"] = row["result_type"]

        user = self.ctx.auth.get_user(uid) or {}
        test_id = row["test_type"]
        t = next((x for x in self.ctx.scoring.get_tests() if x.id == test_id), None)
        title = f"{t.title} — {t.subtitle}" if t else test_id

        try:
            path = self.ctx.pdf.create_report(
                user_name=user.get("name", "User"),
                user_email=user.get("email", "-"),
                test_title=title,
                result_payload=payload,
                created_at_iso=row.get("created_at"),
            )
        except Exception as exc:
            show_error(self, "Export PDF Gagal", str(exc))
            return
        show_info(self, "Export PDF", f"PDF tersimpan di:\n{path}")

    # Note: Email sending feature intentionally removed for simplicity.

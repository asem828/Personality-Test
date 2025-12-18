from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from characterify.app_context import AppContext
from characterify.db.repositories import TestHistoryRepository
from characterify.services.pdf_report import PdfReportService
from characterify.ui.widgets.charts import ChartPayload, ChartWidget
from characterify.ui.widgets.common import Badge, Card, H1, H2, Muted
from characterify.ui.widgets.dialogs import show_error, show_info
from characterify.utils.i18n import t


class ResultPage(QWidget):
    def __init__(self, ctx: AppContext, on_done) -> None:
        super().__init__()
        self.ctx = ctx
        self.on_done = on_done

        self.payload: Dict[str, Any] = {}
        self.history_id: Optional[int] = None
        self.created_at: str = datetime.utcnow().isoformat()
        self.test_title: str = ""

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        root.addWidget(scroll, 1)

        body = QWidget()
        scroll.setWidget(body)
        self.body_layout = QVBoxLayout(body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(12)

        # Footer actions
        actions = QHBoxLayout()
        self.btn_pdf = QPushButton("Export PDF")
        self.btn_pdf.clicked.connect(self._export_pdf)
        actions.addWidget(self.btn_pdf)

        actions.addStretch(1)

        self.btn_done = QPushButton("Akhiri")
        self.btn_done.setObjectName("PrimaryButton")
        self.btn_done.clicked.connect(self.on_done)
        actions.addWidget(self.btn_done)

        root.addLayout(actions)

    def show_result(self, payload: Dict[str, Any], history_id: Optional[int] = None) -> None:
        self.payload = payload or {}
        self.history_id = history_id
        self.created_at = datetime.utcnow().isoformat()

        # If from history, fetch created_at/test title from DB
        if self.ctx.current_user_id and history_id:
            repo = TestHistoryRepository(self.ctx.db)
            row = repo.get(history_id, self.ctx.current_user_id)
            if row:
                self.created_at = row.get("created_at") or self.created_at

        # Determine test title
        test_id = self.payload.get("test_id", "")
        t = next((x for x in self.ctx.scoring.get_tests() if x.id == test_id), None)
        self.test_title = f"{t.title} — {t.subtitle}" if t else test_id

        self._render()

    def _render(self) -> None:
        # Clear
        while self.body_layout.count():
            it = self.body_layout.takeAt(0)
            w = it.widget()
            if w:
                w.deleteLater()

        result_type = self.payload.get("result_type", "-")
        content = self.payload.get("content", {}) or {}

        header = Card()
        lang = self.ctx.settings.get_language(self.ctx.current_user_id)
        header.body.addWidget(H1(t(self.ctx, "Hasil Tes", "Test Result")))
        line = QHBoxLayout()
        line.addWidget(Badge(self.test_title))
        line.addWidget(Badge(f"{t(self.ctx, 'Hasil', 'Result')}: {result_type}"))
        line.addStretch(1)
        header.body.addLayout(line)
        header.body.addWidget(Muted(f"{t(self.ctx, 'Dibuat', 'Generated')}: {self.created_at}"))

        self.body_layout.addWidget(header)

        # Chart
        chart_kind = self.payload.get("chart_kind", "barh")
        chart_card = Card()
        chart_card.body.addWidget(H2(t(self.ctx, "Chart Hasil", "Result Chart")))

        payload = self._build_chart_payload()
        if payload:
            chart = ChartWidget(payload)
            chart_card.body.addWidget(chart)
        else:
            chart_card.body.addWidget(Muted(t(self.ctx, "Chart tidak tersedia.", "Chart is not available.")))

        self.body_layout.addWidget(chart_card)

        # Summary
        summary_card = Card()
        # Localized content payload
        localized = content.get(lang) or content.get("id") or content

        summary_card.body.addWidget(H2(localized.get("title", t(self.ctx, "Ringkasan", "Summary"))))
        subtitle = localized.get("subtitle", "")
        if subtitle:
            summary_card.body.addWidget(Muted(subtitle))

        summary_md = localized.get("summary_md", "")
        summary_label = QLabel(self._md_to_richtext(summary_md))
        summary_label.setWordWrap(True)
        summary_label.setTextFormat(Qt.RichText)
        summary_card.body.addWidget(summary_label)
        self.body_layout.addWidget(summary_card)

        # Sections
        for section in localized.get("sections", []):
            c = Card()
            c.body.addWidget(H2(section.get("title", "")))

            items = section.get("items", [])
            for it in items:
                lbl = QLabel(f"• {it}")
                lbl.setWordWrap(True)
                c.body.addWidget(lbl)

            self.body_layout.addWidget(c)

        self.body_layout.addStretch(1)

    def _build_chart_payload(self) -> Optional[ChartPayload]:
        test_id = self.payload.get("test_id", "")
        kind = self.payload.get("chart_kind", "barh")
        lang = self.ctx.settings.get_language(self.ctx.current_user_id)

        if kind == "mbti_stacked":
            dims = self.payload.get("percentages", [])
            return ChartPayload(kind="mbti_stacked", data={"dims": dims})

        # barh
        perc = self.payload.get("percentages", {})
        if not isinstance(perc, dict):
            return None

        if test_id == "ocean":
            mapping = {
                "id": {"O": "Keterbukaan", "C": "Ketekunan", "E": "Ekstroversi", "A": "Keramahan", "N": "Neurotisisme"},
                "en": {"O": "Openness", "C": "Conscientiousness", "E": "Extraversion", "A": "Agreeableness", "N": "Neuroticism"},
            }["en" if lang == "en" else "id"]
            labels = [mapping.get(k, k) for k in perc.keys()]
            values = [float(v) for v in perc.values()]
            return ChartPayload(kind="barh", data={"labels": labels, "values": values})

        if test_id == "enneagram":
            labels = [f"{t(self.ctx,'Tipe','Type')} {k}" for k in perc.keys()]
            values = [float(v) for v in perc.values()]
            return ChartPayload(kind="barh", data={"labels": labels, "values": values})

        if test_id == "temperament":
            mapping = {
                "id": {"S": "Sanguine", "C": "Choleric", "P": "Phlegmatic", "M": "Melancholic"},
                "en": {"S": "Sanguine", "C": "Choleric", "P": "Phlegmatic", "M": "Melancholic"},
            }["en" if lang == "en" else "id"]
            labels = [mapping.get(k, k) for k in perc.keys()]
            values = [float(v) for v in perc.values()]
            return ChartPayload(kind="barh", data={"labels": labels, "values": values})

        labels = [str(k) for k in perc.keys()]
        values = [float(v) for v in perc.values()]
        return ChartPayload(kind="barh", data={"labels": labels, "values": values})

    def _export_pdf(self) -> None:
        if not self.ctx.current_user_id:
            return
        user = self.ctx.auth.get_user(self.ctx.current_user_id) or {}
        name = user.get("name", "User")
        email = user.get("email", "-")
        try:
            path = self.ctx.pdf.create_report(
                user_name=name,
                user_email=email,
                test_title=self.test_title,
                result_payload=self.payload,
                created_at_iso=self.created_at,
            )
        except Exception as exc:
            show_error(self, t(self.ctx, "Export PDF Gagal", "PDF Export Failed"), str(exc))
            return
        show_info(self, t(self.ctx, "Export PDF", "Export PDF"), f"PDF {t(self.ctx,'tersimpan di','saved to')}:\n{path}")

    def retranslate_ui(self) -> None:
        self.btn_pdf.setText(t(self.ctx, "Export PDF", "Export PDF"))
        self.btn_done.setText(t(self.ctx, "Akhiri", "Finish"))

    @staticmethod
    def _md_to_richtext(md: str) -> str:
        # A minimal markdown-like formatting helper for summary.
        html = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html = html.replace("\n", "<br/>")
        # bold conversion
        while "**" in html:
            html = html.replace("**", "<b>", 1).replace("**", "</b>", 1)
        return html

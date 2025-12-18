from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from characterify.app_context import AppContext
from characterify.ui.widgets.common import Card, H1, H2, Muted
from characterify.utils.i18n import t


class HomePage(QWidget):
    def __init__(self, ctx: AppContext, on_start_test: Callable[[], None]) -> None:
        super().__init__()
        self.ctx = ctx
        self.on_start_test = on_start_test

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        body = QWidget()
        scroll.setWidget(body)
        root.addWidget(scroll)

        layout = QVBoxLayout(body)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        # Hero banner
        hero = Card()
        hero.body.setContentsMargins(0, 0, 0, 0)
        self.hero_img = QLabel()
        self.hero_img.setAlignment(Qt.AlignCenter)
        self.hero_img.setMinimumHeight(220)

        pix = self._load_branding()
        if pix:
            self.hero_img.setPixmap(pix.scaledToWidth(980, Qt.SmoothTransformation))
        else:
            self.hero_img.setText("Characterify")
            self.hero_img.setStyleSheet("font-size: 28pt; font-weight: 800; padding: 40px;")

        hero.body.addWidget(self.hero_img)

        hero_text = QWidget()
        ht = QVBoxLayout(hero_text)
        ht.setContentsMargins(18, 16, 18, 16)
        ht.setSpacing(6)

        self.hero_title = H1()
        self.hero_subtitle = Muted()
        ht.addWidget(self.hero_title)
        ht.addWidget(self.hero_subtitle)

        row = QHBoxLayout()
        self.btn_start = QPushButton()
        self.btn_start.setObjectName("PrimaryButton")
        self.btn_start.clicked.connect(self.on_start_test)
        row.addWidget(self.btn_start)
        row.addStretch(1)
        ht.addLayout(row)

        hero.body.addWidget(hero_text)
        layout.addWidget(hero)

        # Feature highlights
        grid = QGridLayout()
        grid.setSpacing(12)

        self._feature_widgets: list[tuple[H2, Muted, tuple[str, str], tuple[str, str]]] = []

        items = [
            (("Deep Personality Analysis", "Deep Personality Analysis"),
             ("Dapatkan gambaran trait, kekuatan, dan area pengembangan yang jelas untuk konteks personal maupun profesional.",
              "Get a clear picture of traits, strengths, and development areas for personal and professional contexts.")),
            (("Powered by Psychology", "Powered by Psychology"),
             ("Berbasis kerangka psikologi yang umum digunakan. Fokus pada insight, bukan sekadar label.",
              "Built on commonly used psychology frameworks. Focused on insights—not just labels.")),
            (("Quick and Engaging", "Quick and Engaging"),
             ("Tampilan modern. 5 pertanyaan per halaman dengan progress yang jelas.",
              "Modern experience. 5 questions per page with clear progress.")),
            (("Your Path to Growth", "Your Path to Growth"),
             ("Hasil dilengkapi saran pengembangan diri: komunikasi, kerja tim, dan rutinitas kecil yang bisa langsung dicoba.",
              "Results include growth tips: communication, teamwork, and small habits you can try immediately.")),
            (("Detailed Reports", "Detailed Reports"),
             ("Hasil dapat disimpan ke history dan diekspor menjadi PDF untuk dibagikan.",
              "Save results to history and export a PDF report you can share.")),
        ]

        for idx, (title_pair, desc_pair) in enumerate(items):
            c = Card()
            h2 = H2()
            m = Muted()
            c.body.addWidget(h2)
            c.body.addWidget(m)
            grid.addWidget(c, idx // 2, idx % 2)
            self._feature_widgets.append((h2, m, title_pair, desc_pair))

        grid_wrap = QWidget()
        grid_wrap.setLayout(grid)
        layout.addWidget(grid_wrap)

        layout.addStretch(1)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        self.hero_title.setText(t(self.ctx, "Temukan apa yang membuat Anda menonjol", "Find what makes you stand out"))
        self.hero_subtitle.setText(
            t(
                self.ctx,
                "Analisis kepribadian yang cepat, modern, dan berbasis kerangka psikologi — untuk insight yang actionable.",
                "Fast, modern personality insights based on psychology frameworks—designed to be actionable.",
            )
        )
        self.btn_start.setText(t(self.ctx, "Mulai Tes", "Start Test"))

        for h2, m, title_pair, desc_pair in self._feature_widgets:
            h2.setText(t(self.ctx, title_pair[0], title_pair[1]))
            m.setText(t(self.ctx, desc_pair[0], desc_pair[1]))

    def _load_branding(self) -> Optional[QPixmap]:
        here = Path(__file__).resolve()
        img_path = here.parent.parent.parent / "assets" / "images" / "branding.png"
        if img_path.exists():
            return QPixmap(str(img_path))
        return None

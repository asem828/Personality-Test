from __future__ import annotations

from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from characterify import __version__
from characterify.app_context import AppContext
from characterify.ui.widgets.common import Card, H1, H2, Muted
from characterify.utils.i18n import t


class InformationPage(QWidget):
    def __init__(self, ctx: AppContext) -> None:
        super().__init__()
        self.ctx = ctx

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        self.title = H1()
        self.subtitle = Muted()
        root.addWidget(self.title)
        root.addWidget(self.subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        root.addWidget(scroll, 1)

        body = QWidget()
        scroll.setWidget(body)
        layout = QVBoxLayout(body)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.about = Card()
        self.about_h2 = H2()
        self.about_p = Muted()
        self.about.body.addWidget(self.about_h2)
        self.about.body.addWidget(self.about_p)
        layout.addWidget(self.about)

        self.disclaimer = Card()
        self.disclaimer_h2 = H2()
        self.disclaimer_text = QLabel()
        self.disclaimer_text.setWordWrap(True)
        self.disclaimer_text.setTextFormat(Qt.RichText)
        self.disclaimer.body.addWidget(self.disclaimer_h2)
        self.disclaimer.body.addWidget(self.disclaimer_text)
        layout.addWidget(self.disclaimer)

        self.privacy = Card()
        self.privacy_h2 = H2()
        self.privacy_p = Muted()
        self.privacy.body.addWidget(self.privacy_h2)
        self.privacy.body.addWidget(self.privacy_p)
        layout.addWidget(self.privacy)

        self.meta = Card()
        self.meta_h2 = H2()
        self.meta_v = Muted()
        self.meta_contact = Muted()
        self.meta.body.addWidget(self.meta_h2)
        self.meta.body.addWidget(self.meta_v)
        self.meta.body.addWidget(self.meta_contact)
        layout.addWidget(self.meta)

        layout.addStretch(1)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        self.title.setText(t(self.ctx, "Informasi", "Information"))
        self.subtitle.setText(t(self.ctx, "Informasi aplikasi, disclaimer, dan privasi.", "App information, disclaimers, and privacy."))

        self.about_h2.setText(t(self.ctx, "Tentang Characterify", "About Characterify"))
        self.about_p.setText(
            t(
                self.ctx,
                "Characterify adalah aplikasi desktop untuk tes kepribadian dan pembelajaran psikologi. "
                "UI/UX terinspirasi dari struktur Spotify: sidebar, topbar, content area, dan status bar.",
                "Characterify is a desktop app for personality tests and psychology learning. "
                "The UI/UX is inspired by Spotify’s structure: sidebar, topbar, content area, and status bar.",
            )
        )

        self.disclaimer_h2.setText(t(self.ctx, "Disclaimer", "Disclaimer"))
        self.disclaimer_text.setText(
            t(
                self.ctx,
                "• Hasil tes bersifat informatif dan edukatif, bukan diagnosis klinis.<br/>"
                "• Gunakan hasil sebagai bahan refleksi dan pengembangan diri.<br/>"
                "• Jika Anda membutuhkan bantuan profesional, konsultasikan dengan psikolog/psikiater.",
                "• Test results are informational and educational, not a clinical diagnosis.<br/>"
                "• Use results for reflection and growth.<br/>"
                "• If you need professional help, consult a qualified psychologist/psychiatrist.",
            )
        )

        self.privacy_h2.setText(t(self.ctx, "Privasi & Penyimpanan Data", "Privacy & Data Storage"))
        self.privacy_p.setText(
            t(
                self.ctx,
                "Aplikasi ini offline‑first: data disimpan secara lokal di perangkat Anda (SQLite). "
                "Password akun disimpan sebagai hash (bukan plaintext).",
                "This app is offline‑first: data is stored locally on your device (SQLite). "
                "Account passwords are stored as hashes (not plaintext).",
            )
        )

        self.meta_h2.setText(t(self.ctx, "Versi", "Version"))
        self.meta_v.setText(f"Characterify Desktop v{__version__}")
        self.meta_contact.setText(t(self.ctx, "Kontak support: support@characterify.local (contoh)", "Support contact: support@characterify.local (example)"))

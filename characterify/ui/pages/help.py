# characterify/ui/pages/help.py
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
)


class HelpPage(QWidget):
    """
    HelpPage (tanpa QToolBox/tab/accordion, dan tanpa Card widget).
    Aman terhadap QSS global dan tidak tergantung API Card yang berbeda-beda.
    """

    def __init__(self, ctx) -> None:
        super().__init__()
        self.ctx = ctx

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background: transparent;")

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("Bantuan")
        title.setStyleSheet("font-size: 28px; font-weight: 800; color: white;")
        root.addWidget(title)

        subtitle = QLabel("FAQ dan petunjuk penggunaan aplikasi Characterify.")
        subtitle.setStyleSheet("color: rgba(255,255,255,0.72); font-size: 13px;")
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")
        root.addWidget(scroll, 1)

        content = QWidget()
        content.setAttribute(Qt.WA_StyledBackground, True)
        content.setStyleSheet("background: transparent;")
        scroll.setWidget(content)

        lay = QVBoxLayout(content)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        lay.addWidget(self._section_card(
            "Petunjuk Penggunaan",
            "Panduan singkat langkah demi langkah.",
            self._usage_items()
        ))

        lay.addWidget(self._section_card(
            "FAQ",
            "Pertanyaan yang sering ditanyakan.",
            self._faq_items()
        ))

        lay.addStretch(1)

    # ----------------------------
    # Data (konten)
    # ----------------------------
    def _usage_items(self):
        return [
            ("1) Login / Register", "Buat akun terlebih dahulu atau login menggunakan email dan password."),
            ("2) Pilih Menu Test", "Masuk ke menu Test lalu pilih jenis tes yang ingin Anda kerjakan."),
            ("3) Baca Intro & Petunjuk", "Setiap tes memiliki deskripsi dan aturan pengerjaan. Baca sebelum mulai."),
            ("4) Mulai Tes", "Jawab pertanyaan dengan jujur. Tiap halaman menampilkan 5 pertanyaan."),
            ("5) Navigasi Next/Back", "Gunakan Next untuk lanjut dan Back untuk mengoreksi jawaban sebelumnya."),
            ("6) Lihat Hasil", "Setelah selesai, Anda akan melihat hasil, ringkasan, chart, dan rekomendasi pengembangan diri."),
            ("7) Simpan Riwayat", "Hasil otomatis tersimpan di Dashboard sebagai history tes."),
            ("8) Export PDF", "Di halaman hasil atau Dashboard, gunakan tombol Export PDF untuk laporan."),
            ("9) Learn", "Baca materi psikologi/kepribadian di menu Learn. Anda bisa bookmark artikel."),
            ("10) Settings", "Ubah tema (Dark/Light), bahasa (ID/EN), dan kelola data history."),
        ]

    def _faq_items(self):
        return [
            (
                "Apakah ini diagnosis klinis?",
                "Tidak. Characterify adalah alat edukasi dan refleksi diri. Hasil tes tidak menggantikan diagnosis profesional. "
                "Jika Anda mengalami gejala yang berat atau mengganggu aktivitas, pertimbangkan konsultasi ke profesional."
            ),
            (
                "Apakah data saya aman?",
                "Aplikasi ini offline-first: data disimpan lokal di komputer Anda (SQLite). Tidak ada pengiriman data ke server. "
                "Anda bisa menghapus riwayat kapan saja melalui Dashboard atau Settings."
            ),
            (
                "Bagaimana cara export hasil ke PDF?",
                "Buka hasil tes lalu klik Export PDF. Anda juga bisa export dari Dashboard pada item riwayat tes."
            ),
            (
                "Bisakah saya ganti tema dan bahasa?",
                "Bisa. Masuk Settings → Theme (Dark/Light) dan Language (ID/EN). Perubahan langsung diterapkan."
            ),
            (
                "Apakah saya bisa menghapus history tes?",
                "Bisa. Dashboard → Riwayat Tes → Delete pada item tertentu, atau bersihkan semua via Settings."
            ),
        ]

    # ----------------------------
    # UI builders
    # ----------------------------
    def _section_card(self, title: str, subtitle: str, items):
        card = QFrame()
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 16px;
            }
        """)

        outer = QVBoxLayout(card)
        outer.setContentsMargins(18, 16, 18, 16)
        outer.setSpacing(10)

        h = QLabel(title)
        h.setStyleSheet("font-size: 18px; font-weight: 800; color: white;")
        h.setWordWrap(True)

        sub = QLabel(subtitle)
        sub.setStyleSheet("color: rgba(255,255,255,0.72); font-size: 13px;")
        sub.setWordWrap(True)

        outer.addWidget(h)
        outer.addWidget(sub)

        for head, desc in items:
            outer.addWidget(self._item_block(head, desc))

        return card

    def _item_block(self, head: str, desc: str) -> QWidget:
        w = QWidget()
        w.setAttribute(Qt.WA_StyledBackground, True)
        w.setStyleSheet("background: transparent;")

        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(4)

        t = QLabel(head)
        t.setStyleSheet("font-weight: 800; font-size: 14px; color: white;")
        t.setWordWrap(True)

        d = QLabel(desc)
        d.setStyleSheet("color: rgba(255,255,255,0.78); font-size: 13px;")
        d.setWordWrap(True)
        d.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        l.addWidget(t)
        l.addWidget(d)
        return w

from __future__ import annotations

from typing import Callable, Dict, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from characterify.app_context import AppContext
from characterify.data.articles import get_article, get_articles
from characterify.db.repositories import ArticleReadRepository
from characterify.ui.widgets.common import Badge, Card, H1, H2, Muted
from characterify.utils.i18n import t


class LearnPage(QWidget):
    def __init__(self, ctx: AppContext, on_open_article: Callable[[str], None]) -> None:
        super().__init__()
        self.ctx = ctx
        self.on_open_article = on_open_article

        self.repo = ArticleReadRepository(ctx.db)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        self.h_title = H1("")
        self.h_sub = Muted("")
        root.addWidget(self.h_title)
        root.addWidget(self.h_sub)

        # Filters
        filters = QHBoxLayout()
        self.search = QLineEdit()
        self.search.textChanged.connect(self.refresh)
        filters.addWidget(self.search, 2)

        self.category = QComboBox()
        self.category.currentTextChanged.connect(self.refresh)
        filters.addWidget(self.category, 1)

        root.addLayout(filters)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        root.addWidget(scroll, 1)

        body = QWidget()
        scroll.setWidget(body)
        self.body_layout = QVBoxLayout(body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(12)

        self._reload_data()

    def _reload_data(self) -> None:
        lang = self.ctx.settings.get_language(self.ctx.current_user_id)
        self.articles: List[Dict] = get_articles(lang)

        # retranslate static UI
        self.h_title.setText(t(self.ctx, "Learn", "Learn"))
        self.h_sub.setText(
            t(
                self.ctx,
                "Artikel pembelajaran tentang kepribadian dan psikologi—ringkas, terstruktur, dan praktis.",
                "Learning articles about personality and psychology—structured, practical, and easy to follow.",
            )
        )
        self.search.setPlaceholderText(t(self.ctx, "Cari artikel…", "Search articles…"))

        # categories depend on language
        self.category.blockSignals(True)
        prev = self.category.currentText()
        self.category.clear()
        cats = sorted({a["category"] for a in self.articles})
        self.category.addItem(t(self.ctx, "All", "All"))
        for c in cats:
            self.category.addItem(c)
        # try restore selection
        if prev in cats:
            self.category.setCurrentText(prev)
        self.category.blockSignals(False)

        self.refresh()

    def _filtered(self) -> List[Dict]:
        q = (self.search.text() or "").strip().lower()
        cat = self.category.currentText()
        all_label = t(self.ctx, "All", "All")
        items: List[Dict] = []
        for a in self.articles:
            if cat != all_label and a["category"] != cat:
                continue
            if q:
                hay = f"{a['title']} {a['summary']} {a['category']}".lower()
                if q not in hay:
                    continue
            items.append(a)
        return items

    def refresh(self) -> None:
        # Clear
        while self.body_layout.count():
            it = self.body_layout.takeAt(0)
            w = it.widget()
            if w:
                w.deleteLater()

        items = self._filtered()

        for a in items:
            c = Card()
            title_row = QHBoxLayout()
            title_row.addWidget(H2(a["title"]))
            title_row.addStretch(1)
            title_row.addWidget(Badge(a["read_time"]))
            title_row.addWidget(Badge(a["category"]))
            c.body.addLayout(title_row)

            c.body.addWidget(Muted(a["summary"]))

            # Bookmark state
            bookmarked = False
            if self.ctx.current_user_id:
                st = self.repo.get_status(self.ctx.current_user_id, a["id"])
                bookmarked = st["bookmarked"]

            row = QHBoxLayout()
            if bookmarked:
                row.addWidget(Badge("★ " + t(self.ctx, "Tersimpan", "Bookmarked")))
            row.addStretch(1)
            btn = QPushButton(t(self.ctx, "Buka", "Open"))
            btn.setObjectName("PrimaryButton")
            btn.clicked.connect(lambda _=False, aid=a["id"]: self.on_open_article(aid))
            row.addWidget(btn)
            c.body.addLayout(row)

            self.body_layout.addWidget(c)

        self.body_layout.addStretch(1)

    def retranslate_ui(self) -> None:
        self._reload_data()


class ArticleReaderPage(QWidget):
    def __init__(self, ctx: AppContext, on_back: Callable[[], None]) -> None:
        super().__init__()
        self.ctx = ctx
        self.on_back = on_back
        self.repo = ArticleReadRepository(ctx.db)

        self.current_article_id: str = ""

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        top = QHBoxLayout()
        self.btn_back = QPushButton("")
        self.btn_back.setText("← " + t(self.ctx, "Kembali", "Back"))
        self.btn_back.clicked.connect(self.on_back)
        top.addWidget(self.btn_back)

        top.addStretch(1)

        self.btn_bookmark = QPushButton("")
        self.btn_bookmark.clicked.connect(self._toggle_bookmark)
        top.addWidget(self.btn_bookmark)

        root.addLayout(top)

        self.title = H1("")
        root.addWidget(self.title)

        self.meta = Muted("")
        root.addWidget(self.meta)

        self.reader = QTextBrowser()
        self.reader.setOpenExternalLinks(True)
        root.addWidget(self.reader, 1)

    def open_article(self, article_id: str) -> None:
        self.current_article_id = article_id
        lang = self.ctx.settings.get_language(self.ctx.current_user_id)
        a = get_article(article_id, lang)
        if not a:
            self.title.setText(t(self.ctx, "Artikel tidak ditemukan", "Article not found"))
            self.meta.setText("")
            self.reader.setHtml("")
            return

        self.title.setText(a["title"])
        self.meta.setText(f"{a['category']} • {a['read_time']}")
        self.reader.setHtml(a["content"])

        # Mark read
        if self.ctx.current_user_id:
            self.repo.mark_read(self.ctx.current_user_id, article_id, bookmarked=False)

        self._refresh_bookmark_button()

    def retranslate_ui(self) -> None:
        # re-open current article with new language
        if self.current_article_id:
            self.open_article(self.current_article_id)
        else:
            self.btn_back.setText("← " + t(self.ctx, "Kembali", "Back"))
            self._refresh_bookmark_button()

    def _refresh_bookmark_button(self) -> None:
        if not self.ctx.current_user_id or not self.current_article_id:
            self.btn_bookmark.setText(t(self.ctx, "Bookmark", "Bookmark"))
            return
        st = self.repo.get_status(self.ctx.current_user_id, self.current_article_id)
        self.btn_bookmark.setText(
            t(self.ctx, "Unbookmark", "Unbookmark") if st["bookmarked"] else t(self.ctx, "Bookmark", "Bookmark")
        )

    def _toggle_bookmark(self) -> None:
        if not self.ctx.current_user_id or not self.current_article_id:
            return
        st = self.repo.get_status(self.ctx.current_user_id, self.current_article_id)
        new_val = not st["bookmarked"]
        self.repo.toggle_bookmark(self.ctx.current_user_id, self.current_article_id, new_val)
        self._refresh_bookmark_button()

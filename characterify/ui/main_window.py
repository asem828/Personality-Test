from __future__ import annotations

from typing import Any, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from characterify.app_context import AppContext
from characterify.services.telemetry import TelemetryService
from characterify.ui.pages.account_settings import AccountSettingsPage
from characterify.ui.pages.auth import LoginPage, RegisterPage
from characterify.ui.pages.dashboard import DashboardPage
from characterify.ui.pages.help import HelpPage
from characterify.ui.pages.home import HomePage
from characterify.ui.pages.information import InformationPage
from characterify.ui.pages.learn import ArticleReaderPage, LearnPage
from characterify.ui.pages.result import ResultPage
from characterify.ui.pages.settings import SettingsPage
from characterify.ui.pages.test_flow import TestIntroPage, TestListPage, TestRunnerPage
from characterify.ui.widgets.sidebar import NavItem, Sidebar
from characterify.ui.widgets.topbar import TopBar
from characterify.utils.i18n import t


class MainWindow(QMainWindow):
    """Main application window.

    Layout: Spotify-like sidebar + topbar + stacked content area + small bottom status bar.
    """

    def __init__(self, ctx: AppContext, telemetry: TelemetryService) -> None:
        super().__init__()
        self.ctx = ctx
        self.telemetry = telemetry

        self.setWindowTitle("Characterify")
        self.setObjectName("AppRoot")

        self._current_key: str = "home"

        # Root stack: Auth vs App
        root = QStackedWidget()
        self.setCentralWidget(root)
        self._root_stack = root

        self._auth_view = self._build_auth_view()
        self._app_view = self._build_app_view()

        root.addWidget(self._auth_view)
        root.addWidget(self._app_view)

        self._show_auth()

        # Apply initial translations based on global settings
        self.retranslate_ui()

    # ---------------------------
    # i18n refresh
    # ---------------------------
    def retranslate_ui(self) -> None:
        """Refresh nav labels, titles, and per-page static text."""
        # Sidebar nav items (2 groups)
        g1 = [
            NavItem("home", t(self.ctx, "Beranda", "Home"), icon_name="fa5s.home", emoji_fallback="🏠"),
            NavItem("test", t(self.ctx, "Tes", "Test"), icon_name="fa5s.clipboard-list", emoji_fallback="🧪"),
            NavItem("learn", t(self.ctx, "Belajar", "Learn"), icon_name="fa5s.book-open", emoji_fallback="📚"),
        ]
        g2 = [
            NavItem("settings", t(self.ctx, "Pengaturan", "Settings"), icon_name="fa5s.cog", emoji_fallback="⚙️"),
            NavItem("information", t(self.ctx, "Informasi", "Information"), icon_name="fa5s.info-circle", emoji_fallback="ℹ️"),
            NavItem("help", t(self.ctx, "Bantuan", "Help"), icon_name="fa5s.question-circle", emoji_fallback="❓"),
        ]

        if hasattr(self, "sidebar"):
            self.sidebar.set_items(group1=g1, group2=g2)
            # Group labels
            try:
                self.sidebar.group1_label.setText(t(self.ctx, "MENU", "MENU"))
                self.sidebar.group2_label.setText(t(self.ctx, "PREFERENSI", "PREFERENCES"))
            except Exception:
                pass
            # Keep current active item
            self.sidebar.set_active(getattr(self, "_current_key", "home") if self.ctx.is_authenticated() else "home")

        # Topbar texts (search/menu)
        if hasattr(self, "topbar"):
            try:
                self.topbar.retranslate_ui(self.ctx)
            except Exception:
                pass

        # Status bar
        if hasattr(self, "status_label"):
            self.status_label.setText(t(self.ctx, "Siap", "Ready") if self.ctx.is_authenticated() else t(self.ctx, "Silakan login", "Please login"))

        # Title
        if hasattr(self, "topbar"):
            self._apply_title_for_key(getattr(self, "_current_key", "home"))

        # Re-translate pages if they support it
        for p in getattr(self, "_page_map", {}).values():
            fn = getattr(p, "retranslate_ui", None)
            if callable(fn):
                try:
                    fn()
                except Exception:
                    pass

        # Auth pages too
        try:
            for i in range(self._auth_stack.count()):
                w = self._auth_stack.widget(i)
                fn = getattr(w, "retranslate_ui", None)
                if callable(fn):
                    fn()
        except Exception:
            pass

    def _apply_title_for_key(self, key: str) -> None:
        mapping = {
            "home": t(self.ctx, "Beranda", "Home"),
            "test": t(self.ctx, "Tes", "Test"),
            "test_intro": t(self.ctx, "Tes", "Test"),
            "test_run": t(self.ctx, "Tes", "Test"),
            "result": t(self.ctx, "Hasil", "Result"),
            "learn": t(self.ctx, "Belajar", "Learn"),
            "article": t(self.ctx, "Belajar", "Learn"),
            "settings": t(self.ctx, "Pengaturan", "Settings"),
            "information": t(self.ctx, "Informasi", "Information"),
            "help": t(self.ctx, "Bantuan", "Help"),
            "dashboard": t(self.ctx, "Dashboard", "Dashboard"),
            "account": t(self.ctx, "Pengaturan Akun", "Account Settings"),
        }
        self.topbar.set_title(mapping.get(key, "Characterify"))

    # ---------------------------
    # Views
    # ---------------------------
    def _build_auth_view(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(40, 40, 40, 40)

        auth_stack = QStackedWidget()
        self._auth_stack = auth_stack

        login = LoginPage(self.ctx, on_login=self._on_login_success, go_register=lambda: auth_stack.setCurrentIndex(1))
        register = RegisterPage(self.ctx, go_login=lambda: auth_stack.setCurrentIndex(0))

        auth_stack.addWidget(login)
        auth_stack.addWidget(register)

        layout.addStretch(1)
        layout.addWidget(auth_stack, alignment=Qt.AlignCenter)
        layout.addStretch(1)
        return w

    def _build_app_view(self) -> QWidget:
        w = QWidget()
        main_layout = QHBoxLayout(w)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.set_items(group1=[], group2=[])
        self.sidebar.navigated.connect(self.navigate)
        main_layout.addWidget(self.sidebar)

        # Right panel: topbar + pages + bottom status bar
        right = QFrame()
        right.setObjectName("ContentArea")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.topbar = TopBar()
        self.topbar.logoutRequested.connect(self.logout)
        self.topbar.dashboardRequested.connect(lambda: self.navigate("dashboard"))
        self.topbar.accountRequested.connect(lambda: self.navigate("account"))
        right_layout.addWidget(self.topbar)

        self.pages = QStackedWidget()
        right_layout.addWidget(self.pages, 1)

        # Bottom bar
        bottom = QFrame()
        bottom.setFixedHeight(38)
        bottom.setStyleSheet("background: rgba(255,255,255,0.03); border-top: 1px solid #1F1F1F;")
        bl = QHBoxLayout(bottom)
        bl.setContentsMargins(16, 0, 16, 0)
        self.status_label = QLabel(t(self.ctx, "Silakan login", "Please login"))
        self.status_label.setStyleSheet("color: #B3B3B3;")
        bl.addWidget(self.status_label)
        bl.addStretch(1)
        right_layout.addWidget(bottom)

        main_layout.addWidget(right, 1)

        # Instantiate pages
        self._page_map: Dict[str, QWidget] = {}
        self._register_pages()

        return w

    def _register_pages(self) -> None:
        self._add_page("home", HomePage(self.ctx, on_start_test=lambda: self.navigate("test")))
        self._add_page("test", TestListPage(self.ctx, on_select_test=lambda tid: self.navigate("test_intro", test_id=tid)))
        self._add_page("test_intro", TestIntroPage(self.ctx, on_start=lambda tid: self.navigate("test_run", test_id=tid)))
        self._add_page("test_run", TestRunnerPage(self.ctx, on_finished=self._on_test_finished, on_cancel=lambda: self.navigate("test")))
        self._add_page("result", ResultPage(self.ctx, on_done=lambda: self.navigate("test")))
        self._add_page("learn", LearnPage(self.ctx, on_open_article=lambda aid: self.navigate("article", article_id=aid)))
        self._add_page("article", ArticleReaderPage(self.ctx, on_back=lambda: self.navigate("learn")))
        self._add_page("help", HelpPage(self.ctx))
        self._add_page("information", InformationPage(self.ctx))
        self._add_page("settings", SettingsPage(self.ctx, on_theme_changed=self._on_theme_changed))
        self._add_page("dashboard", DashboardPage(self.ctx, on_open_history=self._open_history_result, on_resume_session=self._resume_session))
        self._add_page("account", AccountSettingsPage(self.ctx, on_back=lambda: self.navigate("dashboard")))

        # Default page (won't show until authenticated)
        self.pages.setCurrentWidget(self._page_map["home"])

    def _add_page(self, key: str, page: QWidget) -> None:
        self._page_map[key] = page
        self.pages.addWidget(page)

    # ---------------------------
    # Navigation
    # ---------------------------
    def navigate(self, key: str, **kwargs: Any) -> None:
        if not self.ctx.is_authenticated():
            return

        self._current_key = key

        # Sidebar active only for top-level routes
        if key in ("home", "test", "learn", "settings", "information", "help"):
            self.sidebar.set_active(key)

        # Update dynamic pages
        if key == "test_intro":
            page: TestIntroPage = self._page_map[key]  # type: ignore
            page.load_test(kwargs.get("test_id", "mbti"))
        elif key == "test_run":
            page: TestRunnerPage = self._page_map[key]  # type: ignore
            page.start_test(kwargs.get("test_id", "mbti"))
        elif key == "result":
            page: ResultPage = self._page_map[key]  # type: ignore
            page.show_result(kwargs["payload"], history_id=kwargs.get("history_id"))
        elif key == "article":
            page: ArticleReaderPage = self._page_map[key]  # type: ignore
            page.open_article(kwargs.get("article_id", ""))
        elif key == "dashboard":
            page: DashboardPage = self._page_map[key]  # type: ignore
            page.refresh()
        elif key == "account":
            page: AccountSettingsPage = self._page_map[key]  # type: ignore
            page.load()

        # Change title
        self._apply_title_for_key(key)

        page = self._page_map.get(key)
        if page is None:
            return
        self.pages.setCurrentWidget(page)

    def set_status(self, text: str) -> None:
        self.status_label.setText(text)

    # ---------------------------
    # Auth flow
    # ---------------------------
    def _show_auth(self) -> None:
        self._root_stack.setCurrentWidget(self._auth_view)
        try:
            self._auth_stack.setCurrentIndex(0)
        except Exception:
            pass
        self.set_status(t(self.ctx, "Silakan login", "Please login"))

    def _show_app(self) -> None:
        self._root_stack.setCurrentWidget(self._app_view)
        self.set_status(t(self.ctx, "Siap", "Ready"))

    def _on_login_success(self, user_id: int) -> None:
        self.ctx.current_user_id = user_id
        user = self.ctx.auth.get_user(user_id) or {}
        self.topbar.set_user_label(user.get("name") or t(self.ctx, "Akun", "Account"))

        self.apply_user_preferences(user_id)

        self._show_app()
        self.navigate("dashboard")

    def apply_user_preferences(self, user_id: int) -> None:
        """Apply theme + language for the logged-in user."""
        app = self.qApp()
        theme = self.ctx.settings.get_theme(user_id)
        lang = self.ctx.settings.get_language(user_id)
        self.ctx.settings.apply_theme(app, theme=theme)
        self.ctx.settings.apply_language(app, lang=lang)
        self.retranslate_ui()

    def logout(self) -> None:
        self.ctx.current_user_id = None
        self._show_auth()

    # ---------------------------
    # Test events
    # ---------------------------
    def _on_test_finished(self, payload: Dict[str, Any], history_id: Optional[int] = None) -> None:
        self.navigate("result", payload=payload, history_id=history_id)

    def _open_history_result(self, history_id: int) -> None:
        from characterify.db.repositories import TestHistoryRepository

        repo = TestHistoryRepository(self.ctx.db)
        row = repo.get(history_id, self.ctx.current_user_id or 0)
        if not row:
            return
        payload = self.ctx.db.loads(row["score_json"])
        payload["test_id"] = row["test_type"]
        payload["result_type"] = row["result_type"]
        self.navigate("result", payload=payload, history_id=history_id)

    def _resume_session(self, test_id: str) -> None:
        self.navigate("test_run", test_id=test_id)

    # ---------------------------
    # Settings events
    # ---------------------------
    def _on_theme_changed(self, theme: str) -> None:
        app = self.qApp()
        self.ctx.settings.apply_theme(app, theme=theme)

    @staticmethod
    def qApp():
        from PySide6.QtWidgets import QApplication
        return QApplication.instance()

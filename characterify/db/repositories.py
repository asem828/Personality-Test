from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from characterify.db.database import Database


@dataclass
class UserRepository:
    """CRUD for users."""

    db: Database

    def create(self, name: str, email: str, password_hash: str, password_salt: str) -> int:
        now = datetime.utcnow().isoformat()
        return self.db.execute(
            """
            INSERT INTO users (name, email, password_hash, password_salt, created_at, settings_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, email.lower().strip(), password_hash, password_salt, now, "{}"),
        )

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return self.db.fetch_one("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        return self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))

    def update_profile(self, user_id: int, name: str, email: str) -> None:
        self.db.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name.strip(), email.lower().strip(), user_id),
        )

    def update_password(self, user_id: int, password_hash: str, password_salt: str) -> None:
        self.db.execute(
            "UPDATE users SET password_hash = ?, password_salt = ? WHERE id = ?",
            (password_hash, password_salt, user_id),
        )

    def update_settings_json(self, user_id: int, settings_json: str) -> None:
        self.db.execute(
            "UPDATE users SET settings_json = ? WHERE id = ?",
            (settings_json, user_id),
        )


@dataclass
class TestHistoryRepository:
    """Stores completed test results."""

    db: Database

    def add(
        self,
        user_id: int,
        test_type: str,
        result_type: str,
        score_json: str,
        answers_json: str,
        created_at: Optional[str] = None,
    ) -> int:
        created_at = created_at or datetime.utcnow().isoformat()
        return self.db.execute(
            """
            INSERT INTO test_history (user_id, test_type, score_json, result_type, answers_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, test_type, score_json, result_type, answers_json, created_at),
        )

    def list_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        return self.db.fetch_all(
            "SELECT * FROM test_history WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )

    def get(self, history_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        return self.db.fetch_one(
            "SELECT * FROM test_history WHERE id = ? AND user_id = ?",
            (history_id, user_id),
        )

    def delete(self, history_id: int, user_id: int) -> None:
        self.db.execute(
            "DELETE FROM test_history WHERE id = ? AND user_id = ?",
            (history_id, user_id),
        )

    def clear_all(self, user_id: int) -> None:
        self.db.execute("DELETE FROM test_history WHERE user_id = ?", (user_id,))


@dataclass
class ArticleReadRepository:
    db: Database

    def mark_read(self, user_id: int, article_id: str, bookmarked: bool = False) -> None:
        now = datetime.utcnow().isoformat()
        self.db.execute(
            """
            INSERT INTO article_reads (user_id, article_id, bookmarked, last_read_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, article_id) DO UPDATE SET last_read_at=excluded.last_read_at
            """,
            (user_id, article_id, 1 if bookmarked else 0, now),
        )

    def toggle_bookmark(self, user_id: int, article_id: str, bookmarked: bool) -> None:
        now = datetime.utcnow().isoformat()
        self.db.execute(
            """
            INSERT INTO article_reads (user_id, article_id, bookmarked, last_read_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, article_id) DO UPDATE SET bookmarked=excluded.bookmarked, last_read_at=excluded.last_read_at
            """,
            (user_id, article_id, 1 if bookmarked else 0, now),
        )

    def get_status(self, user_id: int, article_id: str) -> Dict[str, Any]:
        row = self.db.fetch_one(
            "SELECT bookmarked, last_read_at FROM article_reads WHERE user_id = ? AND article_id = ?",
            (user_id, article_id),
        )
        if not row:
            return {"bookmarked": False, "last_read_at": None}
        return {"bookmarked": bool(row.get("bookmarked")), "last_read_at": row.get("last_read_at")}

    def list_bookmarks(self, user_id: int) -> List[str]:
        rows = self.db.fetch_all(
            "SELECT article_id FROM article_reads WHERE user_id = ? AND bookmarked = 1 ORDER BY last_read_at DESC",
            (user_id,),
        )
        return [r["article_id"] for r in rows]


@dataclass
class TestSessionRepository:
    """Stores in-progress sessions so the user can resume later."""

    db: Database

    def upsert(self, user_id: int, test_type: str, current_index: int, answers_json: str) -> None:
        now = datetime.utcnow().isoformat()
        self.db.execute(
            """
            INSERT INTO test_sessions (user_id, test_type, current_index, answers_json, started_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, test_type) DO UPDATE SET current_index=excluded.current_index, answers_json=excluded.answers_json, updated_at=excluded.updated_at
            """,
            (user_id, test_type, current_index, answers_json, now, now),
        )

    def get(self, user_id: int, test_type: str) -> Optional[Dict[str, Any]]:
        return self.db.fetch_one(
            "SELECT * FROM test_sessions WHERE user_id = ? AND test_type = ?",
            (user_id, test_type),
        )

    def delete(self, user_id: int, test_type: str) -> None:
        self.db.execute(
            "DELETE FROM test_sessions WHERE user_id = ? AND test_type = ?",
            (user_id, test_type),
        )

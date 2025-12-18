from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


@dataclass
class Database:
    """Thin wrapper around sqlite3 with helper methods."""

    path: Path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def initialize(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    password_salt TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    settings_json TEXT NOT NULL DEFAULT '{}'
                );

                CREATE TABLE IF NOT EXISTS test_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    test_type TEXT NOT NULL,
                    score_json TEXT NOT NULL,
                    result_type TEXT NOT NULL,
                    answers_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS article_reads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    article_id TEXT NOT NULL,
                    bookmarked INTEGER NOT NULL DEFAULT 0,
                    last_read_at TEXT NOT NULL,
                    UNIQUE(user_id, article_id),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS test_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    test_type TEXT NOT NULL,
                    current_index INTEGER NOT NULL,
                    answers_json TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(user_id, test_type),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                """
            )

    def fetch_one(self, query: str, params: Sequence[Any] = ()) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(query, params)
            row = cur.fetchone()
            return dict(row) if row else None

    def fetch_all(self, query: str, params: Sequence[Any] = ()) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(query, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]

    def execute(self, query: str, params: Sequence[Any] = ()) -> int:
        with self._connect() as conn:
            cur = conn.execute(query, params)
            conn.commit()
            return int(cur.lastrowid or 0)

    def execute_many(self, query: str, params_list: Iterable[Sequence[Any]]) -> None:
        with self._connect() as conn:
            conn.executemany(query, params_list)
            conn.commit()

    @staticmethod
    def dumps(data: Any) -> str:
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def loads(data: str) -> Any:
        try:
            return json.loads(data)
        except Exception:
            return {}

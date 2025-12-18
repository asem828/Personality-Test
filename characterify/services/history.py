from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from characterify.db.database import Database
from characterify.db.repositories import TestHistoryRepository
from characterify.utils.paths import AppPaths


@dataclass
class HistoryService:
    db: Database
    paths: AppPaths

    def __post_init__(self) -> None:
        self.repo = TestHistoryRepository(self.db)

    def export_json(self, user_id: int) -> Path:
        now = datetime.utcnow().isoformat().replace(":", "").replace("-", "")
        out = self.paths.exports_dir / f"history_{user_id}_{now}.json"
        rows = self.repo.list_by_user(user_id)
        out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        return out

    def export_csv(self, user_id: int) -> Path:
        now = datetime.utcnow().isoformat().replace(":", "").replace("-", "")
        out = self.paths.exports_dir / f"history_{user_id}_{now}.csv"
        rows = self.repo.list_by_user(user_id)
        fields = ["id", "test_type", "result_type", "created_at"]
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for r in rows:
                writer.writerow({k: r.get(k) for k in fields})
        return out

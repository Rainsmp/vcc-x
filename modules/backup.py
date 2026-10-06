from __future__ import annotations

from typing import Dict, List


class BackupManager:
    """Simple backup policy scaffold with immutable backup protection semantics."""

    def __init__(self):
        self.retention = {"daily": 7, "weekly": 4, "monthly": 6}

    def plan(self, server: str) -> Dict[str, object]:
        return {
            "server": server,
            "immutable": True,
            "retention": self.retention,
            "status": "planned",
        }

    def list_backups(self) -> List[Dict[str, object]]:
        return [{"name": "nightly-2026-10-04", "immutable": True, "status": "success"}]

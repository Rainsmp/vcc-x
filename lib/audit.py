from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


class AuditLogger:
    """Implements a simple tamper-evident audit log with hash chaining."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]\n", encoding="utf-8")

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _last_hash(self) -> str:
        try:
            items = json.loads(self.path.read_text(encoding="utf-8"))
            if items:
                return items[-1].get("hash", "")
        except json.JSONDecodeError:
            pass
        return ""

    def record(self, event: str, payload: Dict[str, Any] | None = None, request_id: str | None = None) -> Dict[str, Any]:
        payload = payload or {}
        timestamp = datetime.now(timezone.utc).isoformat()
        previous_hash = self._last_hash()
        record = {
            "timestamp": timestamp,
            "event": event,
            "request_id": request_id,
            "payload": payload,
            "previous_hash": previous_hash,
        }
        record["hash"] = self._hash(json.dumps(record, sort_keys=True, separators=(",", ":")))
        items = []
        if self.path.exists():
            try:
                existing = json.loads(self.path.read_text(encoding="utf-8"))
                items = existing if isinstance(existing, list) else []
            except json.JSONDecodeError:
                items = []
        items.append(record)
        self.path.write_text(json.dumps(items, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return record

    def read_events(self) -> List[Dict[str, Any]]:
        try:
            items = json.loads(self.path.read_text(encoding="utf-8"))
            return items if isinstance(items, list) else []
        except json.JSONDecodeError:
            return []

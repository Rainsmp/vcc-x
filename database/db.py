from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List


class DatabaseManager:
    """Small SQLite database for job, audit, and incident records."""

    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else Path(__file__).resolve().parents[1] / "vcc.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT UNIQUE,
                    name TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    payload TEXT,
                    status TEXT NOT NULL DEFAULT 'queued'
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event TEXT NOT NULL,
                    payload TEXT,
                    request_id TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'open',
                    payload TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def insert_job(self, job_id: str, name: str, priority: str, payload: Dict[str, Any], status: str = "queued") -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO jobs (job_id, name, priority, payload, status) VALUES (?, ?, ?, ?, ?)",
                (job_id, name, priority, repr(payload), status),
            )
            conn.commit()

    def list_jobs(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()
            return [dict(row) for row in rows]

    def insert_audit(self, event: str, payload: Dict[str, Any], request_id: str | None = None) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO audit (event, payload, request_id) VALUES (?, ?, ?)",
                (event, repr(payload), request_id),
            )
            conn.commit()

    def list_audit(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM audit ORDER BY id DESC").fetchall()
            return [dict(row) for row in rows]

    def insert_incident(self, title: str, severity: str, payload: Dict[str, Any], status: str = "open") -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO incidents (title, severity, status, payload) VALUES (?, ?, ?, ?)",
                (title, severity, status, repr(payload)),
            )
            conn.commit()

    def list_incidents(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()
            return [dict(row) for row in rows]

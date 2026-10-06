from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class Job:
    name: str
    priority: str = "NORMAL"
    payload: Dict[str, Any] | None = None
    job_id: str | None = None
    status: str = "queued"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if self.payload is None:
            self.payload = {}
        if self.job_id is None:
            self.job_id = f"JOB-{abs(hash(self.name + self.created_at)) % 1000000:06d}"


class JobEngine:
    """A small, explicit job scheduler with queue semantics."""

    def __init__(self):
        self.jobs: List[Job] = []

    def submit(self, job: Job) -> Job:
        self.jobs.append(job)
        return job

    def run_next(self) -> Dict[str, Any]:
        if not self.jobs:
            return {"status": "empty"}
        job = self.jobs.pop(0)
        job.status = "completed"
        result = {
            "job_id": job.job_id,
            "name": job.name,
            "status": job.status,
            "priority": job.priority,
            "payload": job.payload,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
        return result

    def pending(self) -> List[Job]:
        return list(self.jobs)

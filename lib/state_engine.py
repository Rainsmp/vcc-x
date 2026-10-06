from __future__ import annotations

from typing import Any, Dict


class StateEngine:
    """Represent desired and observed state and detect drift."""

    def __init__(self):
        self.desired: Dict[str, Any] = {}
        self.observed: Dict[str, Any] = {}

    def set_desired(self, key: str, value: Any) -> None:
        self.desired[key] = value

    def set_observed(self, key: str, value: Any) -> None:
        self.observed[key] = value

    def is_drifted(self, key: str) -> bool:
        if key not in self.desired and key not in self.observed:
            return False
        if key not in self.desired:
            return True
        if key not in self.observed:
            return True
        return self.desired[key] != self.observed[key]

    def reconcile(self, key: str) -> Dict[str, Any]:
        desired = self.desired.get(key)
        observed = self.observed.get(key)
        if desired == observed:
            return {"key": key, "status": "aligned", "desired": desired, "observed": observed}
        return {
            "key": key,
            "status": "drift",
            "desired": desired,
            "observed": observed,
            "diff": {"desired": desired, "observed": observed},
        }

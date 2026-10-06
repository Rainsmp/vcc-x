from __future__ import annotations

import re
from typing import Any, Dict, List


def redact_sensitive(value: str) -> str:
    if not value:
        return value
    patterns = [
        (r"(Authorization:\s*)(Bearer\s+)?[A-Za-z0-9._~+\-/]+=*", r"\1[REDACTED]"),
        (r"(token\s*[:=]\s*)([A-Za-z0-9._~+\-/]+)", r"\1[REDACTED]"),
        (r"(password\s*[:=]\s*)([^\s,;]+)", r"\1[REDACTED]"),
        (r"(api[_-]?key\s*[:=]\s*)([^\s,;]+)", r"\1[REDACTED]"),
    ]
    text = value
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


class PolicyEngine:
    """A lightweight policy engine for approval and write protection."""

    def __init__(self):
        self.rules = [
            {"when": {"environment": "production", "action": "delete"}, "effect": "require_two_person_approval"},
            {"when": {"disk_usage": ">=", "value": 90}, "effect": "deny_large_backup"},
        ]

    def evaluate(self, context: Dict[str, Any]) -> List[str]:
        effects: List[str] = []
        for rule in self.rules:
            when = rule["when"]
            matches = True
            for key, expected in when.items():
                if key == "environment":
                    matches = matches and context.get("environment") == expected
                elif key == "action":
                    matches = matches and context.get("action") == expected
                elif key == "disk_usage":
                    threshold = context.get("disk_usage", 0)
                    matches = matches and threshold >= expected if expected == ">=" else threshold <= expected
            if matches:
                effects.append(rule["effect"])
        return effects


class AuthorizationManager:
    """Role-based access with explicit action protection."""

    def __init__(self):
        self.roles = {
            "admin": {"all": True},
            "operator": {"status": True, "health": True, "jobs": True},
            "auditor": {"audit": True, "incidents": True},
        }

    def authorize(self, role: str, action: str) -> bool:
        policy = self.roles.get(role, {})
        return policy.get("all", False) or action in policy

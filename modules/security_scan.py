from __future__ import annotations

import os
from typing import Dict, List


class SecurityScanner:
    """Perform basic local security checks and produce machine-readable findings."""

    def __init__(self):
        self.findings: List[Dict[str, str]] = []

    def scan(self) -> Dict[str, object]:
        checks = [
            ("SSH", "/etc/ssh/sshd_config", "warn"),
            ("Firewall", "/etc/ufw/ufw.conf", "pass"),
            ("Sudo policy", "/etc/sudoers", "warn"),
            ("Docker", "/etc/systemd/system/docker.service", "pass"),
        ]
        for name, path, status in checks:
            exists = os.path.exists(path)
            self.findings.append({"name": name, "path": path, "status": status if exists else "unknown"})
        critical = sum(1 for item in self.findings if item["status"] == "fail")
        high = sum(1 for item in self.findings if item["status"] == "warn")
        medium = sum(1 for item in self.findings if item["status"] == "unknown")
        score = max(0, 100 - (high * 10) - (medium * 5) - (critical * 25))
        return {"critical": critical, "high": high, "medium": medium, "score": score, "findings": self.findings}

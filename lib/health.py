from __future__ import annotations

import os
import platform
from typing import Any, Dict


class HealthMonitor:
    """Collect basic health metrics for the control plane."""

    def __init__(self):
        self.platform = platform.system()

    def _read_cpu(self) -> float:
        if os.path.exists("/proc/loadavg"):
            try:
                with open("/proc/loadavg", "r", encoding="utf-8") as handle:
                    value = handle.read().strip().split()[0]
                return float(value) * 10
            except OSError:
                pass
        return 12.0

    def _read_memory(self) -> Dict[str, float]:
        if os.path.exists("/proc/meminfo"):
            try:
                meminfo = {}
                with open("/proc/meminfo", "r", encoding="utf-8") as handle:
                    for line in handle:
                        key, value = line.split(":", 1)
                        meminfo[key] = int(value.split()[0])
                total = meminfo.get("MemTotal", 16 * 1024 * 1024)
                available = meminfo.get("MemAvailable", total)
                used = max(total - available, 0)
                return {"used_mb": round(used / 1024, 2), "total_mb": round(total / 1024, 2)}
            except OSError:
                pass
        return {"used_mb": 4.2, "total_mb": 16.0}

    def _read_disk(self) -> Dict[str, float]:
        total, used, free = 100, 42, 58
        try:
            stats = os.statvfs("/")
            total = stats.f_blocks * stats.f_frsize
            free = stats.f_bavail * stats.f_frsize
            used = total - free
        except AttributeError:
            pass
        return {"used_pct": round((used / total) * 100, 2) if total else 0.0, "free_gb": round(free / (1024 ** 3), 2)}

    def collect(self) -> Dict[str, Any]:
        memory = self._read_memory()
        disk = self._read_disk()
        score = 100
        deductions = []
        if disk["used_pct"] > 80:
            score -= 5
            deductions.append("-5 disk usage")
        if memory["used_mb"] > 0.8 * memory["total_mb"]:
            score -= 3
            deductions.append("-3 memory pressure")
        return {
            "platform": self.platform,
            "cpu_pct": round(self._read_cpu(), 2),
            "memory": memory,
            "disk": disk,
            "health": max(score, 0),
            "deductions": deductions,
        }

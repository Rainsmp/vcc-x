from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class FleetServer:
    server_id: str
    hostname: str
    ip: str
    status: str = "online"
    roles: List[str] = field(default_factory=lambda: ["GENERAL"])
    environment: str = "production"
    tags: Dict[str, str] = field(default_factory=dict)


class FleetManager:
    """Fleet registry and status summary."""

    def __init__(self):
        self.servers: List[FleetServer] = [
            FleetServer("node-01", "node-01", "10.0.0.11", "online", ["PANEL", "GENERAL"], "production", {"env": "production", "role": "panel"}),
            FleetServer("node-02", "node-02", "10.0.0.12", "online", ["NODE"], "staging", {"env": "staging", "role": "node"}),
            FleetServer("node-03", "node-03", "10.0.0.13", "warning", ["DATABASE"], "production", {"env": "production", "role": "database"}),
        ]

    def list_servers(self) -> List[Dict[str, object]]:
        data = []
        for server in self.servers:
            data.append({
                "server_id": server.server_id,
                "hostname": server.hostname,
                "ip": server.ip,
                "status": server.status,
                "roles": server.roles,
                "environment": server.environment,
                "tags": server.tags,
            })
        return data

    def count_by_status(self) -> Dict[str, int]:
        counts = {"online": 0, "warning": 0, "offline": 0}
        for server in self.servers:
            counts[server.status] = counts.get(server.status, 0) + 1
        return counts

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict

from api.server import start_api_server
from database.db import DatabaseManager
from lib.audit import AuditLogger
from lib.config import ConfigManager
from lib.health import HealthMonitor
from lib.job_engine import Job, JobEngine
from lib.state_engine import StateEngine
from lib.security import AuthorizationManager, PolicyEngine, redact_sensitive
from modules.fleet import FleetManager
from modules.security_scan import SecurityScanner


DEFAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def _status_command(args: argparse.Namespace) -> int:
    config = ConfigManager(DEFAULT_ROOT)
    fleet = FleetManager()
    health = HealthMonitor().collect()
    status = {
        "controller": config.get("controller.name"),
        "environment": config.get("controller.environment"),
        "fleet": fleet.count_by_status(),
        "health": health,
    }
    _print_json(status)
    return 0


def _health_command(args: argparse.Namespace) -> int:
    health = HealthMonitor().collect()
    _print_json({"status": "ok", "health": health})
    return 0


def _servers_command(args: argparse.Namespace) -> int:
    _print_json({"servers": FleetManager().list_servers()})
    return 0


def _jobs_command(args: argparse.Namespace) -> int:
    engine = JobEngine()
    engine.submit(Job(name="health-check", priority="HIGH", payload={"server": "node-01"}))
    engine.submit(Job(name="backup-check", priority="NORMAL", payload={"server": "node-02"}))
    results = [engine.run_next(), engine.run_next()]
    _print_json({"jobs": results})
    return 0


def _security_scan_command(args: argparse.Namespace) -> int:
    scan = SecurityScanner().scan()
    _print_json({"security": scan})
    return 0


def _plan_command(args: argparse.Namespace) -> int:
    state = StateEngine()
    state.set_desired("docker", "running")
    state.set_observed("docker", "stopped")
    _print_json({"plan": state.reconcile("docker")})
    return 0


def _apply_command(args: argparse.Namespace) -> int:
    state = StateEngine()
    state.set_desired("docker", "running")
    state.set_observed("docker", "stopped")
    _print_json({"applied": True, "reconcile": state.reconcile("docker")})
    return 0


def _backup_command(args: argparse.Namespace) -> int:
    _print_json({"backup": {"status": "planned", "target": "node-01", "immutable": True}})
    return 0


def _restore_command(args: argparse.Namespace) -> int:
    _print_json({"restore": {"status": "ready", "dry_run": True}})
    return 0


def _incident_command(args: argparse.Namespace) -> int:
    audit = AuditLogger(DEFAULT_ROOT + "/audit.log")
    audit.record("incident.created", {"server": "node-03", "kind": "disk_abuse"})
    _print_json({"incident": {"status": "created", "request_id": "REQ-INC-01"}})
    return 0


def _audit_command(args: argparse.Namespace) -> int:
    audit = AuditLogger(DEFAULT_ROOT + "/audit.log")
    _print_json({"audit": audit.read_events()[-5:]})
    return 0


def _api_command(args: argparse.Namespace) -> int:
    start_api_server(args.host, args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VPS Control Center X")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ["status", "health", "servers", "jobs", "security-scan", "plan", "apply", "backup", "restore", "incident", "audit", "api"]:
        subparsers.add_parser(name, help=f"Run {name}")

    api_parser = subparsers.choices["api"]
    api_parser.add_argument("--host", default="127.0.0.1")
    api_parser.add_argument("--port", type=int, default=8080)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "status":
        return _status_command(args)
    if args.command == "health":
        return _health_command(args)
    if args.command == "servers":
        return _servers_command(args)
    if args.command == "jobs":
        return _jobs_command(args)
    if args.command == "security-scan":
        return _security_scan_command(args)
    if args.command == "plan":
        return _plan_command(args)
    if args.command == "apply":
        return _apply_command(args)
    if args.command == "backup":
        return _backup_command(args)
    if args.command == "restore":
        return _restore_command(args)
    if args.command == "incident":
        return _incident_command(args)
    if args.command == "audit":
        return _audit_command(args)
    if args.command == "api":
        return _api_command(args)

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

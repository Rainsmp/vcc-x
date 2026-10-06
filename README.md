# VPS CONTROL CENTER X

VCC-X is a lightweight infrastructure control plane for responsibly managing Linux VPS infrastructure. It is designed around security, approval gates, audit logging, drift detection, and operational safety. The project provides a working CLI, modular policy and job logic, and a foundation that can be extended with additional infrastructure integrations.

## Goals

- Keep the control plane separate from the data plane.
- Support secure, policy-driven execution with approval checks.
- Maintain audit integrity and state reconciliation.
- Provide a real command-line interface and an API foundation.
- Make unsafe operations explicit and reviewable.

## Directory structure

- lib/ — reusable core logic and helpers
- modules/ — infrastructure subsystems
- database/ — SQLite-backed persistence
- api/ — HTTP API foundation
- config/ — default configuration
- tests/ — unit tests
- runbooks/ — operational procedures

## Quick start

```bash
python vcc status
python vcc health
python vcc servers
python vcc security-scan
python vcc jobs
```

## Basic CLI commands

- `vcc status`
- `vcc health`
- `vcc jobs`
- `vcc servers`
- `vcc security-scan`
- `vcc plan`
- `vcc apply`
- `vcc backup`
- `vcc restore`
- `vcc incident`
- `vcc audit`
- `vcc api` (starts the local API)

## Safety principles

1. Policy evaluation before execution.
2. Approval for high-risk actions.
3. Request IDs and audit provenance.
4. Reversible changes and rollback support.
5. Drift and health checks before self-healing.

## Status

This repository is an implementation scaffold for a serious control plane. It includes real executable logic for the core control-plane concerns and intentionally avoids fake metrics or unsafe automation. Advanced integrations such as Cloudflare, Docker, Pterodactyl, and Discord are represented as explicit interfaces and structured modules rather than fabricated success responses.

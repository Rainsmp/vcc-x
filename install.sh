#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

printf '[VCC-X] Installing from %s\n' "$ROOT_DIR"

mkdir -p "$ROOT_DIR/.install"

chmod +x "$ROOT_DIR/vcc" 2>/dev/null || true

printf '[VCC-X] Installation complete.\n'

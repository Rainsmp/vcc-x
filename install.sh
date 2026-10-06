#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR

require_command() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 1; }
}

main() {
  require_command python3
  if [[ -f "$ROOT_DIR/VERSION" ]]; then
    echo "Installing VCC-X from $ROOT_DIR"
  fi

  install -d "$ROOT_DIR/.install"
  mkdir -p "$ROOT_DIR/config" "$ROOT_DIR/lib" "$ROOT_DIR/modules" "$ROOT_DIR/database" "$ROOT_DIR/api"
  chmod 700 "$ROOT_DIR" || true
  echo "VCC-X installation scaffold complete."
}

main "$@"

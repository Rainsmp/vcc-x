#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR

main() {
  echo "This will remove VCC-X project files from: $ROOT_DIR"
  read -r -p "Continue? [y/N] " response
  case "$response" in
    [yY]|[yY][eE][sS])
      rm -rf "$ROOT_DIR/.install" "$ROOT_DIR/__pycache__" "$ROOT_DIR/tests/__pycache__" 2>/dev/null || true
      echo "VCC-X uninstall scaffold complete."
      ;;
    *)
      echo "Uninstall cancelled."
      ;;
  esac
}

main "$@"

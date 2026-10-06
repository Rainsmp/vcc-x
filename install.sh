#!/usr/bin/env bash
set -Eeuo pipefail

SOURCE="${BASH_SOURCE[0]}"

case "$SOURCE" in
    /dev/fd/*|/proc/*/fd/*)
        command -v git >/dev/null 2>&1 || {
            printf '[VCC-X] Error: git is required.\n' >&2
            exit 1
        }

        TMP_DIR="$(mktemp -d)"
        trap 'rm -rf -- "$TMP_DIR"' EXIT

        printf '[VCC-X] Remote execution detected.\n'
        printf '[VCC-X] Downloading VCC-X...\n'

        git clone --depth 1 \
            "https://github.com/Rainsmp/vcc-x.git" \
            "$TMP_DIR/vcc-x"

        exec bash "$TMP_DIR/vcc-x/install.sh"
        ;;

    *)
        ROOT_DIR="$(cd -- "$(dirname -- "$SOURCE")" && pwd)"

        printf '[VCC-X] Installing from %s\n' "$ROOT_DIR"

        mkdir -p "$ROOT_DIR/.install"

        chmod +x "$ROOT_DIR/vcc" 2>/dev/null || true

        printf '[VCC-X] Installation complete.\n'
        ;;
esac

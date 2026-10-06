#!/usr/bin/env bash
set -Eeuo pipefail

REPO="https://github.com/Rainsmp/vcc-x.git"
INSTALL_DIR="${VCC_INSTALL_DIR:-$HOME/.vcc-x}"

printf '[VCC-X] Downloading VCC-X...\n'

command -v git >/dev/null 2>&1 || {
    printf '[VCC-X] Error: git is required.\n' >&2
    exit 1
}

if [ -d "$INSTALL_DIR/.git" ]; then
    printf '[VCC-X] Updating existing installation...\n'
    git -C "$INSTALL_DIR" pull --ff-only
else
    rm -rf "$INSTALL_DIR"
    git clone --depth 1 "$REPO" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

chmod +x install.sh vcc

bash ./install.sh

printf '[VCC-X] Ready.\n'
printf '[VCC-X] Run: %s/vcc status\n' "$INSTALL_DIR"

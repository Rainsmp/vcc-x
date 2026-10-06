#!/usr/bin/env bash
set -Eeuo pipefail

INSTALL_DIR="${VCC_INSTALL_DIR:-$HOME/.vcc-x}"

printf '%s\n' "VCC-X Uninstaller"
printf '%s\n' "Installation: $INSTALL_DIR"
printf '\n'

if [ ! -d "$INSTALL_DIR" ]; then
    printf '%s\n' "VCC-X installation not found."
    exit 0
fi

# Safety checks: never allow dangerous paths.
case "$INSTALL_DIR" in
    ""|"/"|"$HOME"|"$HOME/"|"/home"|"/root")
        printf '%s\n' "ERROR: Refusing to remove unsafe path: $INSTALL_DIR" >&2
        exit 1
        ;;
esac

printf 'This will permanently remove:\n'
printf '  %s\n\n' "$INSTALL_DIR"

read -r -p "Continue? [y/N] " response

case "$response" in
    y|Y|yes|YES|Yes)
        rm -rf -- "$INSTALL_DIR"
        printf '\n[VCC-X] Uninstalled successfully.\n'
        ;;
    *)
        printf '\n[VCC-X] Uninstall cancelled.\n'
        ;;
esac

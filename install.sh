#!/usr/bin/env bash
# Link (or copy) the /swap-ui command and its script into ~/.claude.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
claude_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
command_dst="$claude_dir/commands/swap-ui.md"
script_dst="$claude_dir/scripts/swap-claude-ui.py"

mode="link"
case "${1:-}" in
  --copy) mode="copy" ;;
  --uninstall) mode="uninstall" ;;
  "") ;;
  *) echo "Usage: install.sh [--copy|--uninstall]" >&2; exit 1 ;;
esac

if [[ "$mode" == "uninstall" ]]; then
  rm -f "$command_dst" "$script_dst"
  echo "Removed $command_dst"
  echo "Removed $script_dst"
  exit 0
fi

mkdir -p "$claude_dir/commands" "$claude_dir/scripts"

install_one() {
  local src="$1" dst="$2"
  if [[ -e "$dst" && ! -L "$dst" ]]; then
    cp "$dst" "$dst.bak"
    echo "Backed up existing $dst to $dst.bak"
  fi
  rm -f "$dst"
  if [[ "$mode" == "copy" ]]; then
    cp "$src" "$dst"
  else
    ln -s "$src" "$dst"
  fi
  echo "Installed $dst"
}

install_one "$repo/commands/swap-ui.md" "$command_dst"
install_one "$repo/scripts/swap-claude-ui.py" "$script_dst"
chmod +x "$script_dst"

echo
echo "Done. Run /swap-ui in Claude Code, or:"
echo "  python3 $script_dst [terminal|native|toggle]"

#!/usr/bin/env python3
"""Toggle the VS Code Claude Code extension between terminal and native UI.

Flips `claudeCode.useTerminal` in the VS Code user settings.json.
Usage: swap-claude-ui.py [terminal|native]   (no arg = toggle)
"""

import json
import re
import sys
from pathlib import Path

KEY = "claudeCode.useTerminal"

CANDIDATES = [
    Path.home() / "Library/Application Support/Code/User/settings.json",
    Path.home() / "Library/Application Support/Code - Insiders/User/settings.json",
    Path.home() / ".config/Code/User/settings.json",
    Path.home() / "AppData/Roaming/Code/User/settings.json",
]


def settings_path() -> Path:
    for path in CANDIDATES:
        if path.exists():
            return path
    sys.exit("Could not find VS Code user settings.json in any known location.")


def target_state(current: bool) -> bool:
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else None
    if arg in (None, "toggle"):
        return not current
    if arg in ("terminal", "term", "cli", "true"):
        return True
    if arg in ("native", "ui", "panel", "false"):
        return False
    sys.exit(f"Unknown argument {arg!r}. Use: terminal | native | toggle")


def main() -> None:
    path = settings_path()
    text = path.read_text()

    # Read the current value with a real JSON parse so a commented-out or
    # duplicated key can't be mistaken for the effective setting.
    try:
        current = bool(json.loads(text).get(KEY, False))
    except json.JSONDecodeError as err:
        sys.exit(f"{path} is not valid JSON ({err}); fix it before toggling.")

    wanted = target_state(current)
    if wanted == current:
        print(f"Already in {'terminal' if current else 'native'} mode; nothing to do.")
        return

    # Rewrite in place rather than round-tripping through json.dump, which would
    # reformat the whole file.
    pattern = re.compile(rf'("{re.escape(KEY)}"\s*:\s*)(true|false)')
    if pattern.search(text):
        new_text = pattern.sub(rf'\g<1>{str(wanted).lower()}', text, count=1)
    else:
        new_text = re.sub(
            r"^\s*\{",
            '{\n  "%s": %s,' % (KEY, str(wanted).lower()),
            text,
            count=1,
        )

    json.loads(new_text)  # Refuse to write anything we just broke.
    path.write_text(new_text)

    mode = "terminal" if wanted else "native UI"
    print(f"{KEY} = {str(wanted).lower()} -> Claude now launches in the {mode}.")
    print(f"Updated {path}")


if __name__ == "__main__":
    main()

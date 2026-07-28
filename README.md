# claude-swap-ui

A `/swap-ui` slash command for [Claude Code](https://claude.com/claude-code) that
switches the VS Code extension between the **terminal** UI and the **native**
panel, without hand-editing `settings.json`.

It flips `claudeCode.useTerminal` in your VS Code user settings, in place, so
the rest of the file (comments, formatting, key order) is left alone.

## Install

```sh
git clone https://github.com/<you>/claude-swap-ui.git
cd claude-swap-ui
./install.sh
```

`install.sh` symlinks the command and script into `~/.claude/`, so pulling new
commits updates your install with no extra step. Pass `--copy` if you'd rather
have real files than symlinks.

Uninstall with `./install.sh --uninstall`.

## Usage

Inside Claude Code:

```
/swap-ui             # toggle
/swap-ui terminal    # force terminal mode
/swap-ui native      # force native panel
```

Or straight from a shell:

```sh
python3 ~/.claude/scripts/swap-claude-ui.py [terminal|native|toggle]
```

Accepted aliases: `terminal` / `term` / `cli` / `true`, and
`native` / `ui` / `panel` / `false`.

## After swapping

The setting takes effect for the *next* session you open; the one you're
sitting in stays as it is.

- Switched to terminal: press `Cmd+Escape` (bound to
  `claude-vscode.terminal.open`) or run **Claude Code: Open in Terminal**.
- Switched to native: reopen Claude from the sidebar, or `Cmd+Escape`.

## Settings file locations

The script uses the first of these that exists:

| Platform | Path |
| --- | --- |
| macOS | `~/Library/Application Support/Code/User/settings.json` |
| macOS (Insiders) | `~/Library/Application Support/Code - Insiders/User/settings.json` |
| Linux | `~/.config/Code/User/settings.json` |
| Windows | `~/AppData/Roaming/Code/User/settings.json` |

## Safety

- The current value is read with a real JSON parse, so a commented-out or
  duplicated key can't be mistaken for the effective setting.
- The rewritten text is re-parsed before it is written; if the edit would
  produce invalid JSON, nothing is saved.
- A no-op swap (already in the requested mode) exits without touching the file.

## Requirements

Python 3.8+ and VS Code with the Claude Code extension. No third-party
dependencies.

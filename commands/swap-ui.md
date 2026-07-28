---
description: Swap Claude Code in VS Code between terminal and native UI
allowed-tools: Bash(python3 ~/.claude/scripts/swap-claude-ui.py:*)
argument-hint: "[terminal|native]  (omit to toggle)"
---

Run this, then report the resulting mode to the user in one line:

```
python3 ~/.claude/scripts/swap-claude-ui.py $ARGUMENTS
```

If it switched to terminal mode, remind the user: the currently open native
session stays open; press `Cmd+Escape` (now bound to
`claude-vscode.terminal.open`) or run **Claude Code: Open in Terminal** to get a
terminal session.

If it switched to native mode, remind them to reopen Claude from the sidebar or
`Cmd+Escape` to get the native panel back.

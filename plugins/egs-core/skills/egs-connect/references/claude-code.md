# Claude Code, this skill and Python

**What it gives:** the daily sweep that starts by itself, the readers for Plutio, Chat, Search
Console and Analytics, and drafts saved on their computer. **Time:** about 15 minutes.

## Before you start

- Their EGS Claude Team invite accepted, signed in with their egs-solutions.com email.
- Which role plugin is theirs: their profile in the egs skill says ("Role plugin to install").

## Walk-through

1. **VS Code.** Install it from code.visualstudio.com if they do not have it.
2. **Git.** Mac: run `git --version` in the terminal; if it asks to install developer tools, accept.
   Windows: install Git for Windows from git-scm.com with the default options (Claude Code on Windows
   needs it).
3. **Python 3.9 or newer.** Run `python3 --version` (Windows: `python --version`). If missing, install
   from python.org. On Windows, tick "Add python.exe to PATH" on the first installer screen.
4. **Claude Code.** In VS Code, open Extensions, search "Claude Code", install the one published by
   Anthropic, then sign in with the EGS Claude account when it asks.
5. **Get the EGS skills.** If the owner has synced EGS's skills to the Claude Team account, they
   appear by themselves in Claude Code once signed in (as plugins ending in `@synced`): open
   `/plugin`, Installed, and make sure **egs-core** and their role plugin are on. If not synced yet,
   in Claude Code run `/plugin marketplace add EGS-Marketing-Solutions/egs-skills`, then
   `/plugin install egs-core@egs` and their role plugin, for example `/plugin install egs-seo@egs`.
   A private repository needs their GitHub sign-in on this computer first: `gh auth login`, then
   `gh auth setup-git`.
6. **Install the readers' libraries.** Run the install command shown in the egs-connect skill (it
   points at the plugin's own folder).
7. **Restart Claude Code** (close and reopen VS Code). The daily sweep and the read-only guard now
   run in every folder.

## Check

`egs.py check` runs. Their next first-message-of-the-day starts the sweep. `/plugin` lists egs-core and their role plugin as enabled.

## Updates

Synced plugins update by themselves. Otherwise, when Kyle announces an update: `/plugin`,
Installed, Update now on each EGS plugin (or `claude plugin update egs-core@egs`).

## If it fails

- "python3: command not found" on Windows: use `python`, or `py`.
- "No module named googleapiclient": step 6 did not run in the same Python; run it again with the
  exact Python the error names.
- The sweep never starts: check that `~/.config/egs-assistant/sweep-off` does not exist, and that
  egs-core shows as enabled under `/plugin`, Installed.

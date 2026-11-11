---
name: egs-connect
description: Walks an EGS team member through connecting Claude to every tool EGS uses - Plutio (including creating their API key), Google Chat, Gmail, Drive, Calendar, Search Console, Analytics, PageSpeed, Fathom, Meta, Canva, Slack and Amplify - one step at a time, and checks each connection. Use it the first time someone uses the EGS skills, when they say set me up or connect my tools, when a tool is not working, when the sweep says a channel was not checked, or when anyone needs an API key or sign-in explained. Also has the owner's one-time setup.
---

# Connecting your person's tools

Use this when someone is new, when `egs.py check` shows something missing, or when they ask to
connect a tool. You are the guide: they click, you explain and check.

## How to walk someone through it

- **One step at a time.** Give one instruction, wait for them to say it is done, then the next. Say
  where on screen to look ("top right, the gear icon"). If what they see differs from the guide,
  ask them to describe it and adapt; menus move.
- **Never take a secret in the chat.** API keys, client secrets and passwords go into a file on
  their computer that they edit themselves, or into the sign-in page itself. If they paste one into
  the chat anyway, tell them to delete that key and make a new one, and do not repeat it.
- **Check every connection** right after it is made, and say which account it is signed in as. A
  tool connected to a personal account instead of the egs-solutions.com one is worse than no
  connection, because the sweep looks complete when it is not.
- **Read-only.** Where a tool offers a choice of access, choose read-only.
- **Finish with a table:** each tool, connected or not, signed in as whom, what is left.

## What each role connects

| Tool | Guide | Everyone | Extra for |
|---|---|---|---|
| Claude Code, this skill, Python | `references/claude-code.md` | yes | |
| Who you are | below | yes | |
| Gmail, Google Drive, Google Calendar | `references/google-workspace.md` | yes | |
| Google sign-in for Chat, Search Console, Analytics | `references/google-signin.md` | yes (Chat) | SEO, account managers, owner (Search Console and Analytics) |
| Plutio | `references/plutio.md` | yes | |
| Fathom (call recordings) | `references/fathom.md` | | anyone who records client calls in Fathom |
| Meta (Facebook and Instagram) | `references/meta.md` | | social, account managers with ads clients, owner |
| Canva | `references/canva.md` | | social, content |
| PageSpeed Insights key | `references/pagespeed.md` | | SEO, websites |
| SEO access (Search Console, Analytics, Business Profile, Tag Manager, Duda, Search Atlas) | `references/seo-access.md` | | SEO |
| Amplify (HighLevel) | `references/amplify.md` | | Amplify manager, only after the owner's decision |
| Slack | `references/slack.md` | | anyone in partner Slack spaces |

The owner does a few things once for everyone: the egs-connect skill's `references/owner-setup.md`.

## Commands this plugin provides

- Readers: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/egs.py" <command>` (Windows: `python`). Below and
  in the guides, `egs.py` means this.
- Install the readers' libraries once: `python3 -m pip install -r "${CLAUDE_PLUGIN_ROOT}/scripts/requirements.txt"`
  (on a Mac that says "externally managed environment", add `--user`).

## Order

Claude Code and this skill first, then who they are, then Google Workspace, then the Google sign-in,
then Plutio, then their role's extras. Each later step depends on the earlier ones.

## Who they are

Ask their name exactly as Plutio shows it, then run:

```
egs.py setup --me "First Last"
```

This creates their private settings folder, `~/.config/egs-assistant/` (on Windows
`C:\Users\<them>\.config\egs-assistant\`), with `me.json` and an empty `plutio.json`. If their
profile lists "Boards I watch", add them: `egs.py setup --me "First Last" --watch "SEO Task Board"`
(repeat `--watch` for each). Unassigned work in those boards then appears in their sweep. Then open their
profile in the egs skill's `references/team/<first-name>.md` and, with their Plutio tasks
(`egs.py plutio sweep --json`) and the last meeting recap, propose corrections to "Clients I own" and
the routines. They send the change to Kyle.

## In claude.ai instead of Claude Code

The skill works in claude.ai (Customize > Skills > upload), but the readers in `scripts/` cannot
reach Plutio or Google Chat from there. Connect Gmail, Drive, Calendar and the role extras as
connectors; Plutio and Chat then reach Claude only through their notification emails. For the full
sweep, use Claude Code.

## When something breaks

Run `egs.py check`. Then the "If it fails" section of that tool's guide. If it is still broken, the
person tells Kyle in the team space with the exact message they saw.

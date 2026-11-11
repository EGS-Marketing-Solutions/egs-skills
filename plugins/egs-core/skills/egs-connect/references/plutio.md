# Plutio

**What it gives:** Claude reads every task, comment and file the person can see: what is waiting on
them, what is due, what a client said on a task. **Time:** 5 minutes. **Needs an API key**, which
they create themselves.

## Walk-through

1. In Plutio (clientportal.egs-solutions.com), signed in as themselves, open Settings (top right),
   then **API manager**.
2. Create a new API client. Any name, for example "Claude, <their first name>".
3. Plutio shows a **client id** and a **client secret**. The secret appears once, so keep the page
   open.
4. Have them open their settings file in a plain text editor (Windows Notepad, Mac TextEdit in plain
   text mode, or VS Code): `~/.config/egs-assistant/plutio.json`. If it does not exist, run
   `egs.py setup --me "First Last"` first.
5. They paste the id and the secret between the quotes, so it looks like
   `{"client_id": "…", "client_secret": "…"}`, and save. They paste it there, never in the chat.
6. Run `egs.py check`.

## Check

`plutio  OK  signed in; you are in Plutio's people list`. Then `egs.py plutio sweep` lists their
tasks. If check says their name was not found, fix the name in `me.json` to match Plutio exactly.

## If it fails

- API manager is not in their settings: members may not have it switched on. The owner either
  enables it or creates a client and sends it to them privately (the egs-connect skill's `references/owner-setup.md`).
- "invalid_client" or "rejected": the id or secret was pasted with a missing character or extra
  space. Create a new client and paste again.
- Timeouts: Plutio is slow at times; the reader retries on its own. Run it again in a minute.

## Read-only

The reader only reads. Stage comments, tasks and replies are posted by the person in Plutio; Claude
writes the text for them to paste.

## Remove access

Plutio > Settings > API manager, delete the client. Then clear `plutio.json`.

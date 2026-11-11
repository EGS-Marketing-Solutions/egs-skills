# Gmail, Google Drive, Google Calendar

**What it gives:** the inbox, client folders and sheets, and the calendar, read by Claude.
**Time:** 5 minutes. **No API keys:** these are Claude connectors with a normal Google sign-in.

## Walk-through

1. Open claude.ai in the browser, signed in with the EGS Claude account.
2. Customize > Connectors. Find Gmail and click Connect.
3. Google asks which account: choose the **egs-solutions.com** one, not a personal account. Allow.
4. Repeat for Google Drive and Google Calendar, same account.
5. If a connector is not in the list, the owner has not enabled it for the organisation yet
   (the egs-connect skill's `references/owner-setup.md`).

These connectors also appear in Claude Code once they are signed in with the same Claude account.

## Check

Search their inbox for one recent email and confirm the address on it is @egs-solutions.com. List
recent Drive files and confirm client folders appear. If either shows a personal account, have them
disconnect it (Customize > Connectors > the connector > Disconnect) and connect again with the EGS
account.

## Read-only

These connectors include tools that send, draft, move and share. This setup does not use them; the
installer blocks them in Claude Code. The person sends from Gmail themselves.

## If it fails

- "This app is blocked" from Google: the owner's Workspace admin settings restrict third-party
  apps; the owner allows Claude in the Google Admin console.
- Only one Google account per Claude account: if they connected the wrong one first, disconnect and
  reconnect.

# Google sign-in for Chat, Search Console and Analytics

**What it gives:** Claude reads Google Chat (team spaces, client spaces, meeting recaps), and, for
those who have access, Search Console and Google Analytics. One sign-in covers all three, read-only.
**Time:** 5 minutes.

## Before you start

- The team's Google sign-in file, `google-client.json`, from Kyle or the owner (made once, see
  the egs-connect skill's `references/owner-setup.md`). It is shared privately, never in the repository.
- For Search Console and Analytics: their Google account must already have access to the client
  properties. Ask whoever owns each property to add them:
  - Search Console: Settings > Users and permissions > Add user, permission "Restricted" is enough.
  - Analytics: Admin > Property access management > Add users, role "Viewer" is enough.

## Walk-through

1. Have them save `google-client.json` into their settings folder, `~/.config/egs-assistant/`
   (Windows: `C:\Users\<them>\.config\egs-assistant\`). Do not open or print the file.
2. Run `egs.py google auth`. A browser tab opens.
3. They choose their **egs-solutions.com** account.
4. Google lists what is being allowed: view Chat spaces, messages and members, view Search Console
   data, view Analytics data. All are view-only. They click Allow.
5. The tab says the sign-in finished; they can close it.

## Check

`egs.py check` shows OK for google chat, search console and analytics. Then `egs.py chat spaces`
lists their spaces, `egs.py gsc sites` lists the sites they can see, and `egs.py ga properties`
lists their properties. An empty list for Search Console or Analytics means nobody has given their
account access yet; that is fixed in those products, not here.

## If it fails

- "Access blocked" or "app not verified": they picked a personal account, or the sign-in file was
  made for a different organisation. Use the EGS account; if it persists, the owner checks
  the egs-connect skill's `references/owner-setup.md`.
- "API has not been used in project" or "is disabled": the owner enables that API in the EGS Google
  Cloud project.
- "insufficient scopes" or MISSING in check: run `egs.py google auth` again and allow everything listed.

## Remove access

Google Account > Security > Third-party connections, remove the EGS sign-in; then delete
`google-token.json` from their settings folder.

# Amplify (HighLevel)

**For:** the Amplify manager and builders, and only after the owner has decided (see
the egs-connect skill's `references/owner-setup.md`). Practice sub-accounts hold patient records, so this connector is gated.

**What it gives:** Claude reads workflows, pipelines, stages, forms, calendars and templates in the
sub-accounts the person allows, so build specs and checks match what is really there.
**Time:** 5 minutes. **No API key:** HighLevel's official connector uses a normal sign-in.

## Walk-through (once the owner has said yes)

1. claude.ai > Customize > Connectors > Add custom connector.
2. Name: Amplify. URL: `https://services.leadconnectorhq.com/mcp/anthropic/v2`. Add.
3. Connect. HighLevel's sign-in opens. They sign in with their own Amplify user.
4. On the consent screen they choose **which sub-accounts** the connection may reach. Only the ones
   the owner approved (until protected health information is cleared, the Amplify DPC agency
   sub-account and EGS's own, never a practice).
5. In Claude Code instead: `claude mcp add --transport http amplify https://services.leadconnectorhq.com/mcp/anthropic/v2`,
   then run `/mcp` and sign in.

## Check

Ask Claude to list the sub-accounts it can reach. It should show only the approved ones.

## Read-only, and no patient data

The connector can create, change and delete almost anything. Claude only runs operations that read
(search, get, list), checks each one's description before running it, and never reads contacts or
conversations in a practice sub-account. Builds are done by a person from Claude's spec.

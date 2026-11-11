# One-time setup by the owner

Done once for the whole team, by Stephani or whoever she delegates. A Claude helping the owner can
walk through these the same way it walks a team member through theirs.

## Claude Team account

- Invite every team member with their egs-solutions.com email.
- Organization settings > Plugins & skills, Policy tab: turn on code execution and "Share with
  organization".
- Organization settings > Connectors: make Gmail, Google Drive, Google Calendar, Fathom, Canva, Meta
  Ads and Slack available. Each person still signs in with their own account.
- **Sync EGS's skills to everyone:** Organization settings > Plugins & skills, add EGS's private skills
  repository, EGS-Marketing-Solutions/egs-skills (it must stay private), and make egs-core available to everyone and each role plugin to
  the people in that role. They then appear in claude.ai, Claude Desktop and Claude Code for everyone
  signed in to the Team account. Without sync, each plugin can be uploaded from the repository's
  `dist/` folder under Customize > Plugins > Upload plugin.
- The ads partner gets only **egs-ads**: it works on its own and needs no access to Plutio, Chat or the inbox.

## The team's Google sign-in file

Lets each person's Claude read Chat, Search Console and Analytics with their own Google account,
read-only. In the EGS Google Cloud project (console.cloud.google.com):

1. APIs & Services > Library: enable **Google Chat API**, **Google Search Console API**, **Google
   Analytics Data API** and **Google Analytics Admin API**.
2. Google Auth Platform > Branding: app name "EGS assistant", support email, logo optional.
3. Google Auth Platform > Audience: **Internal**, so only egs-solutions.com accounts can use it.
4. Google Auth Platform > Data Access: add the scopes `chat.spaces.readonly`,
   `chat.messages.readonly`, `chat.memberships.readonly`, `webmasters.readonly`,
   `analytics.readonly`. All view-only.
5. Google Auth Platform > Clients > Create client, type **Desktop app**, name "EGS assistant".
   Download the JSON.
6. Google Chat API > Configuration: if Google asks for an app configuration before Chat will answer,
   fill in the name "EGS assistant", an avatar URL and a description, and leave it unpublished.
7. Rename the download to `google-client.json` and share it privately with the team (a Drive file
   shared only with team members). Never in the repository, never in a Chat space with clients.

## Plutio

Each person creates their own API client under Settings > API manager. If members cannot see API
manager, enable it for them, or create one client per person and send each privately. Never put a
client secret in the repository, in Chat or in a Plutio comment.

## Amplify (HighLevel): decide before anyone connects

The official connector can read and change everything a user allows, including patient contacts
and conversations in practice sub-accounts. Decide:

- Whether EGS's Claude plan covers protected health information. Ask Anthropic whether your plan
  includes a business associate agreement. Until the answer is yes, only the Amplify DPC agency
  sub-account and EGS's own may be connected, never a practice.
- Who may connect it. Suggested: the Amplify manager and the Amplify builder.

## The repository

- EGS-Marketing-Solutions/egs-skills, private, in EGS's GitHub organisation. Team members need access only if they install from it
  directly instead of through the Team account sync.
- Changes to the skill go through a pull request reviewed by the project manager.
- Drafts, outputs and everyone's settings never reach the repository; `.gitignore` keeps them out.

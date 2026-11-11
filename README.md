# EGS skills

Claude skills for the EGS Marketing Solutions team, packaged as plugins. Everyone installs
**egs-core**; then each person adds the plugin for their role.

With them, a person's Claude:

- **connects to the tools EGS uses** and walks them through each one, including getting API keys;
- **sweeps their channels** at the start of every day (Plutio, Google Chat, Gmail, Drive, Calendar,
  meeting recaps, and Search Console and Analytics where they have access) and lists what is waiting
  on them, what needs chasing and what is due;
- **drafts the work right away**: replies, client updates, copy, reports, briefs, schema, content
  plans, scripts, task descriptions, stage comments;
- **knows their craft** through their role plugin;
- **only reads.** It never sends, posts or changes anything in any system. People do.

## The plugins

| Plugin | Who installs it | What it adds |
|---|---|---|
| egs-core | Everyone | How EGS works, the team, the daily sweep, tool connections, client updates, copy, reports, meetings to tasks, SOPs, the read-only readers and guard |
| egs-seo | SEO | SEO and AI search for practices: trackers, schema, Core Web Vitals, Google Business Profile, AI citation checks |
| egs-social | Social media | Content plans, captions, Reels and Shorts scripts, design briefs, event kits, results |
| egs-content | Writers | Blogs, newsletters, email sequences, SMS |
| egs-websites | Websites | Build order, scope, page and go-live checklists, revision triage |
| egs-account-manager | Account managers | Weekly updates, three-channel contact, chasers, call prep |
| egs-amplify | Amplify | The standard patient pipeline, build specs, workflow checks, test plans |
| egs-project-manager | Project manager | Board clean-up, meetings to tasks, SOP tracking, vendor follow-ups |
| egs-owner | Owner | Team overview, decisions not yet on tasks, client health |
| egs-ads | Ads, including our ads partner | Health ad rules, campaign briefs, ad copy, landing page checks, results. Works on its own. |

## Install

**For the whole team (owner, once):** in claude.ai, Organization settings > Plugins & skills, add this
private repository. The plugins then appear for everyone in claude.ai, Claude Desktop and Claude Code.

**One person, in Claude Code:**

```
/plugin marketplace add EGS-Marketing-Solutions/egs-skills
/plugin install egs-core@egs
/plugin install egs-seo@egs        (or their role)
```

Then say **"Set me up."** The egs-connect skill walks them through connecting each tool, about 30
minutes.

## Rules that never bend

- Claude reads and drafts. People send, post and change things. The egs-core guard blocks the
  connector tools that send, post or change anything.
- No patient information goes into Claude.
- Secrets stay in `~/.config/egs-assistant/` on each person's own computer, never in this repository
  or a chat.

## Changing a skill

Tell your Claude what should change for everyone. It drafts the change; send it to Kyle as a pull
request. Bump the plugin's `version` in `plugins/<name>/.claude-plugin/plugin.json` so installed
copies update. Personal preferences go in your profile or `CLAUDE.local.md`, which stays on your
computer.

Check a change before sharing it: `claude plugin validate .` and `claude plugin validate plugins/<name>`,
and run the sweep test cases in `evals/`. Rebuild the upload packages with:

```
for p in plugins/*/; do n=$(basename "$p"); (cd "$p" && zip -qr "../../dist/$n.zip" . -x "*/__pycache__/*" "*.DS_Store"); done
```

## Also here

- `docs/`: for people: the meeting guide, ten habits for working fast, and the plan for daily
  priorities and reports.
- `evals/`: test cases for the daily sweep.

# Working with Claude at EGS

The guide for the Claude Skills meeting, Wednesday 11 November 2026, and for anyone joining later.

## Why we are doing this

We are moving our AI work onto Claude, on accounts EGS owns. The aim is not a chatbot you have to
instruct each time. It is an assistant that reads our systems on its own every morning, knows what
is waiting on you, and has the first drafts written before you start.

## What "agentic" means

1. It reads the channels: Plutio, Google Chat, Gmail, Drive, your calendar, the last meeting.
2. It works out what is waiting on you, oldest first.
3. It produces everything it can: replies, client updates, copy, reports, task descriptions.
4. It hands you the drafts with the sources named, and says what it could not open.
5. You judge, edit and send, and post the stage comment it wrote for you.

It only reads. It never sends, posts or changes anything in any system. You stay in charge of every
decision and every message a client sees.

## Your day

- **First message to Claude each day:** the sweep runs by itself. You get a short note and a
  folder of drafts for today.
- **A new session later:** a quick catch-up on what is new since the morning.
- **During the day:** ask for anything. Claude already has the context.
- **When you finish something the team will repeat:** ask for the SOP draft.

## The EGS skills: one core plugin, one plugin for your role

Everyone installs **egs-core**. It loads by itself for any EGS work and brings:

- **Connection guides** for every tool, so your Claude can walk you through setup and API keys.
- **Workflows**: the daily sweep, client updates, copy, monthly reports, meetings to tasks, SOPs.
- **Your profile**: your role, your clients, your routines.
- **A read-only guard**, so your Claude never sends, posts or changes anything in our tools.

Then you add the plugin for your role, which makes your Claude good at your craft and lists what it
drafts for you on its own: egs-seo, egs-social, egs-content, egs-websites, egs-account-manager,
egs-amplify, egs-project-manager, egs-owner, or egs-ads.

## What changes by role

- **Account managers:** Monday client updates are drafted for every client you own. Replies to
  waiting clients are drafted each morning, with the Amplify text and Plutio comment for the
  three-channel rule.
- **Project manager:** after the Monday meeting, the recap arrives as task drafts and comments on
  existing tasks. Each morning, a board clean-up list with the fixes drafted.
- **SEO and AI search:** monthly reports with Search Console and Analytics numbers on the first
  working day; a weekly watch of what moved, with the fix written; blog briefs; schema; title and
  meta rewrites; a monthly check of whether AI assistants name the client.
- **Content:** briefs turned into drafts as soon as a task has its inputs; revisions folded in.
- **Social media:** next month's content plan with captions around the 20th, the creative brief for
  the design team, two short-video scripts per client, event kits, approval chasers, monthly results.
- **Websites:** revision lists sorted into in scope and out of scope, with the reply drafted.
- **Amplify:** everything waiting on you across Plutio and the Amplify spaces, with build notes.

Your profile in `team/` says which of these your Claude runs. Change it to fit how you work.

## The rules

- **Read-only.** Claude reads and drafts. You send, post, comment and change things.
- **Stage comments** on every Plutio task, at every stage.
- **Three channels** for client contact, recorded: email, Amplify text, Plutio comment.
- **A task carries its context**, and has one owner.
- **No patient information in Claude.** No patient lists, no names with health details.
- **EGS accounts only.** Never connect a personal Gmail or Drive.
- **Say what you could not open.**

## Getting set up

Once egs-core and your role plugin are installed (Stephani makes them available to the whole team),
open Claude Code and say "Set me up." Your Claude walks you through connecting each tool, about 30
minutes. Then read `docs/efficiency.md`, ten habits that make the
difference.

## Questions people have asked

- **Usage limits.** The sweep is the heaviest thing Claude does each day. Keep each session to one
  piece of work, and tell Stephani if you hit a limit.
- **Which Claude project do I use?** In claude.ai, use the client's project if one exists. In Claude
  Code, the skills work in any folder.
- **A connector will not connect.** Ask your Claude to check your connections. It says what is
  missing and walks you through fixing it.
- **Claude got something wrong.** Tell it in plain words. If the mistake would happen to everyone,
  it drafts a change to the shared rules for Kyle to approve.

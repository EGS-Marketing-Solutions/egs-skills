---
name: egs-client-update
description: Drafts the weekly or monthly client update an EGS account manager sends to a practice, in the client's words, from the week's Plutio activity, the client's Chat space, email, Drive and the last call. Use it for any client update, Monday update, status email, progress report, or "what do I tell <client> this week", and during an account manager's Monday sweep.
---

# Client update

Load the egs skill first; its rules apply here.

## Gather the week

Look back 7 days (or the period asked) across every source you can reach. Name the ones you could not.

- **Plutio:** `egs.py plutio client "<client name>" --days 7` lists every task
  for the client that finished or moved, with the week's comments. "Sent to client to review" and
  "client approved" are the events the update is made of.
- **Google Chat:** `egs.py chat read "<client name>" --days 7`. What they asked,
  what we answered, what is still open.
- **Gmail:** threads with the client's domain. Approvals, requests, questions we have not
  answered.
- **Drive:** files added to their folder this week (drafts, designs, photos).
- **Last call:** the recap or transcript. Decisions and promises.

Before writing, list what is genuinely waiting on the client, with the date we first asked. The
update is where those get asked again, politely and specifically.

## Write the update

In the client's words, not ours. No vendor names, no internal tool names, no team process. Say
"your newsletter", not "the Plutio task". Confident and plain. Short paragraphs or short bullets.

```
Subject: <Practice name>: this week's update

Hi <first name>,

Here is where things stand this week.

**Finished**
- <thing>, <one line on what it means for them>. <link if public>

**In progress**
- <thing>: <where it is, what happens next, when>.

**We need from you**
- <specific item>, so that <what it unblocks>. We first asked on <date>.

**Coming up**
- <next week's items>.

<one line sign-off>
<account manager name>
```

Leave out a heading with nothing under it. If nothing finished, say what moved and why. Never
invent progress; if the week was quiet, the update is short and honest.

## Hand over

Save it to `drafts/<date>/<client>/weekly-update.md`, marked DRAFT. Give the account manager the draft, the list of sources read, and anything you
could not open. They send it by email and, where the client uses it, as an Amplify text, and
post the stage comment on the Plutio task. Write that comment for them to post:
"Weekly update sent to <name> on <date> by email and Amplify text."

# Plan: daily priorities and team reports

Status: draft plan, 11 November 2026. Plutio task: "Build the team's automatic morning updates in Google Chat".

## What we want

1. **Every team member starts the day knowing exactly what to work on:** a short priority list, a one-line
   explanation of each task (what it is and the next step), and a link to the Plutio task.
2. **Reporting builds itself:** a daily report and a weekly report of what was finished, what was worked
   on, what is blocked and why, and what is waiting on clients.

Nobody sets anything up. One service, run by EGS, does it for everyone.

## How it fits together

| Part | Who runs it | What it does |
|---|---|---|
| **The morning service** (Cloud Run on EGS's Google Cloud) | Ethan builds; EGS owns | Reads Plutio and Chat for everyone on a schedule, posts each person their list, posts the reports |
| **Each person's Claude** (the EGS skills) | Each person | Opens the list, reads the full threads, drafts the work, writes the stage comments for them to post |
| **Profiles** (in the egs-core plugin) | Each person, reviewed by Kyle | Say who someone is, which clients and boards are theirs, when they want their list, and their routines |

The service and each person's Claude use the same readers (`plugins/egs-core/scripts/egslib`), so a
fix in one place fixes both.

## 1. The morning priority list

**When and where:** 8:00 AM in each person's own time zone (two runs: Manila and US Central), as a
direct message in Google Chat from the EGS assistant.

**What it looks like** (made-up example):

```
Good morning, Grey. Your priorities for Thursday 12 November:

1. Client A, blog approval: Michaela asked on 3 Nov whether the second blog is ready to send.
   Next: confirm it, or say what is missing. <Plutio link>
2. Client B, monthly SEO report: due today, routine from your profile. The draft is in your
   Claude's drafts. Next: check the numbers and send it to the account manager. <link>
3. Client C, home page schema: the markup on the live page does not parse. Next: replace it with
   the corrected version. <link>
...
Waiting on others (no action today): Client D blog, sent to the client on 6 Nov.
Yesterday: finished 2, worked on 4, 1 blocked (see the team report).
```

**How priorities are decided.** Rules first, then Claude writes the explanations. In order:

1. Something already wrong that a client can see (a broken page, a mistaken post).
2. A client waiting on a reply from this person, oldest first.
3. A teammate's question or request to this person in a Plutio comment or Chat, not yet answered.
4. Overdue tasks that are still active (activity in the last 60 days), by due date.
5. Promises this person made in a comment ("I'll check") and has not followed up.
6. Due in the next three days.
7. Routines due today from their profile (for example the Monday client updates).
8. Unassigned work in their area that is due soon (tracker subtasks, their own group).

Left out of the list, and sent to Kyle's clean-up report instead: tasks with no activity for 90 days,
tasks still assigned to people who have left, and templates.

**Each item carries:** the task title, the client, one line on what it is, one line on the next step,
who said what and when if someone is waiting, and the Plutio link. Ten items at most, then "and N
more".

## 2. The reports

**Daily team report**, 8:30 AM Manila, to Kyle and Stephani (a team space or direct messages):

- per person: finished yesterday, worked on, blocked and why, waiting on a client;
- new work that arrived with no owner;
- the clean-up list (stale, departed owners, bare tasks).

**Weekly report**, Monday 7:00 AM Central, before the 9:00 team meeting, posted to that week's meeting
space:

- by person: finished, in progress, blocked (with the reason and since when);
- by client: delivered this week, waiting on the client (with the date we first asked and the three
  contact attempts), due next week;
- trends: overdue count and blocked count against last week.

**How "finished", "worked on" and "blocked" are worked out:**

- *Finished:* the task was completed in Plutio, or its newest stage comment says sent, approved or
  published.
- *Worked on:* the person commented on it, or it was updated, that day.
- *Blocked:* the newest comment says the work is waiting on someone ("waiting on", "need the
  assets", "client hasn't replied"), or carries the convention below. The reason is quoted from that
  comment, with who and when.
- *Waiting on a client:* the newest stage comment is "sent to client" with no approval since.

**One new habit makes the reports reliable:** add "Blocked: <what we are waiting for, from whom>" to
the stage comments the team already posts (ready for review, sent, approved, published, closed).
Everyone's Claude writes these comments for them, so it costs a paste.

The service keeps a small daily snapshot of every active task (status, owner, newest comment, due
date) so it can tell what changed since yesterday and how long something has been blocked.

## 3. How the service is built

- **One Cloud Run job, three schedules** (Cloud Scheduler): morning lists at 8:00 Manila and 8:00
  Central, the daily team report at 8:30 Manila, the weekly report Mondays 7:00 Central.
- **In the EGS Google Cloud project** that already runs the Amplify Integration Hub and is covered by
  Google's business associate agreement. Secrets in Secret Manager; snapshots in a private bucket.
- **Read everything once per run, then work out every person's view in memory.** Fetching per person
  takes about a minute each in Plutio; one shared pass over active tasks, recently updated tasks and
  their comments keeps a run to a few minutes.
- **Claude API** for the one-line explanations, the blocked reasons and the weekly summary. The current
  Sonnet model (`claude-sonnet-5-5`) for the daily lists; Opus (`claude-opus-5-5`) for the weekly
  report if the quality needs it. Run the lists as an overnight batch and cache the shared rules to
  keep the cost down; measure the real cost in the pilot.
- **Read-only, except posting the notes.** It never comments in Plutio, never emails, never posts in
  client spaces.
- **No patient information** in any note; a final check drops any line that looks like a patient's
  name or health detail.
- **Dry-run mode:** every note goes to Ethan only until the pilot passes.

## 4. What EGS needs to provide

| Need | Who | Why |
|---|---|---|
| A Workspace service account allowed to read Chat for team members | Stephani (Workspace admin) | To read mentions and client spaces for everyone |
| A Google Chat app for the assistant, installed for the team | Stephani | To post the direct messages and reports |
| A Plutio API client for the service, created by an account that sees every project | Stephani | So the service reads the whole board |
| An Anthropic API account under EGS, with a spending limit | Stephani | For the explanations and summaries |
| The assistant's name, and where reports post | Ethan and Stephani | Decided once |

Tasks created through Plutio's API land off the team board and are invisible to other API clients
until someone drags them onto the board. Keep the board the home of every task, or the service will
miss them.

## 5. Phases

| Phase | What ships | How we know it works |
|---|---|---|
| 0 (this week) | Decisions and access above; profiles get a short machine-readable header (time zone, delivery time, boards watched, routines) | The service can read Plutio and one person's Chat |
| 1 | Morning lists from Plutio only, dry run to Ethan for Kyle and Grey | Five mornings where each list matches what they would have picked first |
| 2 | Chat signals added (mentions, clients waiting); lists go live to Kyle and Grey; the "Blocked:" habit starts | They say the list saves them the morning read-through |
| 3 | Lists live for everyone; daily team report to Kyle and Stephani | Kyle stops building his own daily list |
| 4 | Weekly report before the Monday meeting | The meeting runs from the report |
| 5 (optional) | Gmail signals, through the same service account | Client emails waiting appear in the lists |

## 6. Risks

- **Plutio comments are the only signal of progress.** A task with no comments looks untouched. The
  stage-comment habit is what makes the reports true; the skills make it a paste.
- **Plutio is slow and sometimes times out.** The readers retry; the run reads everything once.
- **Wrong priorities lose trust fast.** Pilot with two people, fix the rules, then widen.
- **Too many messages get ignored.** One morning message per person, one daily report, one weekly
  report. Nothing else.

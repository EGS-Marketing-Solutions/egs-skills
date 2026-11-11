---
name: egs-meeting-to-tasks
description: Turns an EGS meeting (the weekly team meeting, a client call, an onboarding call) into Plutio task drafts and comments with full context, checking Plutio first so nothing is duplicated. Use it whenever someone shares a recording, transcript, recap or notes, or asks what came out of a call or for the action items.
---

# Meeting to tasks

Load the egs skill first; its rules apply here.

## Read the whole thing

Find it: the recap posts in the meeting's Chat space (`egs.py chat sweep` shows the
latest), arrives by email, and the recording or notes sit in the meeting folder in Drive that
the project manager links on the weekly meetings task in Plutio. Use the transcript when one
exists; summaries drop who said what and soften decisions. Pull out,
with a timestamp or quote for each:

- Decisions: what was agreed, by whom.
- Commitments: who said they would do what, by when.
- Client requests: what the client asked for, in their words.
- Changes to existing work: anything that alters a task already on the board.
- Open questions: asked and not answered, and who owes the answer.

Identify the client from the attendees and the content, never from the meeting title.

## Check the board first

Search Plutio for each item before proposing anything (`egs.py plutio search "<words>"`):
by the words used in the meeting and by the words we would have used. If a task already covers it, the right move is a comment on that
task quoting the decision, not a new task. Say which existing tasks you found.

## Draft the tasks

For each genuinely new item, draft a task the way we write them. One owner.

```
Title: <verb> <object> for <client>
Owner: <name>   Due: <date if one was said, otherwise none>
Goal: <what will be true when this is done>
Situation: <the client, why this came up, what was said>
Decided: <names, wording, numbers, links, as a list>
Not decided: <and who decides>
Where things are: <Drive folder, Chat space, recording link with timestamp>
How it will be checked: <what the reviewer will look at>
Source: <recording or recap link, timestamp>
```

Then list the comments to post on existing tasks, each quoting the decision with the source.

Save the proposals to `drafts/<date>/team/meeting-<date>-tasks.md`.

## Hand over

Give the project manager the list of proposed tasks and comments, each ready to paste. They create
and post them. Put the recording or recap link in each task's first line so it carries its own
evidence. Items a client owes us go on the client's list in the account
manager's next update, not as tasks for us.

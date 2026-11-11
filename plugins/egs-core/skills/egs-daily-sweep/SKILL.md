---
name: egs-daily-sweep
description: The EGS daily sweep: reads the person's Plutio, Google Chat, Gmail, Drive, calendar and latest meeting recap, writes a short note of what is waiting on them, then immediately drafts everything the sources allow. Use it whenever the EGS sweep hook fires, at the start of a day or session, and whenever someone on the EGS team says start my day, catch me up, what's on my plate, what do I owe people, what did I miss, or comes back from time off.
---

# The daily sweep: read, then produce

Load the egs skill first; its rules apply here. Read the person's profile in
the egs skill's `references/team/<first-name>.md` and their role playbook in their role skill. The playbook's
"Produce automatically" list is part of this sweep.

## Mode

- **Full:** the first sweep of the day. Read every window below.
- **Catch-up:** a later session on a day already swept. Read only what is new since the time in
  `~/.config/egs-assistant/last-sweep` (line 2, UTC), keep the note to what changed, and skip routines already done.

## 0. Know the time

Every reader prints "Local time" with the UTC offset. Use it for "today", for ages in days and for
every time you write. Time zone abbreviations are ambiguous (PST is Pacific to an American and
Philippine Standard Time to a Filipino), so trust the offset, and write times as "9:00 AM Manila"
or "7:00 PM Central", with the client's zone in brackets when it differs. "The next two days" means
today and the next two calendar days in the person's own zone.

## 1. Check whose accounts you are reading

Confirm each connector is on the person's EGS account: the address on Gmail threads, the identity
the meeting tool reports, the owner shown on Drive files. `egs.py check` covers
Plutio and Chat. A connector on a personal account is "not checked", except for items that are
plainly EGS work: an EGS client, an EGS colleague, or an EGS document shared by link (Google Docs
linked in a task or email open fine from any account and are often essential). Use those, and say
in the first lines where they came from.

## 2. Read

- **Plutio:** `egs.py plutio sweep` (catch-up: `--days 2`). Gives what is waiting on them (mentions
  not yet answered over 30 days, someone else's comment on their task in the last 14), answers to
  them that ask nothing, what is due in three days, what is overdue but still active, and what has
  gone quiet. One job often has two tasks: before acting on an item, search for its sibling
  (`egs.py plutio search "<key words>"`); a sibling saying "paused" or "done" settles it. Open any thread you will act on with
  `egs.py plutio task <id>`.
- **Google Chat:** `egs.py chat sweep` (7 days; catch-up: `--days 1`). Mentions not answered, client
  spaces where the client spoke last, direct messages waiting, and the latest meeting recap. To check
  whether the person already replied somewhere, `egs.py chat read "<space>"` or `egs.py chat all`.
  The recap in Chat is cut short by the notes tool; read the full recap email or notes document for
  every next step.
- **Gmail, two passes,** excluding notification senders in the query
  (`-from:(noreply OR no-reply OR notifications OR chat-noreply OR calendar-notification)` plus
  Plutio, Keragon and HighLevel system mail). Keep results small: list threads in summary view
  25 at a time, then open only the threads you will report or answer. Attachments cannot be read
  through the connector; when a reply depends on one, say so and ask the person to save it to
  Drive or paste the text.
  - last 7 days: threads where a client, partner or colleague wrote last;
  - last 30 days: threads where a client or partner wrote last and nobody has answered.
  Then check sent mail for the people you are about to list, so you never report a reply that
  already went out. A thread answered and then reopened by a new message is waiting again.
- **Calendar:** today and the next two days. Meetings that need preparation get a prep note. With no
  calendar connector, rebuild the schedule from invitation, booking and reminder emails, and say so.
- **Drive:** files shared with them or changed in their clients' folders in the last 3 days.
- **Meetings:** recaps and recordings from the last 7 days. Their lines under "Next steps" are
  commitments.
- **Disconnected channels:** if Plutio or Chat cannot be read, their notification emails are the
  only signal. Use them in their own block, marked unverified.
- **Slack and other tools EGS uses with partners:** treat mention emails as notifications; list them
  once, unverified.

Read the thread behind each item before listing it. An item earns its place because of what the
last message says.

## 3. Produce

Before writing the note, write the drafts. For each item where the inputs exist, produce it now
and save it as `drafts/<YYYY-MM-DD>/<client or "team">/<short-name>.md`, starting with a line
naming the source (task link, thread link) and the word DRAFT.

What to produce, by what you found:
- A client or partner waiting on a reply: the reply, in the person's voice, answering every
  question in the last message. If an answer depends on a fact you do not have, write the reply
  with that sentence marked `[confirm: ...]`.
- A Plutio thread waiting on them: the comment that answers it, and the stage comment if the work
  moved a stage.
- A task whose deliverable is writing (copy, email sequence, newsletter, blog, page, script,
  outline, questionnaire, SOP): the deliverable (the egs-copy skill).
- A client update due (see routines): the update (the egs-client-update skill).
- A report due: the report (the egs-client-report skill).
- A meeting recap with their actions: the follow-ups and task drafts (the egs-meeting-to-tasks skill).
- Anything on their role playbook's "Produce automatically" list that the sources make possible today.
- A meeting in the next two days: a one-page prep note (what is open with that client, what to ask).

Then run the person's **routines** from their profile that are due today. Produce, do not list.
For each Plutio item that moved a stage, write the stage comment text in the draft, ready to paste.

Skip an item only when an input is genuinely missing (a document you cannot open, a decision only
the client can make). Name the missing input in the note.

When an item is real work and no Plutio task covers it (after searching), write the new task, in
the task format from the egs skill's `references/plutio-map.md`, as a draft for the person or the project manager to
create. Mark it "new task proposed" in the note.

## 4. Write the note

Keep it short. Link every task, thread and file. Times in the person's time zone, with the
client's zone in brackets when it differs. Tag each "Needs you" item (client), (partner) or
(team), oldest first.

```
# Today for <name>, <weekday day month>

Read: Plutio, Chat (n spaces), Gmail (7 and 30 days), Calendar, Drive, <recap date>.
Not checked: <connector and what that hides>.

## Fix first
- <anything already wrong that you or the team caused, and is live or visible: a mistaken comment, a broken page, a wrong date>. Correction: drafts/<path>.

## Needs you
- <task or thread>: <who>, <date> (<n> days): "<quote>". <what they need>. Draft: <path or "none, missing X">. (client)

## Drafted for you (n)
- <what> for <client or task>: drafts/<path>. <one line on what you need to check before sending>.

## Today and the next two days
- <meeting or deadline>, <time>. <prep note path if any>.

## From the <date> meeting
- <action they own>. <draft path or status>.

## Seen only through notifications, state unverified
- <item>, <channel>.

## Promises you have not followed up
- <task>: you said "<quote>" on <date>.

## Gone quiet (still open, 30 to 90 days)
- <task>. Close, re-plan or chase?

## Already answered
- <thread>: replied <date>. Nothing to do.

## Alerts
- <automation failure on a live client workflow, security alert, carrier ticket>.
```

Leave out empty sections. "Fix first" is only for errors already visible to someone; it goes
first because it is the cheapest damage to undo. Save the note as `drafts/<date>/today.md` and show it in the reply.

## 5. Finish

Run `egs.py sweep-done` so the hook goes quiet. Then answer whatever the person asked in the
message that started the session. Point them at the most urgent draft first. Never send, post,
comment or publish; they do.

# Reading each source well

First, for every connector: confirm it is signed in as the person's EGS account. The Gmail
address on the threads, the identity the meeting tool reports, the owner shown on Drive files.
A personal account shows a different life, and a note built on it is wrong in ways that are hard
to spot later. Say it in the first lines if a connector is on the wrong account.

## Plutio

- Find your tasks with `egs.py plutio sweep`: active tasks assigned to you, plus
  every recently active task where a comment @mentions you, because mentions are how work
  actually reaches people here. Plutio has no search for mentions, so the tool reads the threads
  of every task that moved in the window.
- For each task that matters, read the comments oldest to newest, then the description. The
  description is what the task was meant to be; the comments are what it became.
- Ask of the last comment: who wrote it, when, does it name someone, does it ask a question. If
  someone else wrote it and it names you or asks something, the ball is yours.
- Quote the comment, with the author and date, when you report it. "Michelle, 6 Nov: 'sent to
  client to review'" tells the reader more than "waiting".
- Attachments and links live on the task and in comments. A link to a Drive folder is a source
  you must open before writing the section that depends on it.
- The board has many unassigned templates and checklists. Skip them.

## Google Chat

- Client spaces are named for the practice (and often the contact). The last message in a client
  space tells you whether the client is waiting on us: if the client wrote it and it is older
  than a day and not a thank-you, we owe a reply.
- @mentions in team spaces are assignments. If you are mentioned and have not replied in that
  space since, it is on your list.
- The weekly meeting space carries the recap (Gemini) and sometimes a transcript. The "Next
  steps" lines name an owner in brackets. Those are commitments.
- Decisions made in Chat change what gets built. When you find one, check whether the Plutio
  task reflects it. If not, draft the comment that would.

## Gmail

- Search a window that reaches back past the item you are checking. A three-day-old question
  needs more than today's mail.
- For each thread, look at the final message. If the final message is ours, we replied; it is not
  waiting on us. If it is theirs, measure the age from that message.
- Ignore notification traffic: Plutio notifications, appointment confirmations, ticket updates,
  vendor marketing, meeting-bot recaps. They are never a task. Two exceptions: when Plutio or
  Chat is not connected, their notification emails are the only signal, so use them in a block
  marked unverified; and automation failure or security alerts get one line in an Alerts section.
- Look past the last week as well. A client's unanswered ask from three weeks ago is still
  unanswered. A second pass over 30 days for threads where a client wrote last catches it.
- Our inbox is the EGS account. If a client writes to a colleague's address, you will not see
  it; say so rather than presenting the inbox as the whole picture.

## Google Drive

- Each client has a folder, and a Client Information Sheet that is meant to be the current
  truth about them. Read it before writing for that client, and note anything in it that the
  other sources contradict.
- Meeting folders hold recordings, notes and files from a call. A folder's name is not a
  description of what is in it; open it.
- If a folder is shared to another account you cannot see it. Report the folder by name and say
  it could not be opened.
- Check the size and resolution of client photos before designing around them.

## Meeting recordings and recaps

- Prefer the transcript to the summary when a decision or an owner matters. Summaries drop
  the "who" and soften the "what".
- Classify a meeting by its attendees and content, not its title. Most are called "Impromptu
  Google Meet Meeting".
- The weekly recap also arrives by email. Count it even when the meeting tool shows nothing.
- Pull out: decisions, who owns what, what the client asked for, dates named, and anything that
  changes an existing task. Each of those becomes a Plutio comment or a task draft.

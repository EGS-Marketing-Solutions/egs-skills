---
name: egs-copy
description: How EGS writes copy for clients: brief first, then draft, edit and check against the brief. Use it for any blog, newsletter, email or sequence, text message, landing or website page, lead magnet, social post, ad copy, script or Google Business Profile post for an EGS client, and whenever a Plutio task's deliverable is writing.
---

# Copy for EGS clients

Load the egs skill first; its rules apply here.

## 1. The brief comes first

No draft starts without a brief. Most revision rounds come from a missed brief item, not from
weak writing. Build the brief from the sources, not from memory:

- **The task:** the Plutio task description and every comment (`egs.py plutio task <id>`).
  Comments often change the brief after it was written.
- **The client:** their Client Information Sheet in Drive, their website, their past approved copy
  (last newsletter, last sequence). Match their voice, not ours.
- **The execution plan:** the client's plan group on the board says what this piece is for in
  the bigger plan.
- **What was said:** the client's Chat space and recent meeting recap.

Write the brief at the top of the draft:

```
Brief
- Client and audience:
- Goal of this piece (one action we want the reader to take):
- Content type and length:
- Keyword or topic (SEO pieces):
- Must include: (client's own words, facts, dates, offers, links)
- Must avoid: (claims, topics, competitors, anything the client has rejected before)
- Call to action and link:
- Internal links (blogs and pages):
- Sources read: (task, sheet, past copy, Chat, recap)
- Open questions: (anything only the client can answer)
```

If something on the brief is missing and only the client can supply it, draft anyway with a
clearly marked placeholder, and put the question in the handover.

## 2. Draft

- The client's voice and words. Second person to the reader.
- Outcome first: what changes for the reader, then how.
- Short paragraphs. One idea each. Subheads a skimmer can follow.
- Real details from the sources: names, dates, places, prices as the client gave them.
- For medical practices: no promise of a clinical outcome, no diagnosis, no "cure". Describe
  the service and the experience. Never use a patient's story or likeness unless the task says
  consent was given.
- Dates: check the year. Clients often write last year's date for an upcoming event.

## 3. Edit, then check against the brief

Read it back once as the client's reader would. Cut anything that does not serve the goal. Then
add a check table under the draft:

```
| Brief item | Met? | Where |
|---|---|---|
| <item> | yes / no / placeholder | <section or line> |
```

Any "no" means the draft is not done. Fix it, or name it as an open question.

## 4. Hand over

Save to `drafts/<date>/<client>/<piece>.md` with DRAFT and the source links on top. Tell the
person what to check, what is a placeholder, and what to ask the client. When they approve, they paste it into
a Google Doc in the client's Drive folder. Write the stage comment for them to post on the Plutio
task: "Draft ready for review: <link>".

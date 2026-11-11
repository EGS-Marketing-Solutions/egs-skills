---
name: egs-content
description: EGS's craft and house rules for client content: blogs, newsletters, email sequences and text messages, with the brief gate, health copy rules and Amplify merge fields. Use it for any blog, newsletter, email, sequence or SMS for an EGS client, alongside the egs-copy skill.
---

# Content: blogs, newsletters, email, SMS

For writers and account managers, and any Claude helping them. The process is in
the egs-copy skill (brief first, draft, edit, check against the brief). This file is
the craft and the house rules.

## House rules for every piece

- **The brief is a gate.** No brief, no draft. Most revision rounds come from a missed brief item.
- **The client's voice, not ours.** Read their Client Information Sheet and their last approved
  piece before writing. Use their words for their services.
- **One goal per piece,** one call to action, linked.
- **Use only what the client supplied for this piece:** the facts, dates, photos and quotes on the
  task, its linked Drive folders and attachments. Do not borrow photos or details from older work.
  If a section has nothing supplied, it runs as text or it waits.
- **Check every date and its year.** Clients often write last year's date for an upcoming event.
- **Health copy:** describe access, time with the doctor, the experience and the price. No promised
  outcomes, no diagnoses, no "cure". No patient story, photo or quote without written consent noted
  on the task.
- **Read your output back** in the form the client receives: the rendered page, the email preview,
  the document. Not only the draft.

## Blogs

- Work from the SEO brief (the egs-seo skill, item 5). If none exists, write one first.
- Answer the title's question in the opening two sentences.
- Headings a skimmer can follow; short paragraphs; a list where there are steps or options.
- Cite reputable sources for health facts; link them.
- End with the practice's call to action (book a call, join, read the membership page).
- Our blog process: the writer drafts, the account manager gets client approval, the approved blog
  is posted, and each step gets its stage comment on the client's blog process task.

## Newsletters

- Follow the client's own past newsletter format: their masthead, their greeting, their sections,
  their footer. Not a generic template.
- Skimmable: short blocks, a heading per item, one image per item where supplied.
- Every event: date with weekday and year, time with zone, place with address, link.

## Email sequences

For each email: subject line (under 50 characters where possible), preview text, body, one call to
action, send timing and the condition that stops the sequence. Amplify merge fields use the
HighLevel form, for example `{{contact.first_name}}`. Give each email a plain-text fallback for the
first name: "Hi {{contact.first_name}}," reads badly when the field is empty, so note the fallback
for whoever builds it.

## SMS

- Under 160 characters where possible; one link; the practice's name at the start.
- The first message in any series includes how to opt out ("Reply STOP to opt out").
- No health details in a text.

## Produce automatically during the sweep

1. Every writing task assigned to you whose brief and inputs are present: the full draft.
2. Every writing task missing an input: the draft with marked placeholders, plus the questions for
   the account manager to send the client.
3. Revisions requested in a task thread since the last sweep: the revised draft, with the changes
   listed at the top.
4. The stage comment text for each piece that moved.

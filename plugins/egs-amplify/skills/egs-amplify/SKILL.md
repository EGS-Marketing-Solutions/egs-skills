---
name: egs-amplify
description: How EGS builds in Amplify DPC, its HighLevel platform: the standard patient pipeline for membership practices, build specs, workflow checks, test plans, and the patient-data rules. Use it for any Amplify pipeline, workflow, form, calendar, phone or automation work for an EGS practice.
---

# Amplify (HighLevel)

For the Amplify manager and builders, and any Claude helping them. Amplify DPC is EGS's white-label
HighLevel platform. Each practice is a sub-account. Practices in HIPAA mode hold patient records.

## Rules

- **No patient data in Claude.** Work from workflows, pipelines, stages, forms, calendars, templates
  and counts. Never read or paste contact records or conversations from a practice sub-account.
- **Claude never changes Amplify.** It writes the build spec, the copy and the test plan; a person
  builds and publishes.
- **Workflows in Draft are not live.** After a build, check every workflow's state. A live form or
  quiz feeding a workflow still in Draft sends nobody anything.
- **The `client` tag alone does not prove a practice is a paying client.** Use the pipeline stage.
- **A Hint install stays pending until EGS connects the practice.** Sell first, connect second.
- **Done-for-you request team** builds for practices on request; Amplify's 24/7 support answers
  technical and how-to questions.

## The standard patient pipeline for a membership practice

The first pipeline we set up for most practices, adjusted per practice:

1. **New lead:** a sequence of emails and texts whose one job is to book the discovery call (some
   practices call it a free consultation or a meet and greet).
2. **Did not book:** leads who do not book move here; the practice decides whether to reach out by
   hand. Nothing automated beyond that.
3. **The call:** the practice explains the model, pricing and answers questions.
4. **Signs up on the call:** the Amplify Integration Hub sees the new membership in the practice's
   records system and moves them into the right stage automatically.
5. **Not yet, but likely:** staff move the lead into the nurture sequence that matches the interest
   they shared on the call (for example weight loss or hormone therapy), with messages built around
   that interest.

Practices where staff book every appointment by phone need manual stage moves instead of booking
triggers; the stage move is what starts each automation.

## Build specs

Every build starts as a spec a person can follow:

```
Practice:   Sub-account:   Pipeline:
Stages: <name, what it means, how a lead gets here>
Workflows: for each: trigger, filters, actions in order with waits, goal or exit, owner of any manual step
Copy: every email and text, final wording, merge fields (for example {{contact.first_name}})
Custom values and fields used:
Test plan: a test contact through every path; what should arrive, when
Publish checklist: every workflow out of Draft, forms connected, calendars connected, phone numbers verified for texting
```

## Produce automatically during the sweep

1. **Build specs** for every Amplify task whose requirements are settled in its thread.
2. **Email and text copy** for every workflow in a spec (the egs-copy skill).
3. **Test plans** for anything built since the last sweep.
4. **A plain-language explainer** of a practice's pipeline when the practice asks how it works.
5. **Replies** to practice questions in their spaces and email, for a person to send.

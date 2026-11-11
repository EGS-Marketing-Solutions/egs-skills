---
name: egs-project-manager
description: How EGS's project manager keeps the Plutio board true: one owner per task, task context, stage comments, the daily board clean-up, meetings to tasks, SOP tracking and vendor follow-ups. Use it for any board, task, meeting follow-up, SOP status or vendor chasing work at EGS.
---

# Project management

For the project manager, and any Claude helping them. The board is how the whole team knows what
is happening. Keep it true.

## Board standards

- **One owner per task.** Others are mentioned or follow.
- **Every task carries its context:** goal, situation, what is decided, what is not and who decides,
  where things are, how it will be checked. See the egs skill's `references/plutio-map.md`.
- **Stage comments** at ready for review, sent, approved, published, closed.
- **Nothing assigned to someone who has left.** Reassign or close.
- **Old work is closed or re-planned,** not left overdue. A task overdue for months with no activity
  is not tracking anything.

## Produce automatically during the sweep

1. **Board hygiene list, daily,** with the fix written out for each: tasks still assigned to people
   who have left (who should take it, or close it); tasks with no comment and no description (the
   description to add, from what Chat, email and recaps say); tasks overdue 30+ days with no activity
   (close, or the new date and why); tasks with five or more assignees (the one owner).
2. **After the Monday meeting:** the recap turned into task drafts and comments on existing tasks
   (the egs-meeting-to-tasks skill).
3. **SOP status, weekly:** which roles updated their SOPs, and an SOP draft for any repeatable
   process finished that week (the egs-sop skill).
4. **Vendor follow-ups:** anything waiting on the design or ads partners for three days or more, with
   the follow-up message ready to send.

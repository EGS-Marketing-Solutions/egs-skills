# The team

One file per person: role, time zone, the clients they own, and the routines their Claude runs
during the daily sweep. Every Claude reads the whole folder, so it knows who owns what and can
route a question to the right person.

- `roster.json` is the machine-readable version: Plutio ids, who has left, which Chat spaces are
  internal. The readers in the egs-core plugin use it.
- Client lists marked "to confirm" come from the 2 and 9 November team meetings. Correct yours
  the first time you run setup.
- Routines are a starting point. Change yours to match how you actually work; your Claude will
  run whatever this file says.
- Changes go to Kyle for review, so the team's picture stays right.

Someone joins: copy any profile, change it, and add them to `roster.json`. Someone leaves: move
their id to `departed` in `roster.json`; the daily brief then lists their open tasks for
reassignment.

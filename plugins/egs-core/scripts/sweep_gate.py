#!/usr/bin/env python3
"""Claude Code runs this on every message (UserPromptSubmit hook). It speaks at most once per session:
the full daily sweep on the first message of the day, a short catch-up on the first message of any later
session that day. It never blocks a message. State is per person, in ~/.config/egs-assistant/.
Pause it by creating ~/.config/egs-assistant/sweep-off."""
import datetime as dt, json, os, re, sys

HOME = os.path.expanduser(os.environ.get("EGS_CONFIG_DIR", "~/.config/egs-assistant"))
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
EGS = f'"{sys.executable}" "{os.path.join(SCRIPTS, "egs.py")}"'


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        data = {}
    os.makedirs(HOME, exist_ok=True)
    if os.path.exists(os.path.join(HOME, "sweep-off")):
        return
    today = dt.date.today().isoformat()
    sid = data.get("session_id") or "unknown"
    seen_file = os.path.join(HOME, f"sessions-{today}")
    for f in os.listdir(HOME):
        if f.startswith("sessions-") and f != f"sessions-{today}":
            try:
                os.remove(os.path.join(HOME, f))
            except OSError:
                pass
    try:
        me = json.load(open(os.path.join(HOME, "me.json"))).get("name", "")
    except (OSError, ValueError):
        me = ""
    who = re.sub(r"[^a-z0-9]+", "-", me.lower()).strip("-")
    try:
        lines = open(os.path.join(HOME, f"last-sweep-{who}" if who else "last-sweep")).read().split()
    except OSError:
        lines = []
    seen = open(seen_file).read().split() if os.path.exists(seen_file) else []
    swept_today = bool(lines) and lines[0] == today
    if swept_today and sid in seen:
        return
    if sid not in seen:
        with open(seen_file, "a") as f:
            f.write(sid + "\n")
    if not swept_today:
        print(f"[EGS DAILY SWEEP DUE, {today}] First message of the day. Before answering, load the egs skill, then run "
              f"the egs-daily-sweep skill in full mode for the person at this keyboard. "
              f"Read-only in every system. Run the readers as: {EGS} <command>. Produce every draft the sources allow, "
              f"write the note, then run: {EGS} sweep-done. Then answer what they asked.")
    else:
        when = lines[1] if len(lines) > 1 else "earlier today"
        print(f"[EGS CATCH-UP DUE] New session; today's sweep ran at {when} UTC. Before answering, run the egs-daily-sweep "
              f"skill in catch-up mode: only what is new since then, "
              f"new drafts only, read-only. Readers: {EGS} <command>. Then run: {EGS} sweep-done and answer what they asked.")


if __name__ == "__main__":
    main()

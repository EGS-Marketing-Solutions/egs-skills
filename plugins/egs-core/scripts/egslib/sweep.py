"""What is waiting on a person in Plutio, worked out from tasks and threads already fetched. Read-only.

Shared by egs.py (one person, on their own computer) and EGS's morning-updates service (everyone, in one
pass), so a fix to these rules reaches both.

  data = fetch([person_id, ...], days)               one pass over Plutio for everyone listed
  view = person_view(data, person_id, name, days)    what that person's sweep shows
"""
import datetime as dt
import re
from concurrent.futures import ThreadPoolExecutor

from . import plutio

NOW = dt.datetime.now(dt.timezone.utc)  # one clock per run; a long-running process must re-import or refresh

# A short acknowledgement closes a loop; it is not a request.
ACK = re.compile(r"^(ok(ay)?|thanks?( you)?|ty|noted|got it|perfect|great|sounds good|will do|done|nice)\W*$", re.I)
ACK_START = re.compile(r"^(ok(ay)?|sure|noted|will do|on it|got it|thanks?|thank you|sounds good|perfect)\b", re.I)
ASK = re.compile(r"\?|\b(please|can you|could you|would you|can we|need (you|your|a|the)|let me know|waiting (on|for) you|your turn|for you to|kindly)\b", re.I)
PROMISE = re.compile(r"\b(i'?ll|i will|let me (check|look|see|find)|will (follow up|look into|check|send|get back)|look into it|get back to you)\b", re.I)


def clean(text, n=220):
    return re.sub(r"\s+", " ", text or "").strip()[:n]


def is_ask(text):
    return bool(ASK.search(text or ""))


def is_ack(text):
    t = clean(text, 400)
    return bool(ACK.match(t)) or (len(t) < 100 and "?" not in t and bool(ACK_START.match(t)))


def parse(s):
    if not s:
        return None
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def days_ago(d):
    return (NOW - d).days if d else None


def mentions_name(text, name):
    first = name.split(" ")[0]
    return bool(re.search(r"@" + re.escape(name) + r"\b", text) or re.search(r"@" + re.escape(first) + r"\b", text))


def person_id(people, name):
    exact = [k for k, v in people.items() if v.strip().lower() == name.strip().lower()]
    if len(exact) == 1:
        return exact[0]
    first = [k for k, v in people.items() if v.split(" ")[0].lower() == name.split(" ")[0].lower()]
    return first[0] if len(first) == 1 else None


def thread_facts(t, cs, people, me_id, me_name, window):
    """What a task's thread says about the person: is the ball theirs, and why."""
    last = cs[-1] if cs else None
    last_at = parse(last.get("createdAt")) if last else None
    stamps = [d for d in [parse(t.get("updatedAt")), last_at] if d]
    act = max(stamps) if stamps else None
    asks, fyis = [], []
    for i, c in enumerate(cs):
        at = parse(c.get("createdAt"))
        if not at or days_ago(at) > window or c.get("createdBy") == me_id:
            continue
        if mentions_name(c.get("bodyPlain") or "", me_name) and not any(x.get("createdBy") == me_id for x in cs[i + 1:]):
            answers_me = i > 0 and cs[i - 1].get("createdBy") == me_id and "?" not in (c.get("bodyPlain") or "")
            (fyis if answers_me else asks).append(c)
    waiting, reason = bool(asks), ("mentioned you" if asks else "")
    if not waiting and fyis:
        reason = "answered you (no question)"
    if not waiting and last and last.get("createdBy") != me_id and last_at and days_ago(last_at) <= min(window, 14) \
            and me_id in (t.get("assignedTo") or []):
        body = last.get("bodyPlain") or ""
        names_in = [n for n in set(people.values()) if n and mentions_name(body, n)]
        if not names_in and not is_ack(body):
            if is_ask(body):
                waiting, reason = True, "someone asked something on your task"
            else:
                reason = "update on your task, nothing asked"
    src = asks[-1] if asks else (fyis[-1] if fyis else last)
    promise = None
    if last and last.get("createdBy") == me_id and last_at and 3 <= days_ago(last_at) <= window \
            and PROMISE.search(last.get("bodyPlain") or ""):
        promise = {"at": last_at, "text": clean(last.get("bodyPlain"), 400)}
    due = parse(t.get("dueDate"))
    return {
        "id": t["_id"], "title": clean(t.get("title"), 160), "url": plutio.task_url(t) if t.get("projectId") else None,
        "where": plutio.board_path(t), "assignees": [people.get(x, x) for x in t.get("assignedTo") or []],
        "due": due, "overdue_days": days_ago(due) if due and due < NOW else 0,
        "due_in_days": (due - NOW).days if due and due >= NOW else None,
        "last_activity": act, "quiet_days": days_ago(act), "waiting_on_me": waiting, "why": reason,
        "said_by": people.get(src.get("createdBy"), src.get("createdBy")) if src else None,
        "said_at": parse(src.get("createdAt")) if src else None,
        "said": clean(src.get("bodyPlain"), 600) if src else "", "comments": len(cs),
        "fyi": (bool(fyis) and not asks) or reason == "update on your task, nothing asked", "promise": promise,
        "assignee_ids": t.get("assignedTo") or [],
        "description": clean(t.get("descriptionPlain"), 400),
    }


def _iso(d):
    return d.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def fetch(person_ids, days, people=None, workers=4):
    """Everything the sweep needs for these people, read once. Calls shared by everyone (recently updated
    tasks, tasks due this week, comment threads) are made once however many people are listed."""
    people = people if people is not None else plutio.people()
    updated = plutio.updated_since(_iso(NOW - dt.timedelta(days=days)))
    due_week = plutio.due_between(_iso(NOW), _iso(NOW + dt.timedelta(days=7)))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        mine = dict(zip(person_ids, ex.map(plutio.active_tasks_for, person_ids)))
        followed = dict(zip(person_ids, ex.map(plutio.followed_tasks_for, person_ids)))
    recent_ids = [t["_id"] for t in updated if t.get("commentsCount")]
    want = list(dict.fromkeys([t["_id"] for pid in person_ids for t in mine[pid] if t.get("commentsCount")] + recent_ids))
    return {"people": people, "updated": updated, "due_week": due_week, "mine": mine, "followed": followed,
            "threads": plutio.comments_many(want)}


def person_view(data, me_id, me_name, days, watch=(), departed=()):
    """One person's sweep from fetched data. `watch`: board or group names they keep an eye on;
    `departed`: Plutio ids of people who have left."""
    people, threads, updated = data["people"], data["threads"], data["updated"]
    mine = {t["_id"]: t for t in data["mine"].get(me_id, [])}
    recent = {t["_id"]: t for t in updated if t.get("commentsCount")}
    # Work nobody is assigned to but this person carries: tasks they follow (a tracker's subtasks list
    # their creator as follower), and unassigned tasks in their own group or a board they watch.
    first = me_name.split(" ")[0].lower()
    watched = [w.lower() for w in watch]

    def in_my_area(t):
        groups = [b.get("title", "").lower() for b in t.get("breadcrumb") or [] if b.get("entityType") == "task-group"]
        path = plutio.board_path(t).lower()
        return any(g.startswith(first + " ") for g in groups) or any(w in path for w in watched)
    pool = {t["_id"]: t for t in data["followed"].get(me_id, []) + updated + data["due_week"]}
    unassigned = sorted([t for t in pool.values() if not t.get("assignedTo") and t["_id"] not in mine
                         and (me_id in (t.get("followers") or []) or in_my_area(t))],
                        key=lambda t: (t.get("dueDate") or "9999", t.get("title") or ""))
    rows = []
    for tid in sorted(set(mine) | set(recent)):  # sorted, so ties come out in the same order every run
        t = mine.get(tid) or recent[tid]
        f = thread_facts(t, threads.get(tid, []), people, me_id, me_name, days)
        f["assigned_to_me"] = tid in mine
        if f["assigned_to_me"] or f["waiting_on_me"]:
            rows.append(f)
    waiting = sorted([r for r in rows if r["waiting_on_me"]], key=lambda r: r["said_at"] or NOW)
    due = sorted([r for r in rows if r["assigned_to_me"] and r["due_in_days"] is not None and r["due_in_days"] <= 3],
                 key=lambda r: r["due_in_days"])
    overdue = sorted([r for r in rows if r["assigned_to_me"] and r["overdue_days"] and (r["quiet_days"] or 999) < 60
                      and not r["waiting_on_me"]], key=lambda r: -r["overdue_days"])
    quiet = sorted([r for r in rows if r["assigned_to_me"] and r["quiet_days"] is not None and 30 <= r["quiet_days"] < 90],
                   key=lambda r: -r["quiet_days"])
    dead = [r for r in rows if r["assigned_to_me"] and (r["quiet_days"] or 0) >= 90]
    promises = sorted([r for r in rows if r.get("promise")], key=lambda r: r["promise"]["at"])
    departed = set(departed)
    # yours alone now: every other assignee has left
    left_behind = [r for r in rows if r["assigned_to_me"] and departed & set(r["assignee_ids"])
                   and set(r["assignee_ids"]) - departed == {me_id}]
    un_rows = []
    for t in unassigned:
        due_t = parse(t.get("dueDate"))
        parent = (t.get("parentTaskId") and pool.get(t["parentTaskId"], {}).get("title")) or ""
        un_rows.append({"id": t["_id"], "title": clean(t.get("title"), 160), "where": plutio.board_path(t) + (f" > {clean(parent, 60)}" if parent else ""),
                        "url": plutio.task_url(t) if t.get("projectId") else None, "due": due_t,
                        "subtasks": len(t.get("subTasks") or []), "parent": clean(parent, 80)})
    return {"person": me_name, "window_days": days, "assigned_active": len(mine), "waiting_on_me": waiting,
            "promises_not_followed_up": promises, "due_next_3_days": due, "overdue_still_active": overdue,
            "unassigned_in_my_area": un_rows, "shared_with_people_who_left": left_behind,
            "quiet_30_to_90_days": quiet, "untouched_90_plus_days": len(dead),
            "answers_and_updates": [r for r in rows if r.get("fyi")]}


def unassigned_due_soon(view, days=14):
    """Unassigned work in the person's area that is overdue or due within `days`."""
    cut = NOW + dt.timedelta(days=days)
    return [r for r in view["unassigned_in_my_area"] if r["due"] and r["due"] <= cut]

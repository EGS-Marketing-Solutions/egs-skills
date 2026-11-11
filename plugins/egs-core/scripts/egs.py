#!/usr/bin/env python3
"""egs: read EGS's tools the same way on every computer. Read-only: nothing here can post, send or change anything.

Claude runs this during the daily sweep and whenever it needs context. A person rarely needs to.

  egs.py setup --me "First Last"        make your private settings folder
  egs.py check                          what is connected on this computer
  egs.py google auth                    sign in to Google once (Chat, Search Console, Analytics, read-only)

  egs.py plutio sweep [--days 30] [--all]  waiting on me, answers to me, due soon, overdue but active, gone quiet
  egs.py plutio task <task id>          one task: description and full thread
  egs.py plutio search "<words>" [--all] [--text] [--assigned]   titles (and descriptions with --text)
  egs.py plutio client "<name>" [--days 7]   a client's recent activity, for updates and reports

  egs.py chat sweep [--days 7]          mentions not answered, clients waiting, DMs waiting, latest recap
  egs.py chat read "<space>" [--days 7] one space (or every space whose name contains the words)
  egs.py chat all [--days 7]            every message in every space, to check what was already answered
  egs.py chat spaces

  egs.py gsc sites                      Search Console properties you can read
  egs.py gsc report "<site>" [--days 28]   totals, top queries, top pages, change vs the period before
  egs.py ga properties                  Analytics properties you can read
  egs.py ga report "<property>" [--days 28]

  egs.py pagespeed <url> [--strategy desktop]   Core Web Vitals and the biggest fixes for one page

  egs.py sweep-done                     record that today's sweep ran

Settings and sign-ins live in ~/.config/egs-assistant/ on your computer, never in the skill.
"""
import argparse, datetime as dt, json, os, re, stat, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from egslib import config, plutio  # noqa: E402

NOW = dt.datetime.now(dt.timezone.utc)
LOCAL = dt.datetime.now().astimezone()


def local_line():
    off = LOCAL.strftime("%z")
    return f"Local time: {LOCAL.strftime('%a %d %b %Y, %H:%M')} (UTC{off[:3]}:{off[3:]})"
# A short acknowledgement closes a loop; it is not a request.
ACK = re.compile(r"^(ok(ay)?|thanks?( you)?|ty|noted|got it|perfect|great|sounds good|will do|done|nice)\W*$", re.I)
ACK_START = re.compile(r"^(ok(ay)?|sure|noted|will do|on it|got it|thanks?|thank you|sounds good|perfect)\b", re.I)


ASK = re.compile(r"\?|\b(please|can you|could you|would you|can we|need (you|your|a|the)|let me know|waiting (on|for) you|your turn|for you to|kindly)\b", re.I)
PROMISE = re.compile(r"\b(i'?ll|i will|let me (check|look|see|find)|will (follow up|look into|check|send|get back)|look into it|get back to you)\b", re.I)


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


def local(d, fmt="%d %b %H:%M"):
    """A timestamp shown in this computer's time zone (the offset is in the Local time line)."""
    return d.astimezone().strftime(fmt) if d else ""


def days_ago(d):
    return (NOW - d).days if d else None


def clean(text, n=220):
    return re.sub(r"\s+", " ", text or "").strip()[:n]


def need_me():
    name = config.me()
    if not name:
        raise SystemExit("I do not know who you are yet. Ask Claude to \"set me up\" (egs-connect skill), or run: egs.py setup --me \"First Last\"")
    return name


def mentions_name(text, name):
    first = name.split(" ")[0]
    return bool(re.search(r"@" + re.escape(name) + r"\b", text) or re.search(r"@" + re.escape(first) + r"\b", text))


def print_json(obj):
    def d(o):
        if isinstance(o, (dt.datetime, dt.date)):
            return o.isoformat()
        raise TypeError(str(o))
    print(json.dumps(obj, default=d, indent=1, ensure_ascii=False))


def pct(new, old):
    try:
        new, old = float(new), float(old)
    except (TypeError, ValueError):
        return ""
    if old == 0:
        return "new" if new else ""
    return f"{(new - old) / old * 100:+.0f}%"


# ------------------------------------------------------------------ setup / check

def cmd_setup(a):
    os.makedirs(config.HOME_DIR, exist_ok=True)
    if a.me or a.watch or not os.path.exists(config.ME_FILE):
        cur = config.me_settings()
        cur["name"] = a.me or cur.get("name", "")
        if a.watch:
            cur["watch"] = a.watch
        with open(config.ME_FILE, "w") as f:
            json.dump(cur, f, indent=1)
    if not os.path.exists(config.PLUTIO_FILE):
        with open(config.PLUTIO_FILE, "w") as f:
            json.dump({"client_id": "", "client_secret": ""}, f, indent=1)
        os.chmod(config.PLUTIO_FILE, stat.S_IRUSR | stat.S_IWUSR)
    print("Settings folder:", config.HOME_DIR)
    print("  me.json            your name:", config.me() or "(empty)", "| boards you watch:", ", ".join(config.watch()) or "none")
    print("  plutio.json        Plutio API client id and secret, pasted by you in a text editor")
    print("  google-client.json the Google sign-in file the team shares (save it here)")


def cmd_check(a):
    print(local_line())
    rows = [("you", "OK" if config.me() else "MISSING", config.me() or "no name set")]
    try:
        people = plutio.people()
        found = person_id(people, config.me()) if config.me() else None
        rows.append(("plutio", "OK", "signed in; " + ("you are in Plutio's people list" if found else "your name was NOT found in Plutio")))
    except SystemExit as e:
        rows.append(("plutio", "MISSING", str(e)))
    except Exception as e:  # noqa: BLE001
        rows.append(("plutio", "ERROR", clean(str(e), 120)))
    try:
        from egslib import gchat
        gchat.credentials()
        for label, scope in [("google chat", "chat.messages.readonly"), ("search console", "webmasters.readonly"),
                             ("analytics", "analytics.readonly")]:
            ok = gchat.granted("https://www.googleapis.com/auth/" + scope)
            rows.append((label, "OK" if ok else "MISSING", "signed in" if ok else "sign in again with: egs.py google auth"))
    except SystemExit as e:
        rows.append(("google", "MISSING", str(e)))
    except Exception as e:  # noqa: BLE001
        rows.append(("google", "ERROR", clean(str(e), 120)))
    for r in rows:
        print(f"{r[0]:<15} {r[1]:<8} {r[2]}")
    print("\nGmail, Drive, Calendar and meeting recordings are Claude connectors (Customize > Connectors), not checked here.")


# ------------------------------------------------------------------ google sign-in

def cmd_google_auth(a):
    if not os.path.exists(config.GOOGLE_CLIENT):
        raise SystemExit(f"First save the team's Google sign-in file as {config.GOOGLE_CLIENT}. Ask Claude to \"connect Google\".")
    from google_auth_oauthlib.flow import InstalledAppFlow
    from egslib import gchat
    flow = InstalledAppFlow.from_client_secrets_file(config.GOOGLE_CLIENT, gchat.SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True, prompt="consent", access_type="offline")
    with open(config.GCHAT_TOKEN, "w") as f:
        f.write(creds.to_json())
    os.chmod(config.GCHAT_TOKEN, stat.S_IRUSR | stat.S_IWUSR)
    print("Signed in to Google, read-only: Chat, Search Console, Analytics.")


# ------------------------------------------------------------------ plutio

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


def cmd_plutio_sweep(a):
    me_name = a.me or need_me()
    people = plutio.people()
    me_id = person_id(people, me_name)
    if not me_id:
        raise SystemExit(f"'{me_name}' is not in Plutio's people list. Use your name exactly as Plutio shows it.")
    mine = {t["_id"]: t for t in plutio.active_tasks_for(me_id)}
    since = (NOW - dt.timedelta(days=a.days)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    updated = plutio.updated_since(since)
    recent = {t["_id"]: t for t in updated if t.get("commentsCount")}
    # Work nobody is assigned to but this person carries: tasks they follow (a tracker's subtasks list
    # their creator as follower), and unassigned tasks in their own group or a board they watch.
    first = me_name.split(" ")[0].lower()
    watched = [w.lower() for w in config.watch()]
    def in_my_area(t):
        groups = [b.get("title", "").lower() for b in t.get("breadcrumb") or [] if b.get("entityType") == "task-group"]
        path = plutio.board_path(t).lower()
        return any(g.startswith(first + " ") for g in groups) or any(w in path for w in watched)
    week = (NOW + dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    pool = {t["_id"]: t for t in plutio.followed_tasks_for(me_id) + updated + plutio.due_between(NOW.strftime("%Y-%m-%dT%H:%M:%S.000Z"), week)}
    unassigned = sorted([t for t in pool.values() if not t.get("assignedTo") and t["_id"] not in mine
                         and (me_id in (t.get("followers") or []) or in_my_area(t))],
                        key=lambda t: (t.get("dueDate") or "9999", t.get("title") or ""))
    want = [tid for tid, t in mine.items() if t.get("commentsCount")] + [tid for tid in recent if tid not in mine]
    threads = plutio.comments_many(want)
    rows = []
    for tid in set(mine) | set(recent):
        t = mine.get(tid) or recent[tid]
        f = thread_facts(t, threads.get(tid, []), people, me_id, me_name, a.days)
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
    departed = set(config.team().get("departed", {}))
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
    soon_cut = NOW + dt.timedelta(days=14)
    un_soon = [r for r in un_rows if r["due"] and r["due"] <= soon_cut]
    un_groups = {}
    for r in un_rows:
        if r in un_soon:
            continue
        key = r["parent"] or r["where"]
        un_groups.setdefault(key, []).append(r)
    out = {"person": me_name, "window_days": a.days, "assigned_active": len(mine), "waiting_on_me": waiting,
           "promises_not_followed_up": promises, "due_next_3_days": due, "overdue_still_active": overdue,
           "unassigned_in_my_area": un_rows, "shared_with_people_who_left": left_behind,
           "quiet_30_to_90_days": quiet, "untouched_90_plus_days": len(dead)}
    if a.json:
        return print_json(out)
    print(f"# Plutio for {me_name}, {NOW.strftime('%d %b %Y')}")
    print(local_line())
    print(f"{len(mine)} active tasks assigned to you. Mentions read for the last {a.days} days.\n")

    def line(r, extra=""):
        link = f"[{r['title']}]({r['url']})" if r["url"] else f"{r['title']} (no project, no link)"
        return f"- {link}{' (' + r['where'] + ')' if r['where'] else ''} id {r['id']}{extra}"

    def block(title, items, fmt, cap):
        print(f"\n## {title} ({len(items)})")
        for r in items[:cap]:
            print(line(r, fmt(r)))
        if len(items) > cap:
            print(f"- and {len(items) - cap} more: run again with --all to list every one")
    cap = 10_000 if a.all else 25
    fyi = [r for r in rows if r.get("fyi")]
    block("Waiting on you", waiting, lambda r: f". {r['said_by']}, {local(r['said_at'], '%d %b')} ({days_ago(r['said_at'])} days): \"{r['said']}\" [{r['why']}]", cap)
    block("Promises you made, not yet followed up", promises, lambda r: f". You, {local(r['promise']['at'], '%d %b')} ({days_ago(r['promise']['at'])} days): \"{r['promise']['text']}\"", cap)
    block("Answers and updates on your tasks, nothing asked", fyi, lambda r: f". {r['said_by']}, {local(r['said_at'], '%d %b')}: \"{r['said']}\"", cap)
    block("Due in the next 3 days", due, lambda r: f", due {local(r['due'], '%a %d %b')}", cap)
    block("Overdue and still active", overdue, lambda r: f", {r['overdue_days']} days overdue, last activity {r['quiet_days']} days ago", cap)
    print(f"\n## Unassigned work in your area ({len(un_rows)}): tasks you follow, your own group, boards you watch")
    print(f"Due in the next 14 days or overdue ({len(un_soon)}):")
    for r in un_soon[:cap]:
        link = f"[{r['title']}]({r['url']})" if r["url"] else r["title"]
        late = f", {days_ago(r['due'])} days overdue" if r["due"] < NOW else ""
        print(f"- {link} ({r['where']}) id {r['id']}, due {local(r['due'], '%a %d %b')}{late}")
    if len(un_soon) > cap:
        print(f"- and {len(un_soon) - cap} more: run again with --all")
    print(f"The rest, by tracker or group ({len(un_rows) - len(un_soon)}):")
    for key, items in sorted(un_groups.items(), key=lambda kv: -len(kv[1]))[: (10_000 if a.all else 15)]:
        print(f"- {key}: {len(items)} open")
    if a.all:
        for key, items in un_groups.items():
            for r in items:
                print(f"  - {r['title']} ({key}) id {r['id']}")
    block("Shared with people who have left (yours alone now?)", left_behind, lambda r: f", with {', '.join(r['assignees'])}", cap)
    block("Gone quiet, 30 to 90 days", quiet, lambda r: f", quiet {r['quiet_days']} days", cap)
    print(f"\n{len(dead)} more tasks assigned to you have had no activity for 90+ days; not listed.")
    print("Before acting on any item, search for a sibling task for the same job (egs.py plutio search): one job often has two tasks.")


def cmd_plutio_task(a):
    t = plutio.task(a.task_id)
    if not t:
        raise SystemExit("No task with that id, or it is not visible to your Plutio access.")
    people = plutio.people()
    cs = plutio.comments(t["_id"])
    if a.json:
        return print_json({"task": t, "comments": cs})
    due = parse(t.get("dueDate"))
    print(f"# {t.get('title')}")
    print(plutio.task_url(t) if t.get("projectId") else "(no project)")
    print(f"Where: {plutio.board_path(t) or '-'} | Assigned: {', '.join(people.get(x, x) for x in t.get('assignedTo') or []) or 'nobody'}"
          f" | Due: {due.strftime('%d %b %Y') if due else 'none'} | Done: {'yes ' + t['completedAt'][:10] if t.get('completedAt') else 'no'}"
          f" | Files: {t.get('filesCount') or 0}")
    print(local_line())
    print("\n## Description\n" + ((t.get("descriptionPlain") or "").strip() or "(none)"))
    subs = t.get("subTasks") or []
    if subs:
        print(f"\n## Subtasks ({len(subs)})")
        for st in subs:
            who = ", ".join(people.get(x, x) for x in st.get("assignedTo") or []) or "nobody"
            sd = parse(st.get("dueDate"))
            print(f"- {'[done] ' if st.get('completedAt') else ''}{clean(st.get('title'), 140)} | {who}"
                  f"{' | due ' + local(sd, '%d %b') if sd else ''} | id {st.get('_id', '')}")
    print(f"\n## Thread ({len(cs)} comments, oldest first)")
    for c in cs:
        print(f"\n[{local(parse(c.get('createdAt')), '%d %b %Y %H:%M')}] {people.get(c.get('createdBy'), c.get('createdBy'))}:")
        print((c.get("bodyPlain") or "").strip())
        for att in c.get("attachments") or []:
            print(f"  attachment: {att.get('title') or att.get('name') or ''} {att.get('url') or ''}")


def cmd_plutio_search(a):
    found = {t["_id"]: t for t in plutio.search(a.words, active=not a.all)}
    if a.text:
        found.update({t["_id"]: t for t in plutio.search_text(a.words, active=not a.all)})
    people = plutio.people()
    rows = [t for t in found.values() if t.get("assignedTo") or not a.assigned]
    print(f"{len(rows)} tasks match \"{a.words}\" in {'titles and descriptions' if a.text else 'titles'}"
          f"{', including finished' if a.all else ', active only'}{', assigned only' if a.assigned else ''}")
    for t in sorted(rows, key=lambda t: t.get("updatedAt") or "", reverse=True)[:40]:
        who = ", ".join(people.get(x, x) for x in t.get("assignedTo") or []) or "nobody"
        link = f"[{clean(t.get('title'), 120)}]({plutio.task_url(t)})" if t.get("projectId") else f"{clean(t.get('title'), 120)} (no link)"
        print(f"- {link} id {t['_id']}"
              f"{' DONE' if t.get('completedAt') else ''} | {plutio.board_path(t)} | {who} | updated {(t.get('updatedAt') or '')[:10]}")


def cmd_plutio_client(a):
    name = a.name.lower()
    people = plutio.people()
    projects = plutio.projects()
    pids = [pid for pid, n in projects.items() if name in (n or "").lower()]
    window = NOW - dt.timedelta(days=a.days)
    tasks = {}
    for t in plutio.updated_since(window.strftime("%Y-%m-%dT%H:%M:%S.000Z"), active=False):
        crumbs = " ".join(b.get("title", "") for b in t.get("breadcrumb") or []).lower()
        if t.get("projectId") in pids or name in crumbs or name in (t.get("title") or "").lower():
            tasks[t["_id"]] = t
    threads = plutio.comments_many([tid for tid, t in tasks.items() if t.get("commentsCount")])
    out = []
    for tid, t in tasks.items():
        cs = [c for c in threads.get(tid, []) if (parse(c.get("createdAt")) or NOW) >= window]
        if cs or (t.get("completedAt") and parse(t["completedAt"]) >= window):
            out.append((t, cs))
    print(f"# {a.name}: Plutio activity in the last {a.days} days")
    print(f"Projects matched: {', '.join(projects[p] for p in pids) or 'none by name; matched on board and title'}. {len(out)} tasks.\n")
    for t, cs in sorted(out, key=lambda x: x[0].get("updatedAt") or "", reverse=True):
        done = f" FINISHED {t['completedAt'][:10]}" if t.get("completedAt") and parse(t["completedAt"]) >= window else ""
        title = clean(t.get('title'), 140)
        print(f"## [{title}]({plutio.task_url(t)}) id {t['_id']}{done}" if t.get("projectId") else f"## {title} (no project, no link) id {t['_id']}{done}")
        print(f"{plutio.board_path(t)} | {', '.join(people.get(x, x) for x in t.get('assignedTo') or []) or 'nobody'}")
        for c in cs:
            print(f"- {(c.get('createdAt') or '')[:10]} {people.get(c.get('createdBy'), c.get('createdBy'))}: \"{clean(c.get('bodyPlain'), 300)}\"")
        print()


# ------------------------------------------------------------------ chat

def chat_messages(days, space_filter=None):
    from egslib import gchat
    since = (NOW - dt.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return [m for m in gchat.messages_since(since, owner_name=config.me(), space_filter=space_filter) if "error" not in m]


def cmd_chat_spaces(a):
    from egslib import gchat
    chat = gchat.service()
    for s in gchat._pages(lambda t: chat.spaces().list(pageSize=1000, pageToken=t), "spaces"):
        print(f"- {s.get('displayName') or '(direct message)'} [{s.get('spaceType')}]")


def cmd_chat_read(a):
    msgs = [m for m in chat_messages(a.days, space_filter=a.space) if a.space.lower() in m["space"].lower()]
    if not msgs:
        print(f"No messages in a space matching \"{a.space}\" in the last {a.days} days.")
    for m in msgs:
        print(f"[{local(parse(m['created']), '%d %b %H:%M')}] {m['space']} | {m['sender']}: {m['text']}")


def cmd_chat_all(a):
    """Every message in every space, oldest first per space. Use it to check whether the person already replied."""
    msgs = chat_messages(a.days)
    print(local_line())
    for m in sorted(msgs, key=lambda m: (m["space"], m["created"])):
        print(f"[{local(parse(m['created']), '%d %b %H:%M')}] {m['space']} | {m['sender']}: {m['text']}")


def cmd_chat_sweep(a):
    me_name = a.me or need_me()
    team = config.team()
    staff = set(team.get("staff_names", [])) | set(team.get("vendor_names", [])) | {me_name}
    bots = set(team.get("bot_senders", []))
    internal = set(team.get("internal_spaces", []))
    prefixes = tuple(p for p in team.get("internal_space_prefixes", []) if p not in ("DM with", "Group:"))
    by_space = {}
    for m in chat_messages(a.days):
        by_space.setdefault(m["space"], []).append(m)
    mentions, clients, dms, recaps = [], [], [], []
    for space, ms in by_space.items():
        ms.sort(key=lambda m: m["created"])
        last = ms[-1]
        if ms[0].get("space_type") == "DIRECT_MESSAGE":
            closing = is_ack(last["text"]) or (len(last["text"]) < 40 and "?" not in last["text"]
                                                 and re.search(r"thank", last["text"], re.I))
            if last["sender"] != me_name and last["sender"] not in bots and not closing:
                dms.append({"space": space, "sender": last["sender"], "at": last["created"], "text": clean(last["text"], 800)})
            continue
        for i, m in enumerate(ms):
            if m["sender"] in bots:
                if "Recap:" in m["text"]:
                    recaps.append({"space": space, "at": m["created"], "text": m["text"]})
                continue
            if m["sender"] != me_name and mentions_name(m["text"], me_name) and not any(x["sender"] == me_name for x in ms[i + 1:]):
                mentions.append({"space": space, "sender": m["sender"], "at": m["created"], "text": clean(m["text"], 800)})
        is_internal = space in internal or space.startswith(prefixes)
        if not is_internal and last["sender"] not in staff and last["sender"] not in bots:
            age = days_ago(parse(last["created"]))
            if age is not None and age >= 1 and not is_ack(last["text"]):
                clients.append({"space": space, "sender": last["sender"], "at": last["created"], "age_days": age,
                                "text": clean(last["text"], 800)})
    out = {"person": me_name, "days": a.days, "spaces_with_activity": len(by_space), "mentions_unanswered": mentions,
           "clients_waiting": clients, "direct_messages_waiting": dms,
           "latest_recap": max(recaps, key=lambda r: r["at"]) if recaps else None}
    if a.json:
        return print_json(out)
    print(f"# Google Chat for {me_name}, last {a.days} days ({len(by_space)} spaces with activity)")
    print(local_line() + "\n")
    print(f"## You were mentioned and have not replied in that space ({len(mentions)})")
    for m in mentions:
        print(f"- {m['space']}: {m['sender']}, {m['at'][:10]}: \"{m['text']}\"")
    print(f"\n## Client spaces where the client spoke last ({len(clients)})")
    for c in clients:
        print(f"- {c['space']}: {c['sender']}, {c['age_days']} days ago: \"{c['text']}\"")
    print(f"\n## Direct messages where the other person spoke last ({len(dms)})")
    for d in dms:
        print(f"- {d['space']}, {d['at'][:10]}: \"{d['text']}\"")
    if out["latest_recap"]:
        r = out["latest_recap"]
        print(f"\n## Latest meeting recap ({r['space']}, {r['at'][:10]})\n{r['text']}")
        if "more..." in r["text"]:
            print("\n(The recap above is cut short by the notes tool. The full next steps are in the recap email and the notes document linked in the meeting's space; read them before listing actions.)")


# ------------------------------------------------------------------ search console / analytics

def periods(days):
    end = (NOW - dt.timedelta(days=3)).date()  # Search Console data lags about three days
    start = end - dt.timedelta(days=days - 1)
    prev_end = start - dt.timedelta(days=1)
    prev_start = prev_end - dt.timedelta(days=days - 1)
    return [str(x) for x in (start, end, prev_start, prev_end)]


def cmd_gsc_sites(a):
    from egslib import google
    for s in google.gsc_sites():
        print(f"- {s['siteUrl']} ({s.get('permissionLevel', '')})")


def cmd_gsc_report(a):
    from egslib import google
    site = google.gsc_match(a.site)
    if not site:
        raise SystemExit(f"No Search Console property you can read matches \"{a.site}\". Run: egs.py gsc sites")
    s, e, ps, pe = periods(a.days)
    cur = (google.gsc_query(site, s, e) or [{}])[0]
    prev = (google.gsc_query(site, ps, pe) or [{}])[0]
    print(f"# Search Console: {site}\n{s} to {e}, compared with {ps} to {pe}\n")
    print("| Measure | This period | Previous | Change |\n|---|---|---|---|")
    for k, label in [("clicks", "Clicks"), ("impressions", "Impressions"), ("ctr", "Click-through rate"), ("position", "Average position")]:
        c, p = cur.get(k, 0), prev.get(k, 0)
        fmt = (lambda v: f"{v * 100:.1f}%") if k == "ctr" else (lambda v: f"{v:.1f}") if k == "position" else (lambda v: f"{v:,.0f}")
        print(f"| {label} | {fmt(c)} | {fmt(p)} | {pct(c, p) if k != 'position' else f'{p - c:+.1f} places'} |")
    for dim, title in [("query", "Top queries"), ("page", "Top pages")]:
        rows = google.gsc_query(site, s, e, [dim], limit=a.limit)
        prev_rows = {r["keys"][0]: r for r in google.gsc_query(site, ps, pe, [dim], limit=250)}
        print(f"\n## {title}\n| {dim.title()} | Clicks | Change | Impressions | Position |\n|---|---|---|---|---|")
        for r in rows:
            k = r["keys"][0]
            print(f"| {k} | {r['clicks']:,.0f} | {pct(r['clicks'], prev_rows.get(k, {}).get('clicks', 0))} | {r['impressions']:,.0f} | {r['position']:.1f} |")


def cmd_ga_properties(a):
    from egslib import google
    for prop, name, acct in google.ga_properties():
        print(f"- {name} ({acct}): {prop}")


def cmd_ga_report(a):
    from egslib import google
    prop = google.ga_match(a.property)
    if not prop:
        raise SystemExit(f"No Analytics property you can read matches \"{a.property}\". Run: egs.py ga properties")
    end = NOW.date() - dt.timedelta(days=1)
    start = end - dt.timedelta(days=a.days - 1)
    pend = start - dt.timedelta(days=1)
    pstart = pend - dt.timedelta(days=a.days - 1)
    metrics = ["activeUsers", "sessions", "engagementRate", "keyEvents"]
    cur = (google.ga_report(prop, str(start), str(end), metrics) or [[0] * 4])[0]
    prev = (google.ga_report(prop, str(pstart), str(pend), metrics) or [[0] * 4])[0]
    print(f"# Analytics: {prop}\n{start} to {end}, compared with {pstart} to {pend}\n")
    print("| Measure | This period | Previous | Change |\n|---|---|---|---|")
    for i, label in enumerate(["Users", "Sessions", "Engagement rate", "Key events (conversions)"]):
        c, p = float(cur[i]), float(prev[i])
        f = (lambda v: f"{v * 100:.1f}%") if i == 2 else (lambda v: f"{v:,.0f}")
        print(f"| {label} | {f(c)} | {f(p)} | {pct(c, p)} |")
    for dims, title in [(["sessionDefaultChannelGroup"], "Where visitors came from"), (["pagePath"], "Top pages")]:
        rows = google.ga_report(prop, str(start), str(end), ["sessions", "keyEvents"], dims, limit=a.limit, order_metric="sessions")
        print(f"\n## {title}\n| {dims[0]} | Sessions | Key events |\n|---|---|---|")
        for r in rows:
            print(f"| {r[0]} | {float(r[1]):,.0f} | {float(r[2]):,.0f} |")


def cmd_pagespeed(a):
    """PageSpeed Insights for one page, mobile by default. Uses ~/.config/egs-assistant/pagespeed.json {"key": ...} if present."""
    import urllib.parse, urllib.request, urllib.error
    key = os.environ.get("PAGESPEED_KEY") or config.me_settings().get("pagespeed_key", "")
    kf = os.path.join(config.HOME_DIR, "pagespeed.json")
    if not key and os.path.exists(kf):
        key = json.load(open(kf)).get("key", "")
    qs = {"url": a.url, "strategy": a.strategy, "category": "performance"}
    if key:
        qs["key"] = key
    try:
        with urllib.request.urlopen("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?" + urllib.parse.urlencode(qs), timeout=120) as r:
            d = json.load(r)
    except urllib.error.HTTPError as err:
        if err.code == 429:
            raise SystemExit("PageSpeed Insights refused: the shared free quota is used up. Add a free API key (ask Claude to "
                             "\"connect PageSpeed\"), or run the page by hand at pagespeed.web.dev and paste the numbers.")
        raise
    lh = d.get("lighthouseResult", {})
    audits = lh.get("audits", {})
    field = (d.get("loadingExperience") or {}).get("metrics", {})
    print(f"# PageSpeed: {a.url} ({a.strategy})")
    print(f"Performance score: {round((lh.get('categories', {}).get('performance', {}).get('score') or 0) * 100)}")
    print("\n## Real visitors (Chrome field data, 28 days)" + ("" if field else ": not enough traffic for field data"))
    for k, label in [("LARGEST_CONTENTFUL_PAINT_MS", "LCP ms"), ("INTERACTION_TO_NEXT_PAINT", "INP ms"), ("CUMULATIVE_LAYOUT_SHIFT_SCORE", "CLS x100")]:
        if k in field:
            print(f"- {label}: {field[k].get('percentile')} ({field[k].get('category')})")
    print("\n## Lab test")
    for k in ["largest-contentful-paint", "total-blocking-time", "cumulative-layout-shift", "speed-index", "total-byte-weight"]:
        if k in audits:
            print(f"- {audits[k].get('title')}: {audits[k].get('displayValue', '')}")
    opps = [v for v in audits.values() if (v.get("details") or {}).get("type") == "opportunity" and (v.get("score") or 1) < 0.9]
    opps.sort(key=lambda v: -((v.get("details") or {}).get("overallSavingsMs") or 0))
    print("\n## Biggest opportunities")
    for v in opps[:6]:
        print(f"- {v.get('title')}: {v.get('displayValue', '')}")


# ------------------------------------------------------------------ sweep stamp

def cmd_sweep_done(a):
    os.makedirs(config.HOME_DIR, exist_ok=True)
    stamp = config.stamp_file()
    with open(stamp, "w") as f:
        f.write(dt.datetime.now().strftime("%Y-%m-%d") + "\n" + NOW.strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")
    print("sweep recorded")


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser(prog="egs", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="area", required=True)
    s = sub.add_parser("setup"); s.add_argument("--me", default=""); s.add_argument("--watch", action="append", default=[])
    s.set_defaults(fn=cmd_setup)
    s = sub.add_parser("check"); s.set_defaults(fn=cmd_check)
    s = sub.add_parser("sweep-done"); s.set_defaults(fn=cmd_sweep_done)
    g = sub.add_parser("google").add_subparsers(dest="cmd", required=True)
    s = g.add_parser("auth"); s.set_defaults(fn=cmd_google_auth)

    p = sub.add_parser("plutio").add_subparsers(dest="cmd", required=True)
    s = p.add_parser("sweep"); s.add_argument("--days", type=int, default=30); s.add_argument("--me", default="")
    s.add_argument("--json", action="store_true"); s.add_argument("--all", action="store_true"); s.set_defaults(fn=cmd_plutio_sweep)
    s = p.add_parser("task"); s.add_argument("task_id"); s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_plutio_task)
    s = p.add_parser("search"); s.add_argument("words"); s.add_argument("--all", action="store_true")
    s.add_argument("--text", action="store_true"); s.add_argument("--assigned", action="store_true"); s.set_defaults(fn=cmd_plutio_search)
    s = p.add_parser("client"); s.add_argument("name"); s.add_argument("--days", type=int, default=7); s.set_defaults(fn=cmd_plutio_client)

    c = sub.add_parser("chat").add_subparsers(dest="cmd", required=True)
    s = c.add_parser("spaces"); s.set_defaults(fn=cmd_chat_spaces)
    s = c.add_parser("read"); s.add_argument("space"); s.add_argument("--days", type=int, default=7); s.set_defaults(fn=cmd_chat_read)
    s = c.add_parser("all"); s.add_argument("--days", type=int, default=7); s.set_defaults(fn=cmd_chat_all)
    s = c.add_parser("sweep"); s.add_argument("--days", type=int, default=7); s.add_argument("--me", default="")
    s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_chat_sweep)

    q = sub.add_parser("gsc").add_subparsers(dest="cmd", required=True)
    s = q.add_parser("sites"); s.set_defaults(fn=cmd_gsc_sites)
    s = q.add_parser("report"); s.add_argument("site"); s.add_argument("--days", type=int, default=28)
    s.add_argument("--limit", type=int, default=15); s.set_defaults(fn=cmd_gsc_report)
    q = sub.add_parser("ga").add_subparsers(dest="cmd", required=True)
    s = q.add_parser("properties"); s.set_defaults(fn=cmd_ga_properties)
    s = q.add_parser("report"); s.add_argument("property"); s.add_argument("--days", type=int, default=28)
    s.add_argument("--limit", type=int, default=10); s.set_defaults(fn=cmd_ga_report)

    s = sub.add_parser("pagespeed"); s.add_argument("url"); s.add_argument("--strategy", default="mobile", choices=["mobile", "desktop"])
    s.set_defaults(fn=cmd_pagespeed)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()

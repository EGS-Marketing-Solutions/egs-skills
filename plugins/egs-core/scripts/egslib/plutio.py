"""Plutio API client, read-only. Quirks that are real and must stay:
form-encoded token body; a browser User-Agent (Cloudflare blocks the default one);
a `business` header on every call; ?q= takes a Mongo-style JSON filter; lists cap at 1000;
GET /tasks/<id> is 403, filter by _id instead; /users is blocked, /people gives names."""
import json, socket, time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from . import config

BASE = "https://api.plutio.com/v1.11"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
_token = None


def token():
    global _token
    if _token:
        return _token
    cid, sec = config.plutio_creds()
    body = urllib.parse.urlencode({"grant_type": "client_credentials",
                                   "client_id": cid, "client_secret": sec}).encode()
    req = urllib.request.Request(BASE + "/oauth/token", data=body, headers={
        "User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                _token = json.load(r)["access_token"]
            return _token
        except (socket.timeout, urllib.error.URLError, ConnectionError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code < 500 and e.code != 429:
                raise
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def api(path, tries=4):
    """GET with retries: Plutio times out or returns 5xx now and then, and a daily job must not die on one call."""
    req = urllib.request.Request(BASE + path, headers={
        "User-Agent": UA, "Authorization": "Bearer " + token(), "business": config.BUSINESS})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.load(r)
            break
        except (socket.timeout, urllib.error.URLError, ConnectionError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code < 500 and e.code != 429:
                raise
            if attempt == tries - 1:
                raise
            time.sleep(2 * (attempt + 1))
    if isinstance(data, dict) and "_id" in data:
        return [data]
    return [x for x in (data or []) if isinstance(x, dict)]


def q(obj):
    return urllib.parse.quote(json.dumps(obj))


def people():
    """person id -> display name"""
    out = {}
    for u in api("/people"):
        nm = u.get("name") or u.get("fullName")
        if isinstance(nm, dict):
            nm = " ".join(filter(None, [nm.get("first"), nm.get("last")])).strip()
        out[u["_id"]] = nm or u["_id"]
    return out


def projects():
    """project id -> name"""
    return {p["_id"]: (p.get("name") or p["_id"]) for p in api("/projects?q=" + q({}))}


def active_tasks_for(person_id):
    return api("/tasks?q=" + q({"assignedTo": person_id, "completedAt": None}))


def followed_tasks_for(person_id):
    return api("/tasks?q=" + q({"followers": person_id, "completedAt": None}))


def due_between(start_iso, end_iso):
    return api("/tasks?q=" + q({"dueDate": {"$gte": start_iso, "$lte": end_iso}, "completedAt": None}))


def search_text(text, active=True):
    filt = {"descriptionPlain": {"$regex": text, "$options": "i"}}
    if active:
        filt["completedAt"] = None
    return api("/tasks?q=" + q(filt))


def active_tasks_in(project_id):
    return api("/tasks?q=" + q({"projectId": project_id, "completedAt": None}))


def task(task_id):
    """One task by id, including completed ones. GET /tasks/<id> is refused; the filter works."""
    r = api("/tasks?q=" + q({"_id": task_id}))
    return r[0] if r else None


def updated_since(iso, active=True):
    filt = {"updatedAt": {"$gte": iso}}
    if active:
        filt["completedAt"] = None
    return api("/tasks?q=" + q(filt))


def search(text, active=True):
    filt = {"title": {"$regex": text, "$options": "i"}}
    if active:
        filt["completedAt"] = None
    return api("/tasks?q=" + q(filt))


def comments(task_id):
    cs = api("/comments?q=" + q({"entityType": "task", "entityId": task_id}))
    cs.sort(key=lambda c: c.get("createdAt", ""))
    return cs


def comments_many(task_ids, workers=6):
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return dict(zip(task_ids, ex.map(comments, task_ids)))


def task_url(t):
    return f"{config.PORTAL}/projects/{t.get('projectId')}/tasks/{t['_id']}"


def board_path(t):
    """'Task board > Task group' from the breadcrumb, without the project."""
    bc = t.get("breadcrumb") or []
    return " > ".join(b.get("title", "") for b in bc if b.get("entityType") != "project")

"""Google Chat reader. Locally it uses a signed-in user's OAuth token. On Cloud Run it will use a
Workspace service account with domain-wide delegation (GCHAT_SA_KEY + GCHAT_SA_SUBJECT)."""
import json, os
from . import config

# One Google sign-in covers every read the team needs. All read-only.
SCOPES = ["https://www.googleapis.com/auth/chat.spaces.readonly",
          "https://www.googleapis.com/auth/chat.messages.readonly",
          "https://www.googleapis.com/auth/chat.memberships.readonly",
          "https://www.googleapis.com/auth/webmasters.readonly",
          "https://www.googleapis.com/auth/analytics.readonly"]
CHAT_SCOPES = SCOPES[:3]


def credentials(scopes=None):
    """The person's Google sign-in (or the hosted assistant's service account), refreshed if needed."""
    from google.auth.transport.requests import Request
    if config.GCHAT_SA_KEY:
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_file(config.GCHAT_SA_KEY, scopes=scopes or CHAT_SCOPES)
        if config.GCHAT_SA_SUBJECT:
            creds = creds.with_subject(config.GCHAT_SA_SUBJECT)
    else:
        from google.oauth2.credentials import Credentials
        if not os.path.exists(config.GCHAT_TOKEN):
            raise SystemExit("Google is not signed in on this computer. Ask Claude to \"connect Google Chat\".")
        creds = Credentials.from_authorized_user_file(config.GCHAT_TOKEN)
        if not creds.valid and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(config.GCHAT_TOKEN, "w") as f:
                f.write(creds.to_json())
    return creds


def granted(scope):
    try:
        return scope in (credentials().scopes or [])
    except SystemExit:
        return False


def service():
    from googleapiclient.discovery import build
    return build("chat", "v1", credentials=credentials(), cache_discovery=False)


def _pages(call, key):
    tok = None
    while True:
        resp = call(tok).execute()
        for item in resp.get(key, []):
            yield item
        tok = resp.get("nextPageToken")
        if not tok:
            return


def messages_since(since_iso, owner_name="", space_filter=None):
    """Every message in every space the signed-in identity can see, newest last, with the space label.
    With space_filter, only named spaces whose name contains it are read (much faster)."""
    chat = service()
    out = []
    for s in _pages(lambda t: chat.spaces().list(pageSize=1000, pageToken=t), "spaces"):
        if space_filter and space_filter.lower() not in (s.get("displayName") or "").lower() and s.get("displayName"):
            continue
        try:
            msgs = list(_pages(lambda t: chat.spaces().messages().list(
                parent=s["name"], filter=f'createTime > "{since_iso}"', orderBy="createTime asc",
                pageSize=1000, pageToken=t), "messages"))
        except Exception as e:  # a space we cannot read is reported, not fatal
            out.append({"space": s.get("displayName") or s["name"], "error": str(e)[:200]})
            continue
        if not msgs:
            continue
        names = {}
        try:
            for m in _pages(lambda t: chat.spaces().members().list(parent=s["name"], pageSize=1000, pageToken=t), "memberships"):
                mem = m.get("member", {})
                if mem.get("name"):
                    names[mem["name"]] = mem.get("displayName") or ""
        except Exception:
            pass
        label = s.get("displayName")
        if not label:
            others = sorted({n for n in names.values() if n and n != owner_name})
            label = ("DM with " if s.get("spaceType") == "DIRECT_MESSAGE" else "Group: ") + (", ".join(others) or s["name"])
        for m in msgs:
            snd = m.get("sender", {})
            out.append({"space": label, "space_type": s.get("spaceType"), "space_id": s["name"],
                        "created": m.get("createTime"), "thread": (m.get("thread") or {}).get("name"),
                        "sender": snd.get("displayName") or names.get(snd.get("name"), "") or snd.get("name"),
                        "text": m.get("text") or m.get("formattedText") or ""})
    return out

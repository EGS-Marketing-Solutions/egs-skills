"""Settings. Environment variables first (Cloud Run secrets), then the person's own files in
~/.config/egs-assistant/ (never in the repo)."""
import json, os, re

PORTAL = os.environ.get("PLUTIO_PORTAL", "https://clientportal.egs-solutions.com")
BUSINESS = os.environ.get("PLUTIO_BUSINESS", "egs")
TEAM_BOARD = os.environ.get("PLUTIO_TEAM_BOARD", "ssSBY3uox2sn374Zg")
HOME_DIR = os.path.expanduser(os.environ.get("EGS_CONFIG_DIR", "~/.config/egs-assistant"))
PLUTIO_FILE = os.path.join(HOME_DIR, "plutio.json")
ME_FILE = os.path.join(HOME_DIR, "me.json")
GCHAT_TOKEN = os.path.expanduser(os.environ.get("GCHAT_TOKEN", os.path.join(HOME_DIR, "google-token.json")))
GOOGLE_CLIENT = os.path.join(HOME_DIR, "google-client.json")
GCHAT_SA_KEY = os.environ.get("GCHAT_SA_KEY", "")  # service-account JSON path, for the hosted assistant
GCHAT_SA_SUBJECT = os.environ.get("GCHAT_SA_SUBJECT", "")  # Workspace user the hosted assistant reads as

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROSTER_CANDIDATES = [os.environ.get("EGS_TEAM_FILE", ""),
                      os.path.join(_HERE, "..", "..", "skills", "egs", "references", "team", "roster.json"),  # in the plugin
                      os.path.join(_HERE, "..", "team.json")]                                # in the container


def plutio_creds():
    cid, sec = os.environ.get("PLUTIO_CLIENT_ID"), os.environ.get("PLUTIO_CLIENT_SECRET")
    if cid and sec:
        return cid, sec
    for path in (PLUTIO_FILE, os.path.expanduser("~/.config/plutio-egs/creds.json")):
        if os.path.exists(path):
            with open(path) as f:
                c = json.load(f)
            if c.get("client_id") and c.get("client_secret"):
                return c["client_id"], c["client_secret"]
    raise SystemExit("Plutio is not set up on this computer. Ask Claude to \"connect Plutio\".")


def me():
    """The person at this keyboard, by their name as Plutio and Chat show it."""
    if os.environ.get("EGS_ME"):
        return os.environ["EGS_ME"]
    if os.path.exists(ME_FILE):
        with open(ME_FILE) as f:
            return (json.load(f).get("name") or "").strip()
    return ""


def me_settings():
    if os.path.exists(ME_FILE):
        with open(ME_FILE) as f:
            return json.load(f)
    return {}


def watch():
    """Board or group names this person keeps an eye on, from me.json "watch" (plus their own group)."""
    return [w for w in me_settings().get("watch", []) if w]


def stamp_file():
    """Where today's sweep is recorded, one per person on this computer."""
    who = re.sub(r"[^a-z0-9]+", "-", me().lower()).strip("-")
    return os.path.join(HOME_DIR, f"last-sweep-{who}" if who else "last-sweep")


def team():
    for p in _ROSTER_CANDIDATES:
        if p and os.path.exists(p):
            with open(p) as f:
                return json.load(f)
    raise SystemExit("team roster not found (references/team/roster.json)")

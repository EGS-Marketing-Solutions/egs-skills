"""Search Console and Google Analytics, read-only, on the person's own Google sign-in.
The person only sees the sites and properties their Google account already has access to."""
from . import gchat

WEBMASTERS = "https://www.googleapis.com/auth/webmasters.readonly"
ANALYTICS = "https://www.googleapis.com/auth/analytics.readonly"


def _svc(name, version):
    from googleapiclient.discovery import build
    return build(name, version, credentials=gchat.credentials(), cache_discovery=False)


# ---------------------------------------------------------------- Search Console

def gsc_sites():
    return _svc("searchconsole", "v1").sites().list().execute().get("siteEntry", [])


def gsc_query(site, start, end, dimensions=None, limit=25):
    body = {"startDate": start, "endDate": end, "rowLimit": limit}
    if dimensions:
        body["dimensions"] = dimensions
    return _svc("searchconsole", "v1").searchanalytics().query(siteUrl=site, body=body).execute().get("rows", [])


def gsc_match(name):
    """The site whose address contains `name` (case-insensitive), or None."""
    name = name.lower().replace("https://", "").replace("http://", "").strip("/")
    hits = [s["siteUrl"] for s in gsc_sites() if name in s["siteUrl"].lower()]
    return hits[0] if hits else None


# ---------------------------------------------------------------- Analytics (GA4)

def ga_properties():
    """[(property resource name, display name, account name)] for every GA4 property the person can read."""
    out = []
    req = _svc("analyticsadmin", "v1beta").accountSummaries()
    page = None
    while True:
        resp = req.list(pageSize=200, pageToken=page).execute()
        for acct in resp.get("accountSummaries", []):
            for p in acct.get("propertySummaries", []):
                out.append((p["property"], p.get("displayName", ""), acct.get("displayName", "")))
        page = resp.get("nextPageToken")
        if not page:
            return out


def ga_match(name):
    if name.startswith("properties/") or name.isdigit():
        return name if name.startswith("properties/") else "properties/" + name
    hits = [p for p in ga_properties() if name.lower() in (p[1] + " " + p[2]).lower()]
    return hits[0][0] if hits else None


def ga_report(prop, start, end, metrics, dimensions=None, limit=10, order_metric=None):
    body = {"dateRanges": [{"startDate": start, "endDate": end}],
            "metrics": [{"name": m} for m in metrics], "limit": limit}
    if dimensions:
        body["dimensions"] = [{"name": d} for d in dimensions]
    if order_metric:
        body["orderBys"] = [{"metric": {"metricName": order_metric}, "desc": True}]
    resp = _svc("analyticsdata", "v1beta").properties().runReport(property=prop, body=body).execute()
    rows = []
    for r in resp.get("rows", []):
        rows.append([d["value"] for d in r.get("dimensionValues", [])] + [m["value"] for m in r.get("metricValues", [])])
    return rows

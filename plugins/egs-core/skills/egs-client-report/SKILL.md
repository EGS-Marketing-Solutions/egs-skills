---
name: egs-client-report
description: Builds a monthly or weekly results report for an EGS client from Search Console, Google Analytics, Google Business Profile, Amplify counts, ads results and the work delivered in Plutio, matching the client's previous report format. Use it for any client report, monthly report, SEO results, ads results, or "how did <client> do this month".
---

# Client report

Load the egs skill first; its rules apply here.

## 1. Find the last report

Search the client's Drive folder for the previous report. If one exists, match its sections,
order and tone exactly; clients read reports by habit. If none exists, use the structure below.

## 2. Gather, for the period and the one before it

Use whatever is connected; name what is not.

- **Website (Google Analytics):** `egs.py ga report "<client>" --days 30`: users, sessions,
  engagement, key events, channels, top pages, with the change from the period before.
- **Search (Search Console):** `egs.py gsc report "<client domain>" --days 28`: clicks,
  impressions, click-through rate, position, top queries and pages, with changes.
- **Google Business Profile:** views, calls, direction requests, website clicks, new reviews.
- **Amplify:** stage counts in the practice's pipeline (new leads, booked, signed up), form
  submissions, campaign sends and open rates. Counts only, never patient names.
- **Ads:** spend, results, cost per result, from the ad platform or the ads team's report.
- **Work delivered:** from Plutio, finished tasks for the client in the period
  (`egs.py plutio client "<client>" --days 31`): blogs published, pages built,
  sequences launched.

Compare each number to the previous period. A number with no comparison means little.

## 3. Write

```
# <Client>: <Month Year> results

## The short version
Three sentences: what improved, what did not, what we do next.

## Results
| Measure | This month | Last month | Change |

## What we did
- <deliverable>, <date>, <link if public>.

## What it means
Two or three plain points, each tied to a number above.

## Next month
- <planned work>, and anything we need from you.
```

Never invent a cause. If a number dropped and the sources do not say why, say "we are looking
into it" and add it as a question for the person. Round sensibly; no false precision.

## 4. Hand over

Save to `drafts/<date>/<client>/report-<month>.md`, list every source and anything that could not
be read. The person moves it into the client's Drive folder in the agreed format.

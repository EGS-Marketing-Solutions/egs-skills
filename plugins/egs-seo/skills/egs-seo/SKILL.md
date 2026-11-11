---
name: egs-seo
description: SEO and AI search for EGS clients, most of them membership-based primary care practices: monthly trackers and plan tiers, keywords, technical checks and Core Web Vitals, schema for practices and multi-location clinics, Google Business Profile, citations, getting named by ChatGPT, Perplexity and Google's AI answers, and the SEO work to draft automatically every sweep. Use it for any SEO, AI search, schema, page speed, ranking, Search Console, blog brief or Google Business Profile work for an EGS client.
---

# SEO and AI search at EGS

For whoever does SEO at EGS, and for any Claude helping them. Read it before SEO work. It covers how
we win search and AI answers for our clients, what we include in which plan, and what you produce
on your own during the sweep.

## Who we rank, and why it is different

Most of our SEO clients are membership-based primary care practices, also called direct primary
care. Health is a "your money or your life" topic: search engines and AI assistants hold it to a
higher bar of trust than almost anything else. Three consequences run through everything below:

- **Trust signals are not optional.** Named authors with credentials, clinician review, cited
  sources, a real address and real people.
- **Local intent dominates.** Patients search "direct primary care near me", "doctor without
  insurance <city>", "membership doctor <city>". The map pack and the Google Business Profile
  matter as much as the website.
- **Patient privacy shapes the tactics.** No tracking on patient-only pages, no confirming in a
  review reply that someone is a patient, no patient stories without written consent.

## Where the SEO work lives

- **The monthly trackers are the roster and the work list.** `SEO Task Board > <Month> Task Per Client
  based on Plan` holds one tracker per SEO client, named "<Client> - <Month Year>", each with its
  plan's deliverables as subtasks. `egs.py plutio sweep` lists them under "Unassigned work in your
  area", grouped by tracker; `egs.py plutio task <tracker id>` lists the subtasks. Read the tracker
  before planning a client's month.
- **Strategy clients** (for example a practice on a 180-day execution calendar) have their own plan
  group on the team board instead of, or as well as, a tracker. Their calendar tasks are the plan.
- **Blogs** run through `SEO Task Board > <Month> Blog Process`, one task per client.

## What is in which plan (EGS standard, 2 November 2026)

- **Website build only:** on-page basics on every page (title, meta description, one H1, alt text,
  clean URLs), schema on the core pages (home, about, contact, services, up to five), and a 301
  redirect map from the old site. Nothing ongoing.
- **SEO plans are tiered.** The entry tier is Local Search Essentials; higher tiers raise the
  monthly counts (for example Google Business Profile posts 4, 8 or 12 a month; links 1, 3 or 5).
  The client's tracker is the source of truth for what their tier includes; read it rather than
  assuming.
- **Deliverable types you will see on trackers:** data verification, competitor analysis, backlink
  audit, AI search (LLM) tracking in Search Atlas, local rank heatmap, citations, internal links,
  content optimisation (including "AI answered" content), press release, sitemap submission,
  technical audit and fixes, Google Business Profile posts and replies, reporting.

When a website-only client asks for SEO work, say it is an SEO plan item and draft the polite reply
for the account manager. Do not do the work unasked.

## Keywords and content for practices

Map keywords to intent, one primary intent per page:

| Intent | Typical searches | Page that answers it |
|---|---|---|
| Find a practice | direct primary care <city>, membership doctor near me, family doctor accepting new patients <city> | Home and location pages |
| Understand the model | what is direct primary care, DPC vs concierge medicine, DPC vs insurance | Pillar guide on the model |
| Price | how much is direct primary care, DPC membership cost <city> | Membership and pricing page |
| Specific need | doctor without insurance, primary care for small business employees, HSA and DPC | Service and audience pages, blogs |
| Trust | <doctor name> reviews, <practice name> | About, provider bios, Google Business Profile |

Content rules:
- Answer the question in the first two sentences under the heading that asks it. Then explain.
- One page per real location. Service-area content is fine where it genuinely helps a reader in that
  area; thin city pages with swapped place names are not, and they get demoted.
- Every health article names its author, says it was reviewed by the practice's clinician when it
  was, cites reputable sources (CDC, NIH, peer-reviewed journals, professional bodies), and shows a
  reviewed date.
- No claims of outcomes or cures. Describe access, time with the doctor, price transparency, the
  experience.
- Internal links: every blog links to the relevant service page and to the membership page; pillar
  pages link to their cluster articles and back.

## Technical basics we check on every site

- **Indexing:** the site is verified in Search Console, the sitemap is submitted, important pages are
  indexed, no key page carries `noindex` or is blocked in robots.txt.
- **Speed (Core Web Vitals, good thresholds):** Largest Contentful Paint at or under 2.5 seconds,
  Interaction to Next Paint at or under 200 milliseconds, Cumulative Layout Shift at or under 0.1.
  Measure before guessing (`egs.py pagespeed <url>`); Duda already serves images as WebP, so the
  weight is usually elsewhere: a heavy HTML document, large script bundles, third-party widgets
  (including our own Amplify chat widget and embedded form iframes, which can load on demand
  instead of on page open), duplicate tag containers, and videos that load on page open.
- **One tag container per site, owned by EGS.** One Google Tag Manager container, one GA4 property.
  Duplicate tags double-count. If a tag exists that EGS cannot open, replace it with one EGS owns.
- **Key events in GA4:** form submissions, calls from click-to-call, booking completions.
- **Redirects:** when a site is rebuilt, every old URL gets a 301 to its new home. Losing old URLs
  loses rankings.
- **Mobile:** tap targets, readable text, no horizontal scroll, phone number tappable.

## Schema markup

Use JSON-LD in the page head. Mark up only what is visible on the page.

**First, read what is already there.** Copy the existing JSON-LD from the live page source and parse
it. Invalid JSON is silently ignored by search engines; finding it is often the quickest win.

The practice, one location:

```json
{
  "@context": "https://schema.org",
  "@type": "MedicalClinic",
  "name": "<practice name exactly as on Google Business Profile>",
  "url": "https://<domain>/",
  "logo": "https://<domain>/<logo path>",
  "image": "https://<domain>/<photo of the practice>",
  "telephone": "<+1 phone>",
  "email": "<public email>",
  "address": {"@type": "PostalAddress", "streetAddress": "", "addressLocality": "", "addressRegion": "", "postalCode": "", "addressCountry": "US"},
  "geo": {"@type": "GeoCoordinates", "latitude": 0, "longitude": 0},
  "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "17:00"}],
  "medicalSpecialty": "PrimaryCare",
  "sameAs": ["<Google Business Profile URL>", "<Facebook>", "<Instagram>", "<LinkedIn>"]
}
```

**Two or more locations:** one `MedicalClinic` block per location, each on its own location page,
each with its own address, phone, hours and Google Business Profile in `sameAs`, linked to the
practice with `"parentOrganization": {"@type": "MedicalOrganization", "name": "<practice>", "url": "<home>"}`.
The home page carries the `MedicalOrganization` with `"department"` listing each clinic.

**Providers:** a doctor's bio page can use `Physician`; a nurse practitioner or physician assistant
is never `Physician`. Use `Person` with `jobTitle` (for example "Family Nurse Practitioner") and
`worksFor` pointing at the clinic.

**Offers and events:** remove or update any `validThrough` or event date that has passed; stale
dates make the markup misleading.

Also: `BreadcrumbList` on inner pages; `BlogPosting` on articles with `author` (a `Person` with
`jobTitle` and a link to their bio) and `datePublished`/`dateModified`; `MedicalWebPage` with
`reviewedBy` and `lastReviewed` on clinician-reviewed health pages; `FAQPage` where a page has a
visible question-and-answer section. Two cautions: Google shows FAQ rich results only for a narrow
set of authoritative sites now, so FAQ markup is for understanding, not for stars; and never mark
up the practice's own reviews or ratings on its own site, because self-serving review markup is not
eligible and can draw a manual action.

Every schema draft ends with: "Test in Google's Rich Results Test and the Schema.org validator
before publishing."

## Google Business Profile

- Primary category that matches the practice (for example Family practice physician or Medical
  clinic); add the secondary categories that are true.
- Services and products listed, including membership tiers, with plain descriptions.
- A post at least weekly: an offer, an update, an event, an article. Each with a photo and a link.
- Photos of the real building, team and rooms; no stock.
- Reviews: ask every member, every time, through the practice's review request workflow. Reply to
  every review within a few days. **In replies never confirm that the reviewer is a patient or
  mention anything about their care**; thank them generally and invite them to call.
- Name, address and phone identical everywhere: site, profile, directories.

## Backlinks and citations

Earned, local and relevant. Good sources for practices: local chambers of commerce, employer
partners (practices that sell to businesses), local news and podcasts, community sponsorships,
health directories (Healthgrades, Vitals, WebMD, Zocdoc where used), and direct primary care
directories. Build them by hand and record each in the client's link sheet. Never buy links, use
link networks, or swap links at scale.

## AI search: being the answer

Patients increasingly ask ChatGPT, Gemini, Perplexity, Claude and Google's AI Overviews instead of
scrolling results. To be named and cited:

- **Be quotable.** Short, self-contained answers under question-shaped headings. Specific facts:
  price ranges, what is included, who it is for, the city.
- **Be consistent.** The same name, address, phone, prices and services on the site, the Google
  Business Profile, directories and social profiles. AI systems cross-check.
- **Be mentioned elsewhere.** Assistants lean on third-party sources: directories, local news,
  "best of" lists, community discussions. Each mention is a vote.
- **Be readable by AI crawlers.** robots.txt should not block search crawlers such as OAI-SearchBot,
  PerplexityBot, Claude-SearchBot and Googlebot unless the client decided to. Key content in HTML,
  not only in images or video.
- **Be current.** Visible updated dates on pages that change. Stale prices get quoted wrong.

**AI citation tracking, monthly, per SEO client:**
- **Where it lives:** Search Atlas is EGS's tool for AI search (LLM) tracking; each tracker has a
  subtask for it. Claude reads its exports when the person shares them. Alongside it, keep a fixed
  set of ten to fifteen prompts per client in the client's SEO folder in Drive ("AI citation
  prompts"), unchanged month to month so results compare.
- **Which assistants:** ChatGPT, Perplexity, Google's AI Overviews or AI Mode, and Gemini. Claude can
  run the set through its own web search as a first pass and must say that is what it did; the
  person spot-checks the others.
- **What to record per prompt:** whether the client is named, whether it is linked, and which sources
  the answer cites.
- **Check the client's name, address and phone in every cited source.** Assistants repeat what
  third-party pages say; an old address in a news article becomes the answer. Those sources go on
  the citations list to correct.

## Produce automatically during the sweep

Produce these without being asked whenever the inputs exist. Each goes to `drafts/<date>/<client>/`.

1. **Monthly SEO report** on the first working day, for every SEO client
   (the egs-client-report skill, with `egs.py gsc report` and `egs.py ga report`).
2. **Tracker work Claude can do from what it can read:** data verification (the Client Information
   Sheet against the live site and the Google Business Profile), competitor analysis, the citations
   and name-address-phone audit, internal link plans, content optimisation drafts, press release
   drafts, technical audit notes. Name the tracker subtask each one completes.
3. **Weekly Search Console watch:** the five queries or pages that moved most, each with the fix
   written out. Without Search Console access, say so and pick pages by visible defects instead
   (missing or duplicate titles, thin pages, broken links), clearly labelled as such.
4. **Title and meta rewrites:** three options per page, under 60 and 155 characters, for pages with
   high impressions and low click-through, or by visible defects when the data is not connected.
5. **Schema** for the core pages of every new website build and every new location or provider page,
   plus a parse of the existing markup on any site you touch.
6. **A 301 redirect map** for every site rebuild: old URL, new URL, status.
7. **Blog topics and briefs:** topics need the client's approval first, so when a month has no
   approved topics, propose five with the keyword and intent for each. For approved topics without a
   brief, write the brief: keyword and intent, the question to answer first, outline, internal
   links, FAQs, sources to cite, word count, an image block (what each image should show), and the
   client's rejected phrases.
8. **AI citation check** monthly, as above.
9. **Page speed notes** with `egs.py pagespeed <url>` for any site with a new build or a complaint:
   the measured numbers and the top three fixes in an order Duda allows. If the tool reports the
   quota is used up, say so and give the person the pagespeed.web.dev link to run by hand.
10. **Google Business Profile posts** for clients whose plan includes them: written as a two-month
    document for client approval, with a photo direction for each (a real practice photo where one
    exists; otherwise a short image prompt for the design team, never a stock photo of a doctor).
    Who schedules them (SEO or social, through Amplify) is decided per client; ask if unclear.
11. **Scope replies:** when a website-only client asks for SEO plan work, the polite reply for the
    account manager.

Not SEO's: anything that contacts patients (testimonial requests, reviews from named patients). Route
it to the account manager.

Anything that changes a live site, a profile or an account is done by a person from these drafts.

## Quality bar

- Every recommendation names the page or query it applies to and the number that justifies it.
- No invented numbers. If Search Console or Analytics could not be read, the report says so.
- Health claims checked against the source cited.
- Every change a person will make is written so they can copy it exactly.

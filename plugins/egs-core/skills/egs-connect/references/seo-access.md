# SEO access checklist

What an SEO specialist needs beyond the Google sign-in, and who grants it. Check each, once, and
record gaps in the setup table.

| Access | Where it is granted | Who grants it |
|---|---|---|
| Search Console, each client property | Search Console > Settings > Users and permissions | The property owner (EGS account or the client) |
| Google Analytics, each property | Admin > Property access management, role Viewer | The property owner |
| Google Business Profile, each location | Business Profile > Business profile settings > Managers | The profile owner |
| Google Tag Manager, each container | Admin > User Management | The container owner |
| Duda editor, each site | Duda > Sites > the site > permissions | The Duda account owner at EGS |
| Search Atlas (AI search tracking, rank tracking) | Search Atlas team settings | The EGS Search Atlas account owner |
| PageSpeed key | `references/pagespeed.md` | The person themselves |

Claude reads Search Console and Analytics through `egs.py` once access exists. Search Atlas, Duda,
Tag Manager and Business Profile have no reader in this skill: the person exports or screenshots
what Claude needs, or Claude reads the public result (the live page, the public profile).

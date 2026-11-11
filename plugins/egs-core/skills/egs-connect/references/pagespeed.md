# PageSpeed Insights key

**For:** SEO and websites. **What it gives:** `egs.py pagespeed <url>` measures a page's Core Web
Vitals and lists the biggest fixes. Without a key it shares a small public quota that is often used
up. **Time:** 5 minutes, once. **Needs an API key**, free.

## Walk-through

1. Open console.cloud.google.com with the egs-solutions.com account. Pick the EGS project (top bar).
2. APIs & Services > Library. Search "PageSpeed Insights API". Click Enable.
3. APIs & Services > Credentials > Create credentials > API key. Copy the key.
4. Click the new key, then under API restrictions choose "Restrict key" and tick PageSpeed Insights
   API only. Save.
5. Open a new file in a plain text editor: `~/.config/egs-assistant/pagespeed.json`, containing
   `{"key": "<the key>"}`. Save. Never paste the key into the chat.
6. Run `egs.py pagespeed https://<a client site>`.

## Check

The output shows a performance score and the lab numbers. "Real visitors" may say there is not
enough traffic; that is normal for small sites.

## If it fails

- "quota is used up": the key is not being read. Check the file name and that it is valid JSON.
- "API key not valid": the key was restricted to a different API, or copied incompletely.

## Manual fallback

pagespeed.web.dev: paste the page address, run Mobile, and copy the numbers into the draft.

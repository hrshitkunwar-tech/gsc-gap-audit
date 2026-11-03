# gsc-gap-audit

Find the Search Console queries you already rank for that no page owns.

No credentials, no API, no install. It reads the CSV that Search Console
already exports, so it runs on someone else's site as easily as your own.

## Quickstart, 30 seconds

In Search Console: **Performance → Queries → Export → CSV**. Then:

```
python3 gsc_gap_audit.py Queries.csv --sitemap https://example.com/sitemap.xml
```

Python 3.10+. Standard library only. `--sitemap` is the only thing that
touches the network, and only to read the sitemap.

For the cannibalisation report, export a second CSV with both dimensions
(Performance → add the **Pages** dimension alongside Queries) and pass it:

```
python3 gsc_gap_audit.py Queries.csv --pages-csv QueriesAndPages.csv
```

## What it reports, in the order worth acting on

**1. Cannibalisation.** Two or more of your own URLs ranking for the same
query. This is the only finding that is costing you a position you already
earned, which is why it is first. On our own site it found a blog post and a
docs page sharing a slug, at positions 85.4 and 77.7 on the same query —
Google was holding both and ranking neither.

**2. Striking distance.** Queries already inside a position you could move,
with enough impressions to be worth moving, sorted by impressions. This is
usually the largest surprise: the traffic is not somewhere new, it is sitting
at position 6 getting no clicks.

**3. Uncovered.** Query clusters with real impressions whose words appear in
no URL in your sitemap. These are the pages you have not written. Coverage is
judged by sitemap path words, which is a proxy and will produce false
positives on sites whose URLs are opaque ids — read the examples, not the
label.

## Real output

This is the tool run against mindlyft.io, unedited, and the full file is in
[`example-output.txt`](example-output.txt):

```
500 queries, 2504 impressions, 8 clicks

== STRIKING DISTANCE == position < 20, impressions >= 5
    113 imp  pos   6.7  mindlyft
     73 imp  pos  11.5  crm updates
     45 imp  pos   3.7  gtm engineer club alternatives
     22 imp  pos  16.5  auto update hubspot after calls
     17 imp  pos   4.2  for team collaboration, is agentforce or copilot better?
     16 imp  pos   5.9  ai agent platform with centralized policy rbac and approval workflows wh
     14 imp  pos   2.2  choose automatic crm updates tool
  -- 59 queries, 777 impressions in reach

== UNCOVERED == clusters whose words appear in no sitemap URL
     45 imp  pos   3.7  alternatives club         e.g. gtm engineer club alternatives
     20 imp  pos  64.8  confluence sync           e.g. confluence to zendesk sync
```

777 impressions sitting under position 20 on a site getting 8 clicks. That gap
is the whole reason this exists.

## Limits, stated plainly

- **Clustering is crude on purpose.** Queries are grouped by their two most
  distinctive tokens. It surfaces a theme worth a page; it is not a taxonomy,
  and it will occasionally put two unrelated queries together.
- **Coverage is a path-word proxy.** A page can cover a topic without the word
  appearing in its URL, and that will show as a false "uncovered". Treat the
  section as a list to check, not a list to act on.
- **Search Console samples and truncates.** The export is not every query, and
  anonymised queries are missing entirely. Positions are averages over the
  period, so a query at 11.5 may never have been at 11.5 on any single day.
- **It tells you nothing about intent.** A query you rank 3rd for may belong to
  someone who will never buy from you. Our own run is full of them. Read the
  queries.
- **No fix is suggested, deliberately.** Deciding whether a cluster deserves a
  new page or a section on an existing one is the judgement the tool cannot
  make, and guessing it is how sites end up cannibalising themselves.

## Licence

MIT — see [LICENSE](LICENSE). The code and this README are MIT. The Mindlyft
name and logo are not; they are excluded from the licence grant.

---

Built by Mindlyft. We ran this on our own site and it found two pages
competing with each other and 777 impressions we were not converting. If you
would rather not maintain the fixing part yourself, that is what we do:
<https://mindlyft.io/r/gh>

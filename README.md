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

This is the tool run against mindlyft.io for the 28 days to 3 November 2026,
unedited. The full file is in [`example-output.txt`](example-output.txt):

```
803 queries, 3989 impressions, 9 clicks

== STRIKING DISTANCE == position < 20, impressions >= 5
    125 imp  pos   6.3  mindlyft
     78 imp  pos  11.8  crm updates
     63 imp  pos   4.3  gtm engineer club alternatives
     30 imp  pos   3.7  what gtm software supports salesforce hubspot bidirectional sync?
     27 imp  pos   2.4  clay zoominfo apollo gtm product launch ai sales october 2026
     22 imp  pos  16.5  auto update hubspot after calls
     20 imp  pos   2.5  choose automatic crm updates tool
  -- 92 queries, 1158 impressions in reach

== UNCOVERED == clusters whose words appear in no sitemap URL
     63 imp  pos   4.3  alternatives club         e.g. gtm engineer club alternatives
     21 imp  pos  66.4  confluence sync           e.g. confluence to zendesk sync
```

Nine clicks. Eight of those nine were people who typed "mindlyft" into Google,
so one stranger found the site through search in twenty-eight days. Meanwhile
3,989 impressions went somewhere. That gap is the whole reason this exists.

Read the fifth row before you get excited about any of this. `clay zoominfo
apollo gtm product launch ai sales october 2026` is somebody's monitoring robot,
not a buyer, and the tool has no way to tell the difference. Neither does any
other tool that claims it can.

## No terminal? There is a browser version

<https://mindlyft.io/tools/search-console-gap-audit> runs the same three checks
on the CSVs Search Console exports, with no install and no account. Your file is
read by your own browser and is never uploaded. This CLI is still the one to use
for true query-level collisions, because it accepts a query+page export and the
browser version only has the separate Queries and Pages files to work from.

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

Built by Mindlyft. We ran it on our own site first. It found two of our pages
competing with each other, our home page indexed at both http and https, and
3,989 impressions earning nine clicks. We get paid for the fixing, not the
finding, and the finding is yours to keep either way:
<https://mindlyft.io/r/gh>


---

### Production Services & Toolkits
- **[5-Day Post-Call & CRM Sync Build ($500 flat, Contra)](https://contra.com/s/RmWZoMo3-end-to-end-post-call-automation-and-crm-sync-engine?r=harshit_kunwar_m0yu7crm)**
- **[30-Min Live GTM Teardown (Topmate)](https://topmate.io/harshit_kunwar/2370556)**
- **[GTM Operator Packs ($29–$59, Whop)](https://whop.com/mindlyft-io/products/)** · **[Mindlyft Shop](https://mindlyft.shop)**
- **[GTM Engineering Services](https://mindlyft.io/services)** · **[Pricing](https://mindlyft.io/pricing)**

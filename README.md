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
earned, which is why it is first. The usual case is a blog post and a docs
page written a year apart on the same topic: Google holds both and ranks
neither.

**2. Striking distance.** Queries already inside a position you could move,
with enough impressions to be worth moving, sorted by impressions. This is
usually the largest surprise: the traffic is not somewhere new, it is sitting
at position 6 getting no clicks.

**3. Uncovered.** Query clusters with real impressions whose words appear in
no URL in your sitemap. These are the pages you have not written. Coverage is
judged by sitemap path words, which is a proxy and will produce false
positives on sites whose URLs are opaque ids — read the examples, not the
label.

## Example output

This is the tool run on [`sample/Queries.csv`](sample/Queries.csv), an export
for an invented staff-scheduling company, so you can reproduce it:

```
python3 gsc_gap_audit.py sample/Queries.csv
```

```
38 queries, 45228 impressions, 1196 clicks

== STRIKING DISTANCE == position < 20, impressions >= 5
   4120 imp  pos   6.8  employee scheduling software
   1905 imp  pos  13.1  predictive scheduling laws
   1480 imp  pos   1.1  larkspur scheduling
   1310 imp  pos  17.5  overtime calculator california
   1240 imp  pos   8.9  how to build a rotating shift schedule
   1150 imp  pos  14.3  restaurant staff scheduling app
   1120 imp  pos   5.2  free shift schedule maker
    960 imp  pos  11.2  4 on 3 off schedule template
    884 imp  pos   6.4  shift swap policy template
    870 imp  pos   3.4  2 2 3 schedule explained
    722 imp  pos  12.4  on call rotation template
  ...
```

The full run is in [`example-output.txt`](example-output.txt). The sample is
made up; nothing in it is a real site's data.

Read the list before you get excited about any row. The tool cannot tell a
buyer from a student, a job seeker or somebody's monitoring robot. Neither can
any other tool that claims it can.

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
  someone who will never buy from you. Most exports are full of them. Read
  the queries.
- **No fix is suggested, deliberately.** Deciding whether a cluster deserves a
  new page or a section on an existing one is the judgement the tool cannot
  make, and guessing it is how sites end up cannibalising themselves.

## Licence

MIT — see [LICENSE](LICENSE). The code and this README are MIT. The Mindlyft
name and logo are not; they are excluded from the licence grant.

---

Built by Mindlyft. We get paid for the fixing, not the finding, and the
finding is yours to keep either way: <https://mindlyft.io/r/gh>


---

### Production Services & Toolkits
- **[30-Min Live GTM Teardown (Topmate)](https://topmate.io/harshit_kunwar/2370556)**
- **[GTM Operator Packs ($29–$59, Whop)](https://whop.com/mindlyft-io/products/)** · **[Mindlyft Shop](https://mindlyft.shop)**
- **[GTM Engineering Services](https://mindlyft.io/services)** · **[Pricing](https://mindlyft.io/pricing)**

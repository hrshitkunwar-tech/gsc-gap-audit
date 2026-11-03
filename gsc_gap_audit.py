#!/usr/bin/env python3
"""Find the Search Console queries you already rank for that no page owns.

Reads the CSV that Search Console exports (Performance -> Queries -> Export)
and, optionally, your sitemap. Reports three things, in the order they are
worth acting on:

  1. CANNIBALISATION  two or more of your URLs ranking for the same query.
     Needs the Pages CSV too. This is the only one that is costing you a
     position you already earned.
  2. STRIKING DISTANCE  queries at a position close enough to move, with
     enough impressions to be worth moving. Sorted by impressions.
  3. UNCOVERED  query clusters with real impressions where no URL in your
     sitemap carries the words. These are the pages you have not written.

No credentials, no API, no network unless you pass --sitemap.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import urllib.request
from collections import defaultdict
from dataclasses import dataclass, field

# Words that carry no topical signal, so clustering on them would group
# unrelated queries. Deliberately short: over-stemming merges real clusters.
STOP = {
    "the", "a", "an", "and", "or", "vs", "for", "to", "of", "in", "on", "is",
    "are", "with", "your", "you", "what", "how", "why", "when", "which",
    "does", "do", "can", "best", "better", "it", "my", "we", "i", "at", "by",
    "from", "that", "this", "be", "as", "if", "about", "into", "than",
}


@dataclass
class Row:
    query: str
    clicks: int
    impressions: int
    position: float


@dataclass
class Cluster:
    key: str
    impressions: int = 0
    clicks: int = 0
    rows: list[Row] = field(default_factory=list)

    @property
    def avg_position(self) -> float:
        weighted = sum(r.position * r.impressions for r in self.rows)
        total = sum(r.impressions for r in self.rows) or 1
        return weighted / total

    @property
    def example(self) -> str:
        return max(self.rows, key=lambda r: r.impressions).query


def _num(value: str) -> float:
    """Search Console exports carry commas, percent signs and stray spaces."""
    cleaned = re.sub(r"[^0-9.\-]", "", (value or "").strip())
    return float(cleaned) if cleaned not in ("", "-", ".") else 0.0


def read_queries(path: str) -> list[Row]:
    """Read a Search Console Queries export. Column names vary by locale, so
    match on position after locating the query column rather than on header
    text, which is translated."""
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header is None:
            raise SystemExit(f"{path} is empty")
        rows: list[Row] = []
        for raw in reader:
            if len(raw) < 4 or not raw[0].strip():
                continue
            rows.append(
                Row(
                    query=raw[0].strip(),
                    clicks=int(_num(raw[1])),
                    impressions=int(_num(raw[2])),
                    # A 4-column export is query/clicks/impressions/position;
                    # a 5-column one puts CTR third from the end.
                    position=_num(raw[-1]),
                )
            )
    if not rows:
        raise SystemExit(f"no data rows in {path}")
    return rows


def read_pages(path: str) -> dict[str, list[tuple[str, float]]]:
    """Read a Query+Page export, if one was given, as query -> [(url, pos)]."""
    mapping: dict[str, list[tuple[str, float]]] = defaultdict(list)
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        for raw in reader:
            if len(raw) < 3:
                continue
            query, url = raw[0].strip(), raw[1].strip()
            if query and url.startswith("http"):
                mapping[query].append((url, _num(raw[-1])))
    return mapping


def sitemap_words(url: str) -> set[str]:
    """Every word appearing in a sitemap URL's path, as a coverage proxy."""
    with urllib.request.urlopen(url, timeout=30) as response:  # noqa: S310
        body = response.read().decode("utf-8", "replace")
    words: set[str] = set()
    for loc in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", body):
        for word in re.split(r"[/\-_.]", loc.split("://", 1)[-1].lower()):
            if len(word) > 2:
                words.add(word)
    return words


def tokens(query: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9.]+", query.lower())
            if w not in STOP and len(w) > 2]


def cluster(rows: list[Row]) -> list[Cluster]:
    """Group queries by their two most distinctive tokens. Crude on purpose:
    the point is to surface a theme worth a page, not to be a taxonomy."""
    buckets: dict[str, Cluster] = {}
    for row in rows:
        words = tokens(row.query)
        if not words:
            continue
        key = " ".join(sorted(set(words))[:2])
        bucket = buckets.setdefault(key, Cluster(key))
        bucket.impressions += row.impressions
        bucket.clicks += row.clicks
        bucket.rows.append(row)
    return sorted(buckets.values(), key=lambda c: -c.impressions)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find the queries you rank for that no page owns.")
    parser.add_argument("queries_csv",
                        help="Search Console > Performance > Queries > Export")
    parser.add_argument("--pages-csv",
                        help="a Query+Page export; enables cannibalisation")
    parser.add_argument("--sitemap", help="sitemap URL, for coverage checking")
    parser.add_argument("--max-position", type=float, default=20.0,
                        help="striking-distance cutoff (default 20)")
    parser.add_argument("--min-impressions", type=int, default=5,
                        help="ignore queries below this (default 5)")
    args = parser.parse_args()

    rows = read_queries(args.queries_csv)
    total_impressions = sum(r.impressions for r in rows)
    total_clicks = sum(r.clicks for r in rows)
    print(f"{len(rows)} queries, {total_impressions} impressions, "
          f"{total_clicks} clicks\n")

    if args.pages_csv:
        pages = read_pages(args.pages_csv)
        collisions = {q: urls for q, urls in pages.items() if len(urls) > 1}
        print(f"== CANNIBALISATION ({len(collisions)}) "
              "== two of your URLs on one query")
        if not collisions:
            print("  none found\n")
        for query, urls in sorted(
                collisions.items(),
                key=lambda kv: min(p for _, p in kv[1]))[:20]:
            print(f"  {query}")
            for url, position in sorted(urls, key=lambda u: u[1]):
                print(f"      pos {position:6.1f}  {url}")
        print()

    print(f"== STRIKING DISTANCE == position < {args.max_position:g}, "
          f"impressions >= {args.min_impressions}")
    near = [r for r in rows
            if r.position < args.max_position
            and r.impressions >= args.min_impressions]
    near.sort(key=lambda r: -r.impressions)
    for row in near[:40]:
        print(f"  {row.impressions:5d} imp  pos {row.position:5.1f}  "
              f"{row.query[:72]}")
    recoverable = sum(r.impressions for r in near)
    print(f"  -- {len(near)} queries, {recoverable} impressions in reach\n")

    if args.sitemap:
        covered = sitemap_words(args.sitemap)
        print("== UNCOVERED == clusters whose words appear in no sitemap URL")
        shown = 0
        for group in cluster(rows):
            if shown >= 20 or group.impressions < args.min_impressions:
                break
            if any(word in covered for word in group.key.split()):
                continue
            print(f"  {group.impressions:5d} imp  "
                  f"pos {group.avg_position:5.1f}  "
                  f"{group.key:<24}  e.g. {group.example[:44]}")
            shown += 1
        if shown == 0:
            print("  none: every cluster is named somewhere in the sitemap")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

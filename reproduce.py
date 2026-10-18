#!/usr/bin/env python3
"""Reproduce the GitHub star benchmark snapshot.

Usage:
    python3 reproduce.py
    GITHUB_TOKEN=ghp_xxx python3 reproduce.py   # higher rate limit

Unauthenticated search is limited to 10 requests/minute; the script paces itself.
Writes data/star-counts-<date>.csv. No third-party dependencies.
"""
import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.github.com/search/repositories"
TOKEN = os.environ.get("GITHUB_TOKEN")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", f"star-counts-{dt.date.today().isoformat()}.csv")

QUERIES = [
    ("1+", "stars:>=1"),
    ("10+", "stars:>=10"),
    ("100+", "stars:>=100"),
    ("1,000+", "stars:>=1000"),
    ("5,000+", "stars:>=5000"),
    ("10,000+", "stars:>=10000"),
    ("50,000+", "stars:>=50000"),
    ("100,000+", "stars:>=100000"),
]


def count(query):
    url = API + "?q=" + urllib.parse.quote(query) + "&per_page=1"
    req = urllib.request.Request(url, headers={"User-Agent": "github-star-benchmarks"})
    if TOKEN:
        req.add_header("Authorization", "Bearer " + TOKEN)
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.load(resp)["total_count"], resp.headers.get("X-RateLimit-Remaining")


def main():
    rows = []
    for label, query in QUERIES:
        while True:
            try:
                n, remaining = count(query)
                print(f"{label:>10}  {n:>12,}  (remaining {remaining})", flush=True)
                rows.append((label, n))
                break
            except urllib.error.HTTPError as e:
                if e.code in (403, 429):
                    wait = 60
                    print(f"rate limited, waiting {wait}s", file=sys.stderr, flush=True)
                    time.sleep(wait)
                else:
                    raise
        time.sleep(1)
    base = rows[0][1]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tier", "repositories", "share_of_starred", "one_in"])
        for label, n in rows:
            w.writerow([label, n, f"{100*n/base:.4f}%", round(base/n)])
    print("wrote", OUT)


if __name__ == "__main__":
    main()

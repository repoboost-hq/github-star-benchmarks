# GitHub Star Benchmarks (October 2026)

Reproducible snapshot of how GitHub's star distribution actually looks: how many public
repositories sit above each star threshold, how those counts change by language, and how
age cohorts are represented at the top.

Snapshot date: **2026-10-18**. Source: GitHub REST search API. Raw queries and a reproducer are included.

The full analysis is published at [https://buygithub.com/blog/how-many-github-stars-is-good/](https://buygithub.com/blog/how-many-github-stars-is-good/).

## Headline numbers

| Star tier | Repositories | Share of starred repos | Roughly one in |
|---|---:|---:|---:|
| 1+ | 32,621,661 | 100% | 1 |
| 10+ | 2,908,251 | 8.92% | 11 |
| 100+ | 484,723 | 1.49% | 67 |
| 1,000+ | 65,691 | 0.20% | 497 |
| 5,000+ | 12,744 | 0.039% | 2,560 |
| 10,000+ | 5,650 | 0.017% | 5,774 |
| 50,000+ | 515 | 0.0016% | 63,343 |
| 100,000+ | 132 | 0.0004% | 247,134 |

"Share of starred repos" means public repositories with at least one star. Most GitHub
repositories have no stars at all and are outside this universe.

## What is in this repository

| File | What it is |
|---|---|
| `data/star-counts-2026-10-18.csv` | Repository count above each star threshold |
| `data/language-benchmarks-2026-10-18.csv` | Counts and 100→1,000 / 1,000→10,000 conversion by language |
| `data/age-cohorts-2026-10-18.csv` | Age cohorts among 1,000+ and 100,000+ repositories |
| `data/top-100-repositories-2026-10-18.csv` | The 100 most-starred repositories in the snapshot |
| `chart.svg` | Log-scale chart of the threshold counts |
| `DATA_DICTIONARY.md` | Field definitions and rounding notes |
| `CITATION.cff` | Citation metadata if you use this dataset |
| `reproduce.py` | Re-runs the queries and writes a new snapshot |

## Methodology

- Endpoint: `GET https://api.github.com/search/repositories?q=<query>&per_page=1`
- The value used is the response field `total_count`.
- Threshold queries: `stars:>=N` for N in 1, 10, 100, 1,000, 5,000, 10,000, 50,000, 100,000.
- Language queries: `language:<name> stars:>=N` for Python, JavaScript, TypeScript, Java,
  C++, Go and Rust.
- Age queries: `stars:>=N created:>=YYYY-MM-DD` and `stars:>=N created:<2020-01-01`.
- Top-100 table: `stars:>1000 sort=stars order=desc`, first 100 results.
- Unauthenticated search is limited to 10 requests per minute; `reproduce.py` paces itself
  and supports a `GITHUB_TOKEN` environment variable for a higher limit.

## Caveats

- `total_count` is GitHub's reported, approximate value. It moves as repositories are
  created, deleted, renamed or starred. Comparisons should use a single snapshot date.
- Language queries only cover repositories GitHub classifies with that primary language.
  Unlabelled and multi-language projects are excluded from those rows.
- Conversion rates are ratios between cohorts, not causal effects.
- Counts are repositories, not people, and say nothing about code quality.

## Reproduce

```bash
python3 reproduce.py            # unauthenticated, ~4 minutes due to rate limits
GITHUB_TOKEN=ghp_xxx python3 reproduce.py   # authenticated, faster
```

The script writes `data/star-counts-<snapshot>.csv` next to the existing snapshot.

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: MIT.
Attribute as: "RepoBoost, GitHub Star Benchmarks (October 2026), https://github.com/repoboost-hq/github-star-benchmarks".

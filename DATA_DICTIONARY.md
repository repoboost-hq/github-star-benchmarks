# Data dictionary

Snapshot date: 2026-10-18. All counts are GitHub repositories (not users).

## `data/star-counts-2026-10-18.csv`
| Field | Meaning |
|---|---|
| `tier` | Star threshold: `1+`, `10+`, `100+`, `1,000+`, `5,000+`, `10,000+`, `50,000+`, `100,000+` |
| `repositories` | Number of public repositories at or above the threshold |
| `share_of_starred` | `repositories / repositories with >=1 star`, as a percentage |
| `one_in` | `1 / share_of_starred`, rounded |

## `data/language-benchmarks-2026-10-18.csv`
| Field | Meaning |
|---|---|
| `language` | GitHub primary-language label |
| `repos_ge_100`, `repos_ge_1000`, `repos_ge_10000` | Counts above each threshold for that language |
| `conversion_100_to_1000` | `repos_ge_1000 / repos_ge_100` |
| `conversion_1000_to_10000` | `repos_ge_10000 / repos_ge_1000` |

Only repositories GitHub labels with that primary language are included. Unlabelled
and multi-language repositories are excluded from these rows.

## `data/age-cohorts-2026-10-18.csv`
| Field | Meaning |
|---|---|
| `cohort` | Creation-date bucket |
| `repositories` | Count in that bucket |
| `share_of_1000_plus` | Share of repositories with 1,000+ stars, unless the cohort name says otherwise |

## `data/top-100-repositories-2026-10-18.csv`
The 100 most-starred repositories in the snapshot (`stars:>1000 sort=stars order=desc`).
`rank` 1 is the repository with the most stars. `created_at` is the repository creation date.

## Rounding
Percentages are rounded to 2–4 decimals. `one_in` is rounded to the nearest integer.
Derived shares may not sum to exactly 100% because of rounding.

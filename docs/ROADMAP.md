# Roadmap

## Phase 0 — Design lock

- [x] Product goal
- [x] Architecture
- [x] Source hierarchy
- [x] Explainable scoring
- [x] Failure/staleness policy

## Phase 1 — MVP shell

- [x] Mobile-first static dashboard
- [x] PWA manifest / installability
- [x] Latest JSON loader
- [x] Score cards
- [x] Seven indicator cards
- [x] Big Money section
- [x] Source health section

## Phase 2 — Automated official data

- [x] INDEC inflation adapter
- [x] BCRA reserves adapter
- [x] fiscal structured adapter
- [x] Vaca Muerta production structured adapter
- [x] RIGI official cumulative adapter
- [x] CAMMESA demand/publication adapter with official fallback
- [x] polling/policy news monitor
- [x] capital-flow monitor
- [x] live official-source smoke test on pull requests

Notes:
- Milei approval is not an official government statistic and remains explicitly separated as polling/news data.
- RIGI uses official cumulative snapshots and only advances when a newer official cumulative total can be parsed.
- CAMMESA attempts the public demand API first. If the live MW endpoint is unavailable, it reports the latest official monthly publication period without inventing a number.

Acceptance: one failing news source does not block the dashboard; official data cards expose source/date/status, and PRs verify the required official-source pipeline live.

## Phase 3 — Scheduled updates

- [x] GitHub Actions daily schedule
- [x] snapshot history
- [x] deduplicate news within each run
- [ ] cross-run news identity / event ledger
- [ ] commit only meaningful changes

Target schedule: 06:15 JST (GitHub Actions cron may start later than the nominal time).

## Phase 4 — Web / Quality

- [x] unit tests for scoring and parsing helpers
- [x] fixture tests for fiscal / Vaca Muerta / RIGI / CAMMESA JSON extraction
- [x] offline generation smoke test
- [x] generated JSON validation
- [x] source health alerts in UI
- [x] documentation for manual run
- [x] GitHub Pages deployment workflow
- [ ] confirm Pages is enabled for this private repository/account plan
- [ ] browser/UI smoke test against the deployed URL
- [ ] full data-contract schema validation

## Phase 5 — Optional upgrades

- valuation panel for VIST / CEPU
- portfolio / average purchase price (manual, local-first)
- event timeline for 2027 election
- charts from historical snapshots
- optional LLM summary using the user's own provider/account
- notifications only when a threshold materially changes

## Non-goals for MVP

- brokerage integration
- trading execution
- paid market-data subscription
- multi-user accounts
- black-box AI buy/sell signals
- scraping dozens of unstable sites just to fill every card

# Roadmap

## Phase 0 — Design lock

- [x] Product goal
- [x] Architecture
- [x] Source hierarchy
- [x] Explainable scoring
- [x] Failure/staleness policy

## Phase 1 — MVP shell

- [ ] Mobile-first static dashboard
- [ ] PWA manifest / installability
- [ ] Latest JSON loader
- [ ] Score cards
- [ ] Seven indicator cards
- [ ] Big Money section
- [ ] Source health section

Acceptance: opening `public/index.html` with the seeded data produces a useful iPhone-sized dashboard with no backend.

## Phase 2 — Automated official data

- [ ] INDEC inflation adapter
- [ ] BCRA reserves adapter
- [ ] fiscal adapter
- [ ] Vaca Muerta production adapter
- [ ] RIGI adapter
- [ ] CAMMESA demand adapter
- [ ] polling/news monitor
- [ ] capital-flow monitor

Acceptance: one failing source does not block the rest; each card exposes source/date/status.

## Phase 3 — Scheduled updates

- [ ] GitHub Actions daily schedule
- [ ] snapshot history
- [ ] deduplicate news
- [ ] commit only meaningful data changes

Target schedule: morning Japan time (GitHub Actions uses UTC).

## Phase 4 — Quality

- [ ] unit tests for parsing/scoring
- [ ] schema validation
- [ ] fixture-based parser tests
- [ ] source health alerts in UI
- [ ] documentation for manual run

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

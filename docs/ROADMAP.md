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

Acceptance: `public/` is a useful iPhone-sized dashboard with no backend.

## Phase 2 — Automated official data

- [x] INDEC inflation adapter
- [x] BCRA reserves adapter
- [ ] fiscal structured adapter
- [ ] Vaca Muerta production structured adapter
- [ ] RIGI structured adapter
- [ ] CAMMESA demand structured adapter
- [x] polling/policy news monitor
- [x] capital-flow monitor

Current limitation: fiscal, Vaca Muerta, RIGI and electricity cards still rely on seeded observations plus event/news monitoring until their structured official adapters are hardened.

Acceptance: one failing source does not block the rest; each card exposes source/date/status.

## Phase 3 — Scheduled updates

- [x] GitHub Actions daily schedule
- [x] snapshot history
- [x] deduplicate news within each run
- [ ] cross-run news identity / event ledger
- [ ] commit only meaningful changes

Target schedule: 06:15 JST (GitHub Actions cron may start later than the nominal time).

## Phase 4 — Quality

- [x] unit tests for scoring and BCRA parsing helpers
- [x] offline generation smoke test
- [x] generated JSON validation
- [x] source health alerts in UI
- [x] documentation for manual run
- [ ] full data-contract schema validation
- [ ] fixture-based tests for every external adapter
- [ ] browser/UI smoke test

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

# Architecture

## Product goal

ArgentinaEye answers one question every morning:

> Is the Argentina investment thesis getting stronger or weaker, and what changed since the last update?

It is not a generic finance/news app. It is a personal thesis monitor for Argentina, with VIST and CEPU as the first tracked equities.

## Design philosophy

### 1. Signal before information
The first screen shows changes and implications, not a feed. A user should understand the day in under one minute.

### 2. Primary sources first
Numeric indicators come from official or first-party sources whenever possible. News sources are used for events that cannot be represented by official numeric feeds.

### 3. Explainable scoring
Scores are deterministic and rule-based. Every score contribution can be traced to a metric and threshold.

### 4. Staleness is a first-class state
A stale source is visibly stale. The system never fabricates a current value from an old one.

### 5. Zero-cost MVP
No database, no paid finance API, no LLM API. GitHub Actions performs scheduled collection and commits JSON snapshots. The frontend is static.

### 6. Source adapters are replaceable
Each metric is isolated behind an adapter. If a government endpoint changes, the UI and other metrics remain unaffected.

## System overview

```text
Official APIs / open data / RSS
          |
          v
 scripts/update.py
   |      |      |
 adapters scoring news
   |      |      |
          v
 public/data/latest.json
 public/data/history/YYYY-MM-DD.json
          |
          v
 Static PWA (HTML/CSS/JS)
          |
          v
 iPhone / desktop browser
```

## Components

### Data collector
Python standard library only for MVP.

Responsibilities:
- fetch sources with timeout and identifiable User-Agent
- normalize dates/numbers
- compare against previous snapshot
- assign freshness state
- preserve source URLs and retrieval timestamps
- fail metric-by-metric, not whole-run

### Scoring engine
Consumes normalized metrics and returns:
- Argentina score
- VIST thesis score
- CEPU thesis score
- per-factor contributions

Scores are not buy/sell recommendations. They measure the health of a predefined thesis.

### News monitor
Tracks named capital actors and policy themes using free RSS/search feeds.

Initial entities:
- Peter Thiel / Thiel Macro
- Harold Hamm / Continental Resources
- Chevron
- Mercuria
- Eni
- XRG
- YPF / Argentina LNG

The MVP stores headline, source, published date, URL and matched entities. It does not invent transaction amounts when extraction is uncertain.

### Frontend
A mobile-first static PWA.

Priority order:
1. Today: what changed
2. Argentina / VIST / CEPU scores
3. Seven core indicators
4. Big Money monitor
5. Source health / last update

## Data contract

Every metric follows the same shape:

```json
{
  "id": "inflation_monthly",
  "label": "Inflation",
  "value": 2.1,
  "unit": "% m/m",
  "period": "2026-07",
  "previous": 1.9,
  "change": 0.2,
  "direction": "up",
  "thesis_signal": "negative",
  "status": "fresh",
  "source": {
    "name": "INDEC / Datos Argentina",
    "url": "..."
  },
  "retrieved_at": "..."
}
```

## Failure model

A data failure must result in one of:
- `fresh`: within expected publishing lag
- `stale`: last valid observation exists but is older than expected
- `unavailable`: no valid observation

A failed adapter must never prevent other cards from updating.

## Security and privacy

MVP stores no credentials and no brokerage data. Portfolio tracking, if added later, should default to local/manual values rather than broker credentials.

## Why not Next.js for MVP?

A framework would add build/runtime complexity without improving the core use case. A static PWA is easier to audit, cheaper to run and harder to break. If ArgentinaEye later needs authentication, server-side portfolio data or richer analytics, migration to Next.js can happen behind the same JSON data contract.

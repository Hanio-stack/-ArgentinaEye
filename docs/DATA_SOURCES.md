# Data Sources

## Source hierarchy

1. Official API / official open-data file
2. Official ministry / regulator page
3. Company investor relations / SEC filing
4. Reputable news source for event monitoring
5. Secondary aggregator only as a temporary fallback

ArgentinaEye keeps the source URL with every observation.

## Core indicators

### 1. Milei approval / 2027 reelection risk

**Type:** event / polling monitor

There is no single official polling API. MVP strategy:
- monitor current polling/news headlines via free RSS/search feeds
- store named pollster, field date and percentage only when reliably parseable
- otherwise show the latest relevant headline without fabricating a number
- later add curated pollster adapters if a stable source is identified

Freshness target: 14 days.

### 2. Inflation

Preferred source: Argentina national time-series API backed by official INDEC data.

Endpoint family:
`https://apis.datos.gob.ar/series/api/series`

National monthly CPI variation series:
`145.3_INGNACUAL_DICI_M_38`

Example:
`?ids=145.3_INGNACUAL_DICI_M_38&last=13`

Freshness target: 45 days.

### 3. International reserves

Preferred source: Banco Central de la República Argentina (BCRA) Statistics API v4.

Base:
`https://api.bcra.gob.ar/estadisticas/v4.0/`

Implementation discovers the international-reserves variable from the official variable catalogue instead of assuming a permanent numeric ID.

Freshness target: 5 business days.

### 4. Fiscal balance

Preferred source: Ministerio de Economía / Datos Argentina series and official monthly fiscal releases.

MVP adapter searches the national time-series catalogue for primary/fiscal result series and records the selected series metadata. If no current structured series is available, the metric becomes stale/unavailable rather than using an unverified value.

Freshness target: 45 days.

### 5. Vaca Muerta production

Preferred source: Secretaría de Energía / Datos Argentina.

Dataset:
`Producción de petróleo y gas por pozo (Capítulo IV)`

Useful resources include:
- non-conventional oil/gas well production
- historical oil production by basin/resource type
- production grouped by field and productive formation

The adapter should calculate the latest monthly non-conventional Neuquén/Vaca Muerta production from official CSV resources once the current resource URL is resolved.

Freshness target: 45 days.

### 6. RIGI investment

Preferred source: Ministerio de Economía / official RIGI project pages.

MVP tracks:
- number of approved projects
- announced/approved USD investment when present
- newly approved named projects

RIGI data is low-frequency and event-driven, so a stale-looking unchanged value is not necessarily a failure.

Freshness target: 30 days for source check; value may remain unchanged.

### 7. Electricity market reform / demand

Preferred sources:
- CAMMESA for demand/generation
- Secretaría de Energía for regulation and market reform

CAMMESA has machine-readable demand/generation services; the collector uses those only when the response schema validates successfully.

Metrics:
- latest demand level / comparable change when available
- reform/event headlines (tariff normalization, wholesale market rules, transmission privatization/investment)

Freshness target: 7 days for demand; 30 days for reform events.

## Big Money monitor

Tracked entities and query aliases:

| Entity | Aliases / themes |
|---|---|
| Peter Thiel | Thiel Macro, Vista Energy, VIST, Milei |
| Harold Hamm | Continental Resources, Phoenix Global Resources |
| Chevron | Vaca Muerta, Argentina investment |
| Mercuria | Phoenix, Shell Argentina, Vaca Muerta |
| Eni | Argentina LNG, YPF |
| XRG | Argentina LNG, YPF |

MVP news transport: free RSS/search feeds with deduplication by canonicalized URL/title.

## Equity prices

VIST and CEPU prices are useful context but not one of the seven thesis fundamentals. The MVP may use a free delayed quote source only if it works without secrets and is clearly labeled. The system must continue functioning without stock-price data.

## Source health

Each source records:
- retrieval success/failure
- HTTP status when applicable
- retrieved timestamp
- observation period
- source URL
- freshness state

Never silently substitute an unrelated secondary value for a failed primary source.

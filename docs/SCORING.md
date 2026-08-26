# Scoring

ArgentinaEye scores the health of an investment thesis, not whether a security should be bought or sold.

## Principles

- deterministic rules
- visible factor contributions
- missing data reduces confidence, not necessarily score
- stale data is never treated as fresh confirmation
- score changes should be explainable in one sentence

## Argentina score (0-100)

Initial weights:

- Politics / reelection durability: 20
- Inflation: 15
- International reserves: 15
- Fiscal balance: 15
- Vaca Muerta production: 10
- RIGI / foreign investment: 10
- Electricity reform / demand: 10
- Big Money capital flow: 5

### Interpretation

- 80-100: thesis strongly improving
- 65-79: constructive
- 50-64: mixed / neutral
- 35-49: deteriorating
- 0-34: thesis under major stress

## VIST thesis score (0-100)

- Argentina macro/policy: 25
- Vaca Muerta production trend: 30
- foreign capital / infrastructure commitments: 15
- energy export / pipeline / LNG events: 15
- political durability: 15

The MVP deliberately excludes valuation from the thesis score because a company can have an improving business thesis while its stock is expensive. A later `valuation` panel should remain separate.

## CEPU thesis score (0-100)

- Argentina macro/policy: 20
- electricity market normalization: 25
- electricity demand / generation environment: 20
- RIGI / industrial-mining investment demand: 15
- political durability: 15
- energy-sector capital flow: 5

## Rule examples

### Monthly inflation

Lower is better for the reform thesis.

- <= 1.5%: 100 factor score
- >1.5 to 2.5%: 80
- >2.5 to 4.0%: 60
- >4.0 to 7.0%: 35
- >7.0%: 10

Trend modifier:
- three-month falling trend: +5 (cap 100)
- three-month rising trend: -5 (floor 0)

### International reserves

Use percentage change against 30 days earlier when enough data exists.

- >= +5%: 90
- +1% to +5%: 75
- -1% to +1%: 60
- -5% to -1%: 40
- < -5%: 20

### Vaca Muerta production

Use year-over-year production change.

- >= +20%: 95
- +10 to +20%: 80
- +3 to +10%: 65
- -3 to +3%: 50
- -10 to -3%: 30
- < -10%: 10

### Fiscal balance

Primary surplus is positive for the Milei reform thesis. The normalized fiscal adapter should eventually express the latest result as surplus/deficit relative to GDP or a comparable rolling measure. Until then, a categorical signal may be used with reduced confidence.

### RIGI

Scoring uses event direction rather than raw total alone:
- newly approved credible investment: positive
- cancellation / withdrawal: negative
- unchanged: neutral

### Big Money

This is intentionally low weight. Famous investors are a signal, not proof.

- new committed capital / acquisition / FID: positive
- announced exit / cancellation / divestment due policy risk: negative
- commentary without capital commitment: informational only

## Confidence

Every score includes `confidence` based on fresh weighted inputs.

Example:

```json
{
  "score": 74,
  "confidence": 0.86,
  "label": "constructive"
}
```

If only 50% of weighted inputs are fresh, the UI should show that prominently instead of pretending the score is equally reliable.

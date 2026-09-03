# Scoring

ArgentinaEye scores the **health of an investment thesis**, not whether a security should be bought or sold.

A high score means the surrounding business conditions are supportive. It does **not** mean the stock is cheap. Valuation (price, PER, EV/EBITDA, FCF yield) should be evaluated separately.

## Principles

- deterministic rules
- visible factor contributions
- missing data reduces confidence, not necessarily score
- stale data is never treated as fresh confirmation
- score changes should be explainable in one sentence
- beginner-facing UI should explain what each factor means in plain language

## Interpretation

- 80-100: thesis strongly improving
- 65-79: constructive
- 50-64: mixed / neutral
- 35-49: deteriorating
- 0-34: thesis under major stress

## Argentina score (0-100)

- Politics / reelection durability: 20
- Inflation: 15
- International reserves: 15
- Fiscal balance: 15
- Vaca Muerta production: 10
- RIGI / foreign investment: 10
- Electricity reform / demand: 10
- Big Money capital flow: 5

## VIST thesis score (0-100)

VIST is the **upstream / production** watch: "掘る".

- Argentina macro/policy: 25
- Vaca Muerta production trend: 30
- RIGI / infrastructure commitments: 15
- energy-sector capital flow: 15
- political durability: 15

## PAM thesis score (0-100)

PAM is the **integrated energy** watch: production + power + infrastructure exposure.

- Argentina macro/policy: 25
- Vaca Muerta production trend: 20
- RIGI / large industrial investment: 20
- electricity demand / market environment: 15
- energy-sector capital flow: 10
- political durability: 10

## CEPU thesis score (0-100)

CEPU is the **power generation** watch: "電気を作る".

- Argentina macro/policy: 20
- electricity market / demand environment: 45
- RIGI / industrial-mining investment demand: 15
- political durability: 15
- energy-sector capital flow: 5

## TGS thesis score (0-100)

TGS is the **midstream / infrastructure** watch: "運ぶ・処理する".

- Argentina macro/policy: 20
- Vaca Muerta production trend: 35
- RIGI / infrastructure commitments: 25
- energy-sector capital flow: 10
- political durability: 10

The TGS score intentionally gives more weight to Vaca Muerta volumes and infrastructure than to electricity. The thesis is that increasing gas volumes require transport and processing even when the winning upstream producer changes.

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

The current adapter maps the official production observation into a categorical thesis signal. A future version should score explicit year-over-year production growth with thresholds.

### Fiscal balance

Primary surplus is positive for the Milei reform thesis. The normalized fiscal adapter should eventually express the latest result as surplus/deficit relative to GDP or a comparable rolling measure. Until then, a categorical signal may be used with reduced confidence.

### RIGI

Scoring uses event direction rather than raw total alone:
- newly approved credible investment: positive
- cancellation / withdrawal: negative
- unchanged: neutral

Important: **approval is not the same thing as FID, construction, or operation**. A future project-stage monitor should track these separately.

### Big Money / company news

News is deliberately low weight. Famous investors and headlines are signals, not proof.

- new committed capital / acquisition / FID: positive context
- announced exit / cancellation / divestment due policy risk: negative context
- commentary without capital commitment: informational only

Company news for VIST / PAM / CEPU / TGS is collected for discovery and reading. Headlines alone do not directly override hard-data scores.

## Confidence

Every score includes `confidence` based on available weighted inputs.

Example:

```json
{
  "score": 74,
  "confidence": 0.86,
  "label": "constructive"
}
```

If only 50% of weighted inputs are available, the UI should show that prominently instead of pretending the score is equally reliable.

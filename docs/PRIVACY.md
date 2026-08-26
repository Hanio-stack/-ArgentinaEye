# Privacy boundary

ArgentinaEye is a public repository and a public GitHub Pages dashboard.

## Allowed in the repository

Only public, non-personal information may be committed or published:

- public macroeconomic statistics
- public energy / electricity statistics
- public company and market information
- public news headlines and source links
- derived, non-personal thesis scores
- application source code and documentation

## Never commit or publish

Do not store any user-specific or identifying information in this repository, its generated JSON, issues, logs, or Pages output, including:

- real name, private email, phone number, home/work address, or device identifiers
- brokerage account identifiers or credentials
- API keys, tokens, cookies, passwords, or secrets
- portfolio holdings, share counts, average purchase prices, cost basis, realized/unrealized P&L, or NISA/account details
- private notes, calendar data, or other personal activity

## Future personal portfolio features

If ArgentinaEye later adds user-specific portfolio features, those values must be stored client-side only (for example in browser local storage) and must never be written to GitHub, GitHub Actions artifacts/logs, or the public Pages data files.

Public dashboard data and personal local data must remain separate by design.

## Headline translation

The optional Japanese-translation button may send only the already-public news headline text to an external machine-translation service. No portfolio data, account data, identifiers, private notes, or other user-specific information may be included in translation requests. Cached translations are stored only in the browser local storage and are not committed to GitHub.

## Data-collection rule

Collectors must fetch public sources only. Missing data must remain missing/stale rather than being filled from private user context.

# Running ArgentinaEye

## Local preview

```bash
python -m http.server 8080 -d public
```

Open `http://localhost:8080`.

## Data refresh

```bash
python scripts/update.py
```

Offline smoke test:

```bash
python scripts/update.py --offline
```

Tests:

```bash
python -m unittest discover -s tests -v
```

## Daily automation

`.github/workflows/update-data.yml` runs at about 06:15 JST each morning and commits changed JSON snapshots. It uses no paid API and no app secrets.

## Web publishing

`.github/workflows/pages.yml` deploys the `public/` directory to GitHub Pages after a push to `main`.

Expected project URL after Pages is enabled:

`https://hanio-stack.github.io/-ArgentinaEye/`

GitHub Pages must be enabled for the repository/account. The repository is private, so private-repository Pages support depends on the GitHub plan. The deploy workflow deliberately does **not** change repository visibility or account settings automatically.

If Pages requires one-time setup, open the repository in GitHub, go to **Settings → Pages**, and select **GitHub Actions** as the publishing source. Do not make the repository public just to publish without an explicit decision.

## iPhone use

After the Pages URL works:

1. Open the URL in Safari.
2. Tap **Share**.
3. Tap **Add to Home Screen**.
4. Launch ArgentinaEye from the new home-screen icon.

The site is a PWA and retains a cached last-known view when possible.

## Source verification

`.github/workflows/source-smoke.yml` runs against live official sources on pull requests. Required sources are INDEC, BCRA, Fiscal, Vaca Muerta, RIGI and CAMMESA. News/RSS failures remain non-blocking because numerical official sources are the higher-priority contract.

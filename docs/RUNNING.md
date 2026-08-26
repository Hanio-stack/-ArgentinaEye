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

`.github/workflows/update-data.yml` runs at 06:15 JST each morning and commits changed JSON snapshots. It uses no secrets and no paid API.

## Hosting

The entire app lives under `public/` and is a static PWA. It can be hosted by GitHub Pages, Cloudflare Pages, Netlify, Vercel static hosting, or any simple web server.

For a private repository, GitHub Pages availability depends on the GitHub plan/settings. Hosting is intentionally separate from data collection so the monitor still works locally if Pages is unavailable.

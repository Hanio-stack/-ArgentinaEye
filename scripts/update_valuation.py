#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "public" / "data" / "valuation.json"
TIMEOUT = 20
UA = "ArgentinaEye/0.5 (+learning dashboard; daily valuation refresh)"
TICKERS = ("vist", "pam", "cepu", "tgs")

URLS = {k: f"https://stockanalysis.com/stocks/{k}/statistics/" for k in TICKERS}


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.parts.append(text)


def page_text(raw: str) -> str:
    p = TextParser()
    p.feed(raw)
    return re.sub(r"\s+", " ", html.unescape(" ".join(p.parts))).strip()


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
        return page_text(res.read().decode("utf-8", "replace"))


def num(text: str, pattern: str, default=None):
    m = re.search(pattern, text, re.I)
    if not m:
        return default
    try:
        return float(m.group(1).replace(",", ""))
    except Exception:
        return default


def money_b(text: str, label: str, default=None):
    m = re.search(rf"{label}\s*\|?\s*\$?\s*([0-9.,]+)\s*([BM])\b", text, re.I)
    if not m:
        return default
    value = float(m.group(1).replace(",", ""))
    return round(value if m.group(2).upper() == "B" else value / 1000, 4)


def parse_stock(text: str, old: dict, url: str) -> dict:
    price = num(text, r"Real-Time Price\s*·\s*USD\s+([0-9.,]+)", old.get("price"))
    market = money_b(text, r"Market Cap", old.get("market_cap_b"))
    ev = money_b(text, r"Enterprise Value", old.get("enterprise_value_b"))
    pe = num(text, r"\bPE Ratio\s*\|?\s*([0-9.]+)", old.get("pe"))
    fpe = num(text, r"Forward PE\s*\|?\s*([0-9.]+)", old.get("forward_pe"))
    ev_ebitda = num(text, r"EV\s*/\s*EBITDA\s*\|?\s*([0-9.]+)", old.get("ev_ebitda"))
    p_fcf = num(text, r"P/FCF Ratio\s*\|?\s*([0-9.]+)", old.get("p_fcf"))
    debt_ebitda = num(text, r"Debt\s*/\s*EBITDA\s*\|?\s*([0-9.]+)", old.get("debt_ebitda"))
    ch52 = num(text, r"52-Week Price Change\s*\|?\s*([+\-]?[0-9.]+)%", old.get("change_52w"))
    date_match = re.search(r"(?:At close:|Market closed|Market open)\s*(?:on\s*)?([A-Z][a-z]{2}\s+\d{1,2},\s+20\d{2})", text)
    as_of = old.get("as_of")
    if date_match:
        try:
            as_of = datetime.strptime(date_match.group(1), "%b %d, %Y").strftime("%Y-%m-%d")
        except Exception:
            pass
    return {
        **old,
        "price": price,
        "market_cap_b": market,
        "enterprise_value_b": ev,
        "pe": pe,
        "forward_pe": fpe,
        "ev_ebitda": ev_ebitda,
        "p_fcf": p_fcf,
        "debt_ebitda": debt_ebitda,
        "change_52w": ch52,
        "status": "fresh",
        "as_of": as_of or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "source_url": url,
    }


def scenario_prices(stock: dict, scenarios: dict) -> dict:
    price = stock.get("price")
    market = stock.get("market_cap_b")
    if not price or not market:
        return scenarios
    adr_equiv_m = market * 1000 / price
    out = {"year": scenarios.get("year", 2028)}
    for name in ("bear", "base", "bull"):
        s = dict(scenarios.get(name, {}))
        equity_b = s.get("ebitda_b", 0) * s.get("multiple", 0) - s.get("net_debt_b", 0)
        target = equity_b * 1000 / adr_equiv_m if adr_equiv_m > 0 else None
        s["target_price"] = round(target, 2) if target is not None else None
        s["upside_pct"] = round((target / price - 1) * 100, 1) if target and price else None
        out[name] = s
    return out


def main() -> int:
    data = json.loads(TARGET.read_text(encoding="utf-8"))
    health = []
    for key in TICKERS:
        old = data["stocks"][key]
        try:
            text = fetch_text(URLS[key])
            data["stocks"][key] = parse_stock(text, old, URLS[key])
            health.append({"ticker": key.upper(), "ok": True})
        except Exception as exc:
            old["status"] = "stale"
            old["error"] = str(exc)[:120]
            health.append({"ticker": key.upper(), "ok": False, "note": str(exc)[:90]})
    data["computed_scenarios"] = {
        key: scenario_prices(data["stocks"][key], data["scenarios"][key]) for key in TICKERS
    }
    data["health"] = health
    data["generated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

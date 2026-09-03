#!/usr/bin/env python3
from __future__ import annotations

import argparse
import email.utils
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "public" / "data" / "latest.json"
UA = "ArgentinaEye/0.3 (+personal research dashboard; GitHub Actions)"
TIMEOUT = 18

STOCK_WATCH = {
    "vist": {
        "label": "VIST",
        "role": "掘る｜Vaca Muertaの原油・ガス生産",
        "beginner": "Vaca Muertaから石油・ガスを低コストで生産して売る会社。4社の中では『資源を掘る』成長に最も直接的に賭ける銘柄です。",
        "helps": "生産量の増加、輸出インフラ整備、原油価格の上昇、RIGI投資の進展",
        "hurts": "原油安、生産計画の未達、設備投資や借金の増えすぎ、政策の逆戻り",
        "query": '"Vista Energy" Argentina Vaca Muerta when:30d',
    },
    "pam": {
        "label": "PAM",
        "role": "総合｜掘る＋発電＋インフラ",
        "beginner": "Pampa Energía。石油・ガス生産、発電、送電・ガス輸送会社への出資などを持つ総合エネルギー企業。『アルゼンチンのエネルギー成長を広く持つ』イメージです。",
        "helps": "Vaca Muerta増産、RIGI大型投資、電力需要増、エネルギー市場の正常化",
        "hurts": "大型投資の失敗、借金増加、電力・ガス規制の逆戻り、国内景気悪化",
        "query": '"Pampa Energia" Argentina Vaca Muerta when:30d',
    },
    "cepu": {
        "label": "CEPU",
        "role": "作る｜発電・電力市場",
        "beginner": "Central Puerto。主に電気を作って売る会社。アルゼンチンの電力料金・市場制度が正常化するほど事業環境が改善しやすい銘柄です。",
        "helps": "電力料金の正常化、需要増、発電設備の稼働改善、産業投資の増加",
        "hurts": "価格統制、CAMMESAの支払い問題、規制変更、電力需要の低迷",
        "query": '"Central Puerto" Argentina electricity when:30d',
    },
    "tgs": {
        "label": "TGS",
        "role": "運ぶ｜ガス輸送・処理インフラ",
        "beginner": "Transportadora de Gas del Sur。天然ガスをパイプラインで運び、処理する会社。『誰が掘って勝つか』より、Vaca Muerta全体の流通量が増えることに賭ける銘柄です。",
        "helps": "Vaca Muertaのガス増産、パイプライン増強、NGL・輸出設備の稼働",
        "hurts": "輸送料金規制、インフラ計画の遅延、ガス生産停滞、政策の逆戻り",
        "query": '"Transportadora de Gas del Sur" Argentina Vaca Muerta when:30d',
    },
}


def metric_map(data):
    return {m["id"]: m for m in data.get("metrics", [])}


def categorical_factor(metric, positive=75, neutral=55, negative=30):
    if not metric:
        return None
    if metric.get("status") == "unavailable" and metric.get("value") is None and not metric.get("latest_event"):
        return None
    return {"positive": positive, "neutral": neutral, "negative": negative}.get(metric.get("thesis_signal"), neutral)


def weighted_score(parts):
    available = [(score, weight) for score, weight in parts if score is not None]
    if not available:
        return 50.0, 0.0
    total_weight = sum(weight for _, weight in parts)
    live_weight = sum(weight for _, weight in available)
    score = sum(float(score) * weight for score, weight in available) / live_weight
    return round(score, 1), round(live_weight / total_weight, 2)


def build_extra_scores(data):
    metrics = metric_map(data)
    argentina = data.get("scores", {}).get("argentina", {}).get("score")
    politics = categorical_factor(metrics.get("milei_approval", {}))
    vaca = categorical_factor(metrics.get("vaca_muerta_oil", {}), 90, 55, 20)
    rigi = categorical_factor(metrics.get("rigi_investment", {}), 85, 55, 25)
    electricity = categorical_factor(metrics.get("electricity", {}), 75, 55, 30)
    capital = 70 if data.get("news") else 55

    pam, pam_conf = weighted_score([
        (argentina, 25),
        (vaca, 20),
        (rigi, 20),
        (electricity, 15),
        (capital, 10),
        (politics, 10),
    ])
    tgs, tgs_conf = weighted_score([
        (argentina, 20),
        (vaca, 35),
        (rigi, 25),
        (capital, 10),
        (politics, 10),
    ])
    return {
        "pam": {"label": "PAM", "score": pam, "confidence": pam_conf},
        "tgs": {"label": "TGS", "score": tgs, "confidence": tgs_conf},
    }


def google_news_rss(query, limit=3):
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote_plus(query)}&hl=en&gl=US&ceid=US:en"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    root = ET.fromstring(urllib.request.urlopen(req, timeout=TIMEOUT).read())
    items = []
    for item in root.findall("./channel/item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        raw_date = (item.findtext("pubDate") or "").strip()
        source_node = item.find("source")
        source = (source_node.text or "").strip() if source_node is not None else "Google News"
        published = raw_date
        if raw_date:
            try:
                published = email.utils.parsedate_to_datetime(raw_date).strftime("%Y-%m-%d")
            except Exception:
                pass
        items.append({"title": title, "url": link, "published": published, "source": source})
    return items


def collect_company_news():
    out = []
    health = []
    for key, stock in STOCK_WATCH.items():
        try:
            items = google_news_rss(stock["query"])
            health.append({"name": f"Stock news: {stock['label']}", "ok": True, "note": f"{len(items)} items"})
            for item in items:
                item["topic"] = "company_news"
                item["entities"] = [stock["label"]]
                out.append(item)
        except Exception as exc:
            health.append({"name": f"Stock news: {stock['label']}", "ok": False, "note": str(exc)[:90]})
    return out, health


def merge_news(existing, additions, limit=24):
    seen = set()
    merged = []
    for item in list(additions) + list(existing):
        key = re.sub(r"\W+", " ", item.get("title", "").lower()).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        merged.append(item)
    merged.sort(key=lambda item: item.get("published", ""), reverse=True)
    return merged[:limit]


def augment(data, offline=False):
    scores = data.setdefault("scores", {})
    scores.update(build_extra_scores(data))
    data["stock_watch"] = [
        {k: v for k, v in stock.items() if k != "query"}
        for stock in STOCK_WATCH.values()
    ]

    if not offline:
        company_news, health = collect_company_news()
        data["news"] = merge_news(data.get("news", []), company_news)
        data.setdefault("source_health", []).extend(health)

    data["version"] = max(int(data.get("version", 0)), 3)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    if not LATEST.exists():
        raise SystemExit(f"missing {LATEST}")
    data = json.loads(LATEST.read_text(encoding="utf-8"))
    augment(data, offline=args.offline)
    LATEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"augmented {LATEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

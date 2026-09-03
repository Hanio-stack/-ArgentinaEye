import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "augment_stocks.py"
spec = importlib.util.spec_from_file_location("augment_stocks", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class StockMonitorTests(unittest.TestCase):
    def base_data(self):
        return {
            "scores": {"argentina": {"score": 72, "confidence": 1}},
            "metrics": [
                {"id": "milei_approval", "status": "fresh", "thesis_signal": "neutral", "value": 40},
                {"id": "vaca_muerta_oil", "status": "fresh", "thesis_signal": "positive", "value": 650},
                {"id": "rigi_investment", "status": "fresh", "thesis_signal": "positive", "value": 30},
                {"id": "electricity", "status": "fresh", "thesis_signal": "neutral", "value": 15000},
            ],
            "news": [{"title": "Capital investment", "url": "https://example.com", "published": "2026-09-01"}],
        }

    def test_adds_pam_and_tgs_scores(self):
        data = mod.augment(self.base_data(), offline=True)
        self.assertIn("pam", data["scores"])
        self.assertIn("tgs", data["scores"])
        self.assertGreater(data["scores"]["pam"]["score"], 60)
        self.assertGreater(data["scores"]["tgs"]["score"], 60)

    def test_stock_watch_has_beginner_notes(self):
        data = mod.augment(self.base_data(), offline=True)
        labels = {item["label"] for item in data["stock_watch"]}
        self.assertEqual(labels, {"VIST", "PAM", "CEPU", "TGS"})
        for item in data["stock_watch"]:
            self.assertTrue(item["role"])
            self.assertTrue(item["beginner"])
            self.assertTrue(item["helps"])
            self.assertTrue(item["hurts"])

    def test_merge_news_deduplicates_titles(self):
        existing = [{"title": "Same Story", "published": "2026-09-01"}]
        additions = [{"title": "Same Story", "published": "2026-09-02"}, {"title": "New Story", "published": "2026-09-03"}]
        merged = mod.merge_news(existing, additions)
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["title"], "New Story")


if __name__ == "__main__":
    unittest.main()

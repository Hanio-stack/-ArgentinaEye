import importlib.util,sys,unittest
from pathlib import Path

MODULE_PATH=Path(__file__).resolve().parents[1]/"scripts"/"update_valuation.py"
spec=importlib.util.spec_from_file_location("update_valuation",MODULE_PATH)
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)

class ValuationTests(unittest.TestCase):
 def test_parse_stock(self):
  text="NYSE: VIST · Real-Time Price · USD 77.03 Market Cap | 8.27B Enterprise Value | 11.71B PE Ratio | 10.41 Forward PE | 8.44 P/FCF Ratio | 28.70 EV / EBITDA | 5.62 Debt / EBITDA | 1.74 52-Week Price Change | +97.61%"
  out=mod.parse_stock(text,{"label":"VIST","as_of":"2026-09-02"},"x")
  self.assertEqual(out["price"],77.03);self.assertEqual(out["market_cap_b"],8.27);self.assertEqual(out["ev_ebitda"],5.62);self.assertEqual(out["change_52w"],97.61)
 def test_scenario_price(self):
  stock={"price":77.03,"market_cap_b":8.27}
  raw={"year":2028,"bear":{"ebitda_b":2.4,"multiple":4,"net_debt_b":2},"base":{"ebitda_b":2.8,"multiple":5,"net_debt_b":1.5},"bull":{"ebitda_b":3.2,"multiple":6,"net_debt_b":1}}
  out=mod.scenario_prices(stock,raw)
  self.assertGreater(out["base"]["target_price"],100)
  self.assertLess(out["bear"]["target_price"],stock["price"])
  self.assertGreater(out["bull"]["upside_pct"],100)

if __name__=="__main__":unittest.main()

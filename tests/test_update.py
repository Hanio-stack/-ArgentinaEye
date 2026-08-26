import importlib.util,sys,unittest
from pathlib import Path
MODULE_PATH=Path(__file__).resolve().parents[1]/"scripts"/"update.py";spec=importlib.util.spec_from_file_location("update",MODULE_PATH);update=importlib.util.module_from_spec(spec);sys.modules[spec.name]=update;spec.loader.exec_module(update)
class ScoringTests(unittest.TestCase):
 def test_inflation_good(self):self.assertEqual(update.inflation_factor({"value":1.4,"series":[2.0,1.7,1.4]}),100)
 def test_inflation_rising_modifier(self):self.assertEqual(update.inflation_factor({"value":3.0,"series":[2.4,2.7,3.0]}),55)
 def test_reserves(self):self.assertEqual(update.reserves_factor({"value":50,"change":5.2}),90);self.assertEqual(update.reserves_factor({"value":50,"change":-6}),20)
 def test_weighted_score_confidence(self):score,confidence=update.weighted_score([(80,50),(None,50)]);self.assertEqual(score,80);self.assertEqual(confidence,.5)
 def test_bcra_catalog_discovery(self):self.assertEqual(update._bcra_reserve_catalog_item({"results":[{"idVariable":7,"descripcion":"Base monetaria"},{"idVariable":1,"descripcion":"Reservas internacionales"}]})["idVariable"],1)
 def test_bcra_point_shapes(self):self.assertEqual(update._extract_bcra_points({"results":[{"idVariable":1,"detalle":[{"fecha":"2026-08-01","valor":49000},{"fecha":"2026-08-02","valor":50000}]}]})[-1],("2026-08-02",50000.0))
if __name__=="__main__":unittest.main()

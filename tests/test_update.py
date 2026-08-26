import importlib.util,sys,unittest
from datetime import datetime,timezone
from pathlib import Path
MODULE_PATH=Path(__file__).resolve().parents[1]/"scripts"/"update.py";spec=importlib.util.spec_from_file_location("update",MODULE_PATH);update=importlib.util.module_from_spec(spec);sys.modules[spec.name]=update;spec.loader.exec_module(update)

class ScoringTests(unittest.TestCase):
 def test_inflation_good(self):self.assertEqual(update.inflation_factor({"value":1.4,"series":[2.0,1.7,1.4]}),100)
 def test_inflation_rising_modifier(self):self.assertEqual(update.inflation_factor({"value":3.0,"series":[2.4,2.7,3.0]}),55)
 def test_reserves(self):self.assertEqual(update.reserves_factor({"value":50,"change":5.2}),90);self.assertEqual(update.reserves_factor({"value":50,"change":-6}),20)
 def test_weighted_score_confidence(self):score,confidence=update.weighted_score([(80,50),(None,50)]);self.assertEqual(score,80);self.assertEqual(confidence,.5)
 def test_bcra_catalog_discovery(self):self.assertEqual(update._bcra_reserve_catalog_item({"results":[{"idVariable":7,"descripcion":"Base monetaria"},{"idVariable":1,"descripcion":"Reservas internacionales"}]})["idVariable"],1)
 def test_bcra_point_shapes(self):self.assertEqual(update._extract_bcra_points({"results":[{"idVariable":1,"detalle":[{"fecha":"2026-08-01","valor":49000},{"fecha":"2026-08-02","valor":50000}]}]})[-1],("2026-08-02",50000.0))

class OfficialParserTests(unittest.TestCase):
 def test_spanish_numbers(self):
  self.assertEqual(update.spanish_number("2.960.333"),2960333.0);self.assertEqual(update.spanish_number("643,1"),643.1);self.assertEqual(update.spanish_number("29.892"),29892.0)
 def test_fiscal_parser(self):
  raw="<html><body><div>+ $ 2.960.333 millones</div><div>Resultado primario</div><div>Julio</div></body></html>";m=update.parse_fiscal_html(raw,datetime(2026,8,26,tzinfo=timezone.utc));self.assertEqual(m["value"],2.96);self.assertEqual(m["period"],"2026-07");self.assertEqual(m["thesis_signal"],"positive")
 def test_vaca_muerta_parser(self):
  raw="<html><body>La producción de Vaca Muerta alcanzó 643,1 mil barriles diarios, con un incremento interanual de 26,4% durante julio.</body></html>";m=update.parse_vaca_html(raw,now=datetime(2026,8,26,tzinfo=timezone.utc));self.assertEqual(m["value"],643.1);self.assertEqual(m["change"],26.4);self.assertEqual(m["period"],"2026-07")
 def test_rigi_parser(self):
  raw="<html><body>Proyectos aprobados por resolución 16 proyectos US$ 29.892 millones de inversión. 11 de junio de 2026.</body></html>";m=update.parse_rigi_html(raw,now=datetime(2026,8,26,tzinfo=timezone.utc));self.assertEqual(m["project_count"],16);self.assertEqual(m["value"],29.892);self.assertEqual(m["period"],"2026-06")
 def test_recursive_demand_candidate(self):
  vals=update._demand_candidates({"resultados":[{"temperatura":23.1,"demanda":12345.6},{"potenciaMW":13001}]});self.assertEqual(vals,[12345.6,13001.0])

if __name__=="__main__":unittest.main()

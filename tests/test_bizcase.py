import unittest

from bizcase.load import load_case
from bizcase.market import market_sizing
from bizcase.compete import compete_matrix, compete_alerts
from bizcase.unit_econ import unit_economics
from bizcase.scenario import run_scenarios
from bizcase.judge import judge_pack


class TestBizCase(unittest.TestCase):
    def setUp(self):
        self.cfg = load_case()

    def test_market_funnel_nested(self):
        m = market_sizing(self.cfg)
        self.assertGreater(m["tam"], m["sam"])
        self.assertGreater(m["sam"], m["som_geo"])
        self.assertGreater(m["som_geo"], m["som"])
        self.assertGreater(m["som"], 0)

    def test_competitors_include_brand(self):
        comps = compete_matrix(self.cfg)
        names = [c["name"] for c in comps]
        self.assertIn(self.cfg["meta"]["brand"], names)
        self.assertGreaterEqual(len(comps), 3)

    def test_alerts_not_empty_for_demo(self):
        alerts = compete_alerts(self.cfg)
        self.assertTrue(any(a["level"] in ("P1", "P2") for a in alerts))

    def test_unit_economics_positive_contribution(self):
        u = unit_economics(self.cfg)
        self.assertGreater(u["contribution"], 0)
        self.assertIsNotNone(u["payback_months"])
        self.assertTrue(u["healthy"])

    def test_bad_margin_unhealthy(self):
        u = unit_economics(self.cfg, gross_margin=0.05, cac=80, aov=40)
        self.assertFalse(u["healthy"])

    def test_scenarios_three(self):
        sc = run_scenarios(self.cfg)
        self.assertEqual(len(sc), 3)
        labels = [s["label"] for s in sc]
        self.assertEqual(labels, ["悲观", "基准", "乐观"])
        # upside SOM should exceed downside
        down = next(s for s in sc if s["key"] == "downside")
        up = next(s for s in sc if s["key"] == "upside")
        self.assertGreater(up["som"], down["som"])

    def test_judge_pack(self):
        qs = judge_pack(self.cfg)
        self.assertGreaterEqual(len(qs), 5)
        self.assertTrue(all("q" in x and "a" in x and x["a"] for x in qs))


if __name__ == "__main__":
    unittest.main()

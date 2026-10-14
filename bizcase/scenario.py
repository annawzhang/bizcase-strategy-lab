"""情景推演：乐观 / 基准 / 悲观。"""

from __future__ import annotations

from .market import market_sizing
from .unit_econ import unit_economics


def run_scenarios(cfg: dict) -> list[dict]:
    base_m = market_sizing(cfg)
    out = []
    for key in ("downside", "base", "upside"):
        sc = cfg["scenarios"][key]
        # 调整市场 SOM：用情景份额替换
        mcfg = {
            **cfg,
            "market": {**cfg["market"], "target_share_y3": sc["share_y3"]},
            "unit": {
                **cfg["unit"],
                "aov": cfg["unit"]["aov"] * sc["demand_mult"],
                "cac": cfg["unit"]["cac"] * sc["cac_mult"],
                "gross_margin": cfg["unit"]["gross_margin"] + sc["margin_delta"],
                "orders_per_month": cfg["unit"]["orders_per_month"] * (0.9 + 0.1 * sc["demand_mult"]),
            },
        }
        # clamp margin
        mcfg["unit"]["gross_margin"] = max(0.05, min(0.5, mcfg["unit"]["gross_margin"]))
        sizing = market_sizing(mcfg)
        ue = unit_economics(mcfg)
        out.append({
            "key": key,
            "label": sc["label"],
            "params": sc,
            "som": sizing["som"],
            "som_vs_base": sizing["som"] / base_m["som"] if base_m["som"] else None,
            "unit": ue,
        })
    return out

#!/usr/bin/env python3
"""生成苏州零售消费虚构商赛报告 → docs/index.html。"""

from pathlib import Path

from bizcase.load import load_case
from bizcase import (
    market_sizing,
    compete_matrix,
    compete_alerts,
    unit_economics,
    run_scenarios,
    judge_pack,
)
from bizcase.report import render

ROOT = Path(__file__).resolve().parent


def main() -> None:
    cfg = load_case()
    market = market_sizing(cfg)
    comps = compete_matrix(cfg)
    alerts = compete_alerts(cfg)
    unit = unit_economics(cfg)
    scenarios = run_scenarios(cfg)
    judges = judge_pack(cfg)

    html = render(cfg, market, comps, alerts, unit, scenarios, judges)
    out = ROOT / "docs" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")

    print(cfg["meta"]["title"])
    print(f"TAM={market['tam']/1e8:.1f}亿  SAM={market['sam']/1e8:.2f}亿  SOM={market['som']/1e8:.2f}亿")
    print(f"UE healthy={unit['healthy']} payback={unit['payback_months']}")
    print(f"alerts={len(alerts)} scenarios={len(scenarios)} judge_q={len(judges)}")
    print(f"报告 → {out}")


if __name__ == "__main__":
    main()

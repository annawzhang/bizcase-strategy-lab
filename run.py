#!/usr/bin/env python3
"""生成苏州零售消费虚构商赛报告 → docs/index.html。"""

from pathlib import Path

from bizcase.load import load_case
from bizcase import (
    competition_brief,
    market_sizing,
    compete_matrix,
    compete_alerts,
    unit_economics,
    run_scenarios,
    porter_forces,
    monitor_board,
)
from bizcase.report import render

ROOT = Path(__file__).resolve().parent


def main() -> None:
    cfg = load_case()
    brief = competition_brief(cfg)
    market = market_sizing(cfg)
    comps = compete_matrix(cfg)
    alerts = compete_alerts(cfg)
    unit = unit_economics(cfg)
    scenarios = run_scenarios(cfg)
    porter = porter_forces(cfg)
    monitor = monitor_board(cfg)

    html = render(cfg, market, comps, alerts, unit, scenarios, porter, monitor, brief)
    out = ROOT / "docs" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")

    print(cfg["meta"]["title"])
    print(f"赛道={brief['track']} 奖项={brief['award']} 真实案例={brief['real_case']}")
    print(f"TAM={market['tam']/1e8:.1f}亿  SAM={market['sam']/1e8:.2f}亿  SOM={market['som']/1e8:.2f}亿")
    print(f"porter avg={porter['avg_intensity']:.1f}  monitor 红/黄/绿={monitor['summary']['红']}/{monitor['summary']['黄']}/{monitor['summary']['绿']}")
    print(f"报告 → {out}")


if __name__ == "__main__":
    main()

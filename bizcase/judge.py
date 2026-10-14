"""评委追问包：用当前假设生成回答要点（规则模板）。"""

from __future__ import annotations

from .market import market_sizing
from .unit_econ import unit_economics
from .compete import compete_alerts
from .scenario import run_scenarios


def _yi(n: float) -> str:
    return f"{n / 1e8:.2f} 亿"


def _pay(m: float | None) -> str:
    return "∞" if m is None else f"{m:.1f}月"


def _scenario_answer(sc: list[dict]) -> str:
    parts = [f"{x['label']} SOM {_yi(x['som'])}、回本 {_pay(x['unit']['payback_months'])}" for x in sc]
    return (
        "三情景已跑：悲观需求×0.75、CAC×1.25、毛利下调。"
        + "；".join(parts)
        + "。若悲观回本超上限，应收缩地理而非加大补贴。"
    )


def judge_pack(cfg: dict) -> list[dict]:
    m = market_sizing(cfg)
    u = unit_economics(cfg)
    alerts = compete_alerts(cfg)
    sc = run_scenarios(cfg)
    brand = cfg["meta"]["brand"]
    pay = "无法回本" if u["payback_months"] is None else f"{u['payback_months']:.1f} 个月"

    qs = [
        {
            "q": "市场规模是怎么算的？会不会拍脑袋？",
            "a": (
                f"路径透明：人口→家庭→年支出→可触达占比→地理可服务→三年份额。"
                f"当前 TAM {_yi(m['tam'])}，SAM {_yi(m['sam'])}，SOM {_yi(m['som'])}。"
                f"每一层假设都在 config 里，评委改渗透率可即时重算。"
            ),
        },
        {
            "q": "和现有玩家比，差异化是什么？",
            "a": (
                f"{brand} 定位新鲜度与私域复购，不和「城南大卖场」拼绝对低价。"
                f"今日告警 {len(alerts)} 条，优先处理 P1（份额/价格），避免全面促销战。"
            ),
        },
        {
            "q": "单位经济能不能打平？",
            "a": (
                f"客单 {u['aov']:.0f} 元、毛利 {u['gross_margin']:.0%}、履约 {u['fulfill_cost']:.1f} 元、"
                f"单均贡献 {u['contribution']:.1f} 元、CAC {u['cac']:.0f} 元，回本约 {pay}。"
                f"{'健康' if u['healthy'] else '未达健康线'}（回本上限 {u['cap']} 个月）。"
            ),
        },
        {
            "q": "悲观情景下还成立吗？",
            "a": _scenario_answer(sc),
        },
        {
            "q": "为什么选苏州而不是先做全国？",
            "a": (
                "先吃透可服务地理（演示设为人口 28% 核心区），把履约半径和复购跑通，"
                "再用 SOM 份额目标检验密度，而不是全国铺开烧 CAC。"
            ),
        },
        {
            "q": "预算加 20% 应该投在哪？",
            "a": (
                "优先投能拉高月复购与贡献的动作（会员、履约时效），"
                "而不是无差别补贴；若竞品价格战告警为 P1，只跟核心 SKU。"
            ),
        },
    ]
    return qs

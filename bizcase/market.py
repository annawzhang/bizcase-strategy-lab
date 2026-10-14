"""市场测算：TAM / SAM / SOM（假设可审计）。"""

from __future__ import annotations


def market_sizing(cfg: dict) -> dict:
    m = cfg["market"]
    hh = m["population"] / m["household_size"]
    annual_spend = hh * m["monthly_spend_per_hh"] * m["months"]
    tam = annual_spend  # 苏州家庭食品日用总支出（演示口径）
    sam = tam * m["addressable_share"] * m["segment_share"]  # 社区优选可触达
    som_geo = sam * m["serviceable_geo"]  # 我方可服务地理
    som = som_geo * m["target_share_y3"]  # 三年目标份额

    return {
        "households": hh,
        "tam": tam,
        "sam": sam,
        "som_geo": som_geo,
        "som": som,
        "assumptions": {
            "population": m["population"],
            "household_size": m["household_size"],
            "monthly_spend_per_hh": m["monthly_spend_per_hh"],
            "addressable_share": m["addressable_share"],
            "segment_share": m["segment_share"],
            "serviceable_geo": m["serviceable_geo"],
            "target_share_y3": m["target_share_y3"],
        },
        "narrative": (
            f"苏州约 {hh/1e6:.2f} 百万家庭 × 月支出 {m['monthly_spend_per_hh']:.0f} 元 "
            f"→ TAM {tam/1e8:.1f} 亿元/年；"
            f"可触达社区优选 SAM {sam/1e8:.2f} 亿；"
            f"可服务区域 × 三年份额 {m['target_share_y3']:.0%} → SOM {som/1e8:.2f} 亿。"
        ),
    }

"""竞品雷达与规则告警。"""

from __future__ import annotations


def compete_matrix(cfg: dict) -> list[dict]:
    return [dict(c) for c in cfg["competitors"]]


def compete_alerts(cfg: dict) -> list[dict]:
    rules = cfg["compete_rules"]
    comps = compete_matrix(cfg)
    us = next(c for c in comps if c["name"] == cfg["meta"]["brand"])
    alerts = []

    if us["share"] < rules["share_floor"]:
        alerts.append({
            "level": "P1",
            "title": "我方份额偏低",
            "detail": f"当前份额 {us['share']:.0%} < 地板 {rules['share_floor']:.0%}，优先补密度与复购。",
            "action": "加密履约站 + 老客券，不做全网低价战",
        })

    for c in comps:
        if c["name"] == us["name"]:
            continue
        gap = us["price_index"] - c["price_index"]
        if gap >= rules["price_undercut_vs_us"]:
            alerts.append({
                "level": "P1",
                "title": f"{c['name']} 价格显著更低",
                "detail": f"价格指数 {c['price_index']} vs 我方 {us['price_index']}（低 {gap} 点）",
                "action": "核心 SKU 跟价观察 2 周；非核心用组合装守毛利",
            })
        nps_gap = c["nps"] - us["nps"]
        if nps_gap >= rules["nps_lead_vs_us"]:
            alerts.append({
                "level": "P2",
                "title": f"{c['name']} 体验领先",
                "detail": f"NPS {c['nps']} vs 我方 {us['nps']}（高 {nps_gap}）",
                "action": "拆差评 Top3 议题，对齐 VOC 原声复盘",
            })
        if c["promo_intensity"] >= rules["promo_spike"]:
            alerts.append({
                "level": "P2",
                "title": f"{c['name']} 促销强度偏高",
                "detail": f"促销强度 {c['promo_intensity']:.0%}",
                "action": "避免全面跟促；用会员日精准投放",
            })

    order = {"P1": 0, "P2": 1, "P3": 2}
    alerts.sort(key=lambda a: order.get(a["level"], 9))
    return alerts

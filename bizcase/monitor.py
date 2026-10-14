"""商业监控：KPI 看板 + 红黄绿灯 + 节奏与动作。"""

from __future__ import annotations

from .compete import compete_matrix, compete_alerts
from .unit_econ import unit_economics


def _status(actual: float, *, warn_below=None, warn_above=None,
            crit_below=None, crit_above=None) -> str:
    if crit_below is not None and actual < crit_below:
        return "红"
    if crit_above is not None and actual > crit_above:
        return "红"
    if warn_below is not None and actual < warn_below:
        return "黄"
    if warn_above is not None and actual > warn_above:
        return "黄"
    return "绿"


def _fmt(value: float, kind: str) -> str:
    if kind == "pct":
        return f"{value * 100:.1f}%"
    if kind == "yuan":
        return f"{value:.1f} 元"
    if kind == "months":
        return f"{value:.1f} 月"
    if kind == "index":
        return f"{value:.0f}"
    return f"{value:.2f}"


def _delta_fmt(delta: float, kind: str) -> str:
    sign = "+" if delta > 0 else ""
    if kind == "pct":
        return f"{sign}{delta * 100:.1f}pp"
    if kind in ("yuan", "months", "index"):
        return f"{sign}{delta:.1f}"
    return f"{sign}{delta:.2f}"


def monitor_board(cfg: dict) -> dict:
    """合成监控看板：配置 KPI + 从竞品/UE 拉实时字段。"""
    mcfg = cfg.get("monitor") or {}
    unit = unit_economics(cfg)
    comps = compete_matrix(cfg)
    us = next(c for c in comps if c["name"] == cfg["meta"]["brand"])
    live = {
        "share": us["share"],
        "price_index": us["price_index"],
        "nps": float(us["nps"]),
        "promo_intensity": us["promo_intensity"],
        "aov": unit["aov"],
        "gross_margin": unit["gross_margin"],
        "cac": unit["cac"],
        "contribution": unit["contribution"],
        "payback_months": unit["payback_months"] if unit["payback_months"] is not None else 99.0,
    }

    rows = []
    for item in mcfg.get("kpis") or []:
        key = item["key"]
        kind = item.get("kind", "yuan")
        # 优先用 live 字段，否则用配置 actual（演示快照）
        actual = live[key] if key in live else float(item["actual"])
        target = float(item["target"])
        wow = float(item.get("wow_delta", 0.0))
        status = _status(
            actual,
            warn_below=item.get("warn_below"),
            warn_above=item.get("warn_above"),
            crit_below=item.get("crit_below"),
            crit_above=item.get("crit_above"),
        )
        rows.append({
            "key": key,
            "name": item["name"],
            "kind": kind,
            "actual": actual,
            "actual_fmt": _fmt(actual, kind),
            "target": target,
            "target_fmt": _fmt(target, kind),
            "wow_delta": wow,
            "wow_fmt": _delta_fmt(wow, kind),
            "status": status,
            "owner": item.get("owner", "策略组"),
            "action": item.get("action", ""),
            "cadence": item.get("cadence", mcfg.get("default_cadence", "周")),
        })

    # 竞品规则告警并入监控「事件流」
    events = []
    for a in compete_alerts(cfg):
        events.append({
            "level": a["level"],
            "title": a["title"],
            "detail": a["detail"],
            "action": a["action"],
            "source": "竞品雷达",
        })
    for r in rows:
        if r["status"] == "红":
            events.append({
                "level": "P1",
                "title": f"KPI 红灯 · {r['name']}",
                "detail": f"实际 {r['actual_fmt']} vs 目标 {r['target_fmt']}（周变化 {r['wow_fmt']}）",
                "action": r["action"] or "当日复盘并给动作",
                "source": "KPI 看板",
            })
        elif r["status"] == "黄":
            events.append({
                "level": "P2",
                "title": f"KPI 黄灯 · {r['name']}",
                "detail": f"实际 {r['actual_fmt']} vs 目标 {r['target_fmt']}（周变化 {r['wow_fmt']}）",
                "action": r["action"] or "本周内纠偏",
                "source": "KPI 看板",
            })

    order = {"P1": 0, "P2": 1, "P3": 2}
    events.sort(key=lambda e: order.get(e["level"], 9))
    red = sum(1 for r in rows if r["status"] == "红")
    yellow = sum(1 for r in rows if r["status"] == "黄")
    green = sum(1 for r in rows if r["status"] == "绿")

    return {
        "as_of": mcfg.get("as_of", ""),
        "rhythm": mcfg.get("rhythm", ""),
        "rows": rows,
        "events": events,
        "summary": {"红": red, "黄": yellow, "绿": green},
        "narrative": (
            f"监控期 {mcfg.get('as_of', '—')}：绿 {green} / 黄 {yellow} / 红 {red}；"
            f"事件 {len(events)} 条。节奏：{mcfg.get('rhythm', '日巡检 + 周复盘')}。"
        ),
    }

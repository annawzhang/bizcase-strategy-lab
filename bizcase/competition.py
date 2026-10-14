"""商赛简介 · SOP 赛程 · 策划书映射 · 个人贡献（配置驱动）。"""

from __future__ import annotations


def competition_brief(cfg: dict) -> dict:
    c = cfg.get("competition") or {}
    stages = [dict(s) for s in c.get("sop_stages") or []]
    mapping = [dict(m) for m in c.get("plan_mapping") or []]
    contribs = [dict(x) for x in c.get("contributions") or []]
    scoring = [dict(s) for s in c.get("scoring") or []]

    intro = (
        f"{c.get('series', '全国高校商业精英挑战赛')}由"
        f"{c.get('organizer', '中国贸促会商业行业委员会等')}牵头主办，"
        f"本仓对齐「{c.get('track', '品牌策划赛道')}」方法："
        f"{c.get('mode', '企业出题—院校答题—行业判卷；真实品牌需书面授权')}。"
        f"团队通常 {c.get('team', '3–5 名选手 + 1–2 名指导教师')}。"
    )
    note = c.get("note", "")
    return {
        "series": c.get("series", ""),
        "track": c.get("track", ""),
        "organizer": c.get("organizer", ""),
        "mode": c.get("mode", ""),
        "team": c.get("team", ""),
        "award": c.get("award", ""),
        "real_case": c.get("real_case", ""),
        "demo_case": c.get("demo_case", ""),
        "role": c.get("role", ""),
        "platform": c.get("platform", ""),
        "intro": intro,
        "note": note,
        "stages": stages,
        "plan_mapping": mapping,
        "scoring": scoring,
        "contributions": contribs,
    }

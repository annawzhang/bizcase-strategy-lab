"""波特五力：强度评分 + 驱动因素 + 应对含义。"""

from __future__ import annotations

# 展示顺序（经典五力）
FORCE_ORDER = (
    "rivalry",
    "new_entrants",
    "substitutes",
    "buyer_power",
    "supplier_power",
)

LABELS = {
    "rivalry": "现有竞争者竞争程度",
    "new_entrants": "新进入者威胁",
    "substitutes": "替代品威胁",
    "buyer_power": "买方议价能力",
    "supplier_power": "供方议价能力",
}


def _bar(n: int) -> str:
    n = max(1, min(5, int(n)))
    return "●" * n + "○" * (5 - n)


def _level(n: int) -> str:
    if n >= 5:
        return "极强"
    if n >= 4:
        return "强"
    if n >= 3:
        return "中"
    if n >= 2:
        return "弱"
    return "极弱"


def porter_forces(cfg: dict) -> dict:
    raw = cfg.get("porter") or {}
    forces = []
    for key in FORCE_ORDER:
        f = raw.get(key) or {}
        intensity = int(f.get("intensity", 3))
        intensity = max(1, min(5, intensity))
        forces.append({
            "key": key,
            "label": LABELS[key],
            "intensity": intensity,
            "level": _level(intensity),
            "bar": _bar(intensity),
            "drivers": f.get("drivers", ""),
            "implication": f.get("implication", ""),
        })
    avg = sum(x["intensity"] for x in forces) / len(forces)
    hottest = max(forces, key=lambda x: x["intensity"])
    narrative = (
        f"五力均强约 {avg:.1f}/5；当前最紧的是「{hottest['label']}」（{_level(hottest['intensity'])}）。"
        f"苏州社区零售里，宜用履约密度与私域复购对冲价格战，而不是全面降价。"
    )
    return {
        "forces": forces,
        "avg_intensity": avg,
        "hottest": hottest,
        "narrative": narrative,
    }

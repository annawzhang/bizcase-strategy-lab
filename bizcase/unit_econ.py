"""单位经济：单均贡献、回本月数。"""

from __future__ import annotations


def unit_economics(cfg: dict, *, aov=None, gross_margin=None, cac=None,
                   fulfill_cost=None, take_rate_other=None,
                   orders_per_month=None) -> dict:
    u = cfg["unit"]
    aov = u["aov"] if aov is None else aov
    gm = u["gross_margin"] if gross_margin is None else gross_margin
    cac = u["cac"] if cac is None else cac
    fulfill = u["fulfill_cost"] if fulfill_cost is None else fulfill_cost
    other = u["take_rate_other"] if take_rate_other is None else take_rate_other
    opm = u["orders_per_month"] if orders_per_month is None else orders_per_month

    gross_profit = aov * gm
    contribution = gross_profit - fulfill - aov * other
    # 首单：贡献 - CAC；后续单：贡献
    first_order_net = contribution - cac
    monthly_contrib = contribution * opm
    if monthly_contrib <= 0:
        payback = None
    else:
        # 首月含获客：若首单净贡献为负，用后续月贡献回本
        if first_order_net >= 0:
            payback = 1 / opm  # 不足一个月
        else:
            remain = -first_order_net
            payback = 1 / opm + remain / monthly_contrib

    healthy = (
        contribution > 0
        and payback is not None
        and payback <= u["months_to_payback_cap"]
    )
    return {
        "aov": aov,
        "gross_margin": gm,
        "gross_profit": gross_profit,
        "fulfill_cost": fulfill,
        "other_cost": aov * other,
        "contribution": contribution,
        "cac": cac,
        "first_order_net": first_order_net,
        "orders_per_month": opm,
        "monthly_contrib": monthly_contrib,
        "payback_months": payback,
        "healthy": healthy,
        "cap": u["months_to_payback_cap"],
    }

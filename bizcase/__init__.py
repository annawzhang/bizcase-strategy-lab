"""商赛四件套：市场测算 · 竞品雷达 · 单位经济 · 情景推演。"""

from .market import market_sizing
from .compete import compete_matrix, compete_alerts
from .unit_econ import unit_economics
from .scenario import run_scenarios
from .judge import judge_pack

__all__ = [
    "market_sizing",
    "compete_matrix",
    "compete_alerts",
    "unit_economics",
    "run_scenarios",
    "judge_pack",
]

"""商赛工具：简介架构 · 市场 · 竞品 · UE · 情景 · 五力 · 监控。"""

from .competition import competition_brief
from .market import market_sizing
from .compete import compete_matrix, compete_alerts
from .unit_econ import unit_economics
from .scenario import run_scenarios
from .porter import porter_forces
from .monitor import monitor_board

__all__ = [
    "competition_brief",
    "market_sizing",
    "compete_matrix",
    "compete_alerts",
    "unit_economics",
    "run_scenarios",
    "porter_forces",
    "monitor_board",
]

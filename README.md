# BizCase Strategy Lab · 商赛策略工作台

**市场测算 · 竞品雷达 · 单位经济 · 情景推演 · 波特五力 · 商业监控。** 行业设定：虚构「苏州零售消费 · 社区优选品牌苏里优选」。

[在线报告](https://annawzhang.github.io/bizcase-strategy-lab/) · 纯 Python 标准库，无第三方依赖

> 人口、份额、竞品与财务假设全部为演示数据，**不是**真实苏州市场统计，也不是往届赛题原题。

## 模块

| 模块 | 做什么 | 配置 |
|---|---|---|
| 市场测算 | 人口→家庭→支出→可触达→地理→份额 | `[market]` |
| 竞品雷达 | 价格/SKU/NPS/份额/促销 + P1/P2 告警 | `[[competitors]]` + `[compete_rules]` |
| 单位经济 | 客单、毛利、履约、CAC、回本月数 | `[unit]` |
| 情景推演 | 悲观 / 基准 / 乐观 | `[scenarios.*]` |
| 波特五力 | 五力强度 1–5 + 驱动因素 + 对我方含义 | `[porter.*]` |
| 商业监控 | KPI 红黄绿灯、周变化、节奏/负责人、事件流 | `[monitor]` + `[[monitor.kpis]]` |

监控会从竞品与单位经济回填份额/价格/NPS/毛利/CAC 等实际值，再按阈值打灯；竞品告警并入事件流。

## 本地运行

```bash
python3 -m unittest discover -s tests -v
python3 run.py   # → docs/index.html
```

改 `config/case.toml` 再跑 `run.py` 即更新报告。

## 背景

对应「全国商业精英挑战赛」等方法训练的公开工具化练习：强调可解释假设与决策纪律，而非上传真实 BP。数据虚构。

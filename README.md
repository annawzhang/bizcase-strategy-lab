# BizCase Strategy Lab · 商赛策略工作台

**对齐全国高校商业精英挑战赛（品牌策划赛道）公开 SOP：赛程简介 · 策划书章节映射 · 个人贡献，再接可跑模块——市场测算 · 竞品雷达 · 单位经济 · 情景 · 波特五力 · 商业监控。**

演示行业：虚构「苏州零售消费 · 苏里优选」。真实履历案例为宋锦品牌（全国三等奖），与本仓数据隔离。

[在线报告](https://annawzhang.github.io/bizcase-strategy-lab/) · 纯 Python 标准库

## 报告结构

| # | 板块 | 说明 |
|---|---|---|
| 0 | 商赛简介 · 架构与贡献 | CUBEC SOP 赛程、策划书↔模块映射、评分摘要、个人贡献 |
| 1–4 | 四件套 | TAM/SAM/SOM · 竞品告警 · 单位经济 · 情景推演 |
| 5 | 波特五力 | 强度 + 驱动 + 含义 |
| 6 | 商业监控 | KPI 红黄绿 + 事件流 |

## 本地运行

```bash
python3 -m unittest discover -s tests -v
python3 run.py   # → docs/index.html
```

配置：`config/case.toml`（含 `[competition]` / `[porter]` / `[monitor]`）。

## 背景

方法工具化练习，不上传真实 BP。赛制摘要来自公开细则（知识赛→校赛→省赛/预选→全国总决赛等），非官方全文。

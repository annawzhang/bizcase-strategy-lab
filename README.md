# BizCase Strategy Lab · 商赛策略工作台

**把通用商赛四件套做成可跑工具：市场测算（TAM/SAM/SOM）· 竞品雷达与告警 · 单位经济 · 情景推演，外加评委追问包。行业设定为虚构的「苏州零售消费 · 社区优选品牌苏里优选」。**

[在线报告](https://annawzhang.github.io/bizcase-strategy-lab/) · 纯 Python 标准库，无第三方依赖

> 人口、份额、竞品与财务假设全部为演示数据，**不是**真实苏州市场统计，也不是往届赛题原题。

## 四件套

| 模块 | 做什么 | 配置 |
|---|---|---|
| 市场测算 | 人口→家庭→支出→可触达→地理→份额 | `[market]` |
| 竞品雷达 | 价格/SKU/NPS/份额/促销 + P1/P2 告警 | `[[competitors]]` + `[compete_rules]` |
| 单位经济 | 客单、毛利、履约、CAC、回本月数 | `[unit]` |
| 情景推演 | 悲观 / 基准 / 乐观 | `[scenarios.*]` |

额外：**评委追问包**——用当前假设自动生成 6 道常见追问的回答要点。

## 本地运行

```bash
python3 -m unittest discover -s tests -v
python3 run.py   # → docs/index.html
```

改 `config/case.toml` 里的渗透率、份额或 CAC，再跑 `run.py` 即更新报告——这就是商赛里「假设可审计」的产品化。

## 背景

对应简历中「全国商业精英挑战赛」等方法训练的公开工具化练习：强调可解释假设与决策纪律，而非上传真实 BP。与实习复刻仓隔离，数据虚构。

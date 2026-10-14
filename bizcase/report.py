"""生成 docs/index.html。"""

from __future__ import annotations

from html import escape


def _yi(n: float) -> str:
    return f"{n / 1e8:.2f} 亿"


def _pct(x: float, d: int = 0) -> str:
    return f"{x * 100:.{d}f}%"


def _pay(m: float | None) -> str:
    return "—" if m is None else f"{m:.1f}"


def render(cfg: dict, market: dict, comps: list, alerts: list, unit: dict, scenarios: list, judges: list) -> str:
    meta = cfg["meta"]
    ass = market["assumptions"]
    comp_rows = "".join(
        f"<tr><td>{escape(c['name'])}</td><td class='num'>{c['price_index']}</td>"
        f"<td class='num'>{c['sku']}</td><td class='num'>{c['nps']}</td>"
        f"<td class='num'>{_pct(c['share'])}</td><td class='num'>{_pct(c['promo_intensity'])}</td>"
        f"<td>{escape(c['note'])}</td></tr>"
        for c in comps
    )
    alert_html = "".join(
        f"<div class='alert {a['level'].lower()}'><b>{a['level']} · {escape(a['title'])}</b>"
        f"<div>{escape(a['detail'])}</div><div class='act'>动作：{escape(a['action'])}</div></div>"
        for a in alerts
    ) or "<p class='muted'>暂无告警</p>"
    sc_rows = "".join(
        f"<tr><td>{escape(s['label'])}</td><td class='num'>{_yi(s['som'])}</td>"
        f"<td class='num'>{_pct(s['params']['share_y3'])}</td>"
        f"<td class='num'>{s['unit']['aov']:.0f}</td>"
        f"<td class='num'>{_pct(s['unit']['gross_margin'])}</td>"
        f"<td class='num'>{s['unit']['cac']:.0f}</td>"
        f"<td class='num'>{s['unit']['contribution']:.1f}</td>"
        f"<td class='num'>{_pay(s['unit']['payback_months'])}</td>"
        f"<td>{'✓' if s['unit']['healthy'] else '✗'}</td></tr>"
        for s in scenarios
    )
    judge_html = "".join(
        f"<div class='qa'><div class='q'>Q：{escape(j['q'])}</div>"
        f"<div class='a'>{escape(j['a'])}</div></div>"
        for j in judges
    )
    healthy = "健康" if unit["healthy"] else "需优化"
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>BizCase Strategy Lab · {escape(meta['title'])}</title>
<style>
:root {{ --text:#0f172a; --muted:#64748b; --border:#e2e8f0; --accent:#0f766e; --bg:#f8fafc; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:var(--bg); color:var(--text); font-size:14px; line-height:1.6; }}
.wrap {{ max-width:980px; margin:0 auto; padding:28px 20px 64px; }}
h1 {{ font-size:1.55rem; margin:6px 0; }}
h2 {{ font-size:1.08rem; margin:28px 0 10px; border-left:4px solid var(--accent); padding-left:10px; }}
.muted {{ color:var(--muted); font-size:0.86rem; }}
.badge {{ display:inline-block; background:#fef3c7; color:#92400e; border-radius:999px; padding:2px 10px; font-size:0.75rem; }}
.grid {{ display:grid; gap:12px; grid-template-columns:repeat(4,1fr); margin:14px 0; }}
@media (max-width:800px) {{ .grid {{ grid-template-columns:1fr 1fr; }} }}
.card {{ background:#fff; border:1px solid var(--border); border-radius:12px; padding:14px; }}
.card .lbl {{ color:var(--muted); font-size:0.78rem; }} .card .val {{ font-size:1.35rem; font-weight:700; margin-top:4px; }}
table {{ width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--border); border-radius:12px; overflow:hidden; font-size:0.84rem; }}
th, td {{ padding:8px 10px; border-bottom:1px solid var(--border); text-align:left; vertical-align:top; }}
th {{ color:var(--muted); font-weight:600; }} td.num, th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
.note {{ background:#f0fdfa; border:1px solid #99f6e4; border-radius:10px; padding:12px 14px; font-size:0.86rem; margin-top:10px; }}
.alert {{ background:#fff; border:1px solid var(--border); border-left:4px solid #94a3b8; border-radius:10px; padding:10px 12px; margin:8px 0; font-size:0.86rem; }}
.alert.p1 {{ border-left-color:#b91c1c; background:#fef2f2; }}
.alert.p2 {{ border-left-color:#b45309; background:#fff7ed; }}
.act {{ color:var(--muted); margin-top:4px; }}
.qa {{ background:#fff; border:1px solid var(--border); border-radius:12px; padding:12px 14px; margin:8px 0; }}
.q {{ font-weight:600; margin-bottom:6px; }} .a {{ color:#334155; font-size:0.88rem; }}
code {{ background:#f1f5f9; padding:1px 5px; border-radius:4px; font-size:0.82rem; }}
</style>
</head>
<body>
<div class="wrap">
  <span class="badge">虚构商赛案例 · 苏州零售消费</span>
  <h1>{escape(meta['title'])}</h1>
  <p class="muted">{escape(meta['city'])} · {escape(meta['category'])} · 品牌 {escape(meta['brand'])} · {meta['year']}<br/>
  {escape(meta['disclaimer'])}</p>

  <div class="grid">
    <div class="card"><div class="lbl">TAM</div><div class="val">{_yi(market['tam'])}</div><div class="muted">家庭日用总支出/年</div></div>
    <div class="card"><div class="lbl">SAM</div><div class="val">{_yi(market['sam'])}</div><div class="muted">社区优选可触达</div></div>
    <div class="card"><div class="lbl">SOM（三年）</div><div class="val">{_yi(market['som'])}</div><div class="muted">可服务区 × 目标份额</div></div>
    <div class="card"><div class="lbl">单位经济</div><div class="val">{healthy}</div><div class="muted">回本 {_pay(unit['payback_months'])} 月</div></div>
  </div>

  <h2>1. 市场测算 · TAM / SAM / SOM</h2>
  <p class="muted">{escape(market['narrative'])}</p>
  <table>
    <thead><tr><th>假设</th><th class="num">取值</th></tr></thead>
    <tbody>
      <tr><td>常住人口</td><td class="num">{ass['population']:,}</td></tr>
      <tr><td>户均人口</td><td class="num">{ass['household_size']}</td></tr>
      <tr><td>家庭月支出（元）</td><td class="num">{ass['monthly_spend_per_hh']:.0f}</td></tr>
      <tr><td>可触达品类占比</td><td class="num">{_pct(ass['addressable_share'])}</td></tr>
      <tr><td>社区优选赛道占比</td><td class="num">{_pct(ass['segment_share'])}</td></tr>
      <tr><td>可服务地理占比</td><td class="num">{_pct(ass['serviceable_geo'])}</td></tr>
      <tr><td>三年目标份额</td><td class="num">{_pct(ass['target_share_y3'])}</td></tr>
    </tbody>
  </table>
  <div class="note">每一层都在 <code>config/case.toml</code>，改渗透率或份额即可重算——商赛里「假设可审计」比拍一个总数更重要。</div>

  <h2>2. 竞品雷达 · 今日告警</h2>
  <table>
    <thead><tr><th>品牌</th><th class="num">价格指数</th><th class="num">SKU</th><th class="num">NPS</th><th class="num">份额</th><th class="num">促销强度</th><th>备注</th></tr></thead>
    <tbody>{comp_rows}</tbody>
  </table>
  {alert_html}

  <h2>3. 单位经济 · 单均订单</h2>
  <table>
    <thead><tr><th>指标</th><th class="num">数值</th></tr></thead>
    <tbody>
      <tr><td>客单价 AOV</td><td class="num">{unit['aov']:.1f} 元</td></tr>
      <tr><td>毛利率</td><td class="num">{_pct(unit['gross_margin'])}</td></tr>
      <tr><td>毛利额</td><td class="num">{unit['gross_profit']:.1f} 元</td></tr>
      <tr><td>履约成本</td><td class="num">{unit['fulfill_cost']:.1f} 元</td></tr>
      <tr><td>其他（支付/损耗）</td><td class="num">{unit['other_cost']:.1f} 元</td></tr>
      <tr><td>单均贡献</td><td class="num"><b>{unit['contribution']:.1f} 元</b></td></tr>
      <tr><td>CAC</td><td class="num">{unit['cac']:.1f} 元</td></tr>
      <tr><td>首单净贡献</td><td class="num">{unit['first_order_net']:.1f} 元</td></tr>
      <tr><td>月复购次数</td><td class="num">{unit['orders_per_month']:.1f}</td></tr>
      <tr><td>回本月数</td><td class="num">{_pay(unit['payback_months'])}（上限 {unit['cap']}）</td></tr>
    </tbody>
  </table>

  <h2>4. 情景推演 · 乐观 / 基准 / 悲观</h2>
  <table>
    <thead><tr><th>情景</th><th class="num">SOM</th><th class="num">三年份额</th><th class="num">AOV</th><th class="num">毛利</th><th class="num">CAC</th><th class="num">贡献</th><th class="num">回本月</th><th>健康</th></tr></thead>
    <tbody>{sc_rows}</tbody>
  </table>
  <div class="note">悲观若回本失败：优先收缩可服务地理与补贴，而不是加码获客——这是商赛里常见的「纪律」答法。</div>

  <h2>5. 评委追问包</h2>
  {judge_html}

  <p class="muted" style="margin-top:28px">本地：<code>python3 run.py</code> · 测试：<code>python3 -m unittest discover -s tests -v</code></p>
</div>
</body>
</html>
"""

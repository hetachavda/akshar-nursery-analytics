"""Build dashboard/index.html: a self-contained one-page dashboard (KPIs, charts, findings, sowing plan).

Reads reports/kpis.json and reports/figures/*.png produced by the notebook.
Run:  python src/build_dashboard.py
"""
import base64, html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = json.loads((ROOT / "reports" / "kpis.json").read_text(encoding="utf-8"))
FIG = ROOT / "reports" / "figures"
OUT = ROOT / "dashboard" / "index.html"
LOGO = (ROOT / "assets" / "logo" / "akshar_icon.svg").read_text(encoding="utf-8")
FAV = base64.b64encode((ROOT / "assets" / "logo" / "akshar_favicon_512.png").read_bytes()).decode()
REPO_URL = "https://github.com/hetachavda/akshar-nursery-analytics"   # change after creating the repo

def img(name, alt):
    b64 = base64.b64encode((FIG / f"{name}.png").read_bytes()).decode()
    return f'<img src="data:image/png;base64,{b64}" alt="{html.escape(alt)}" loading="lazy">'

def lakh(x):
    return f"₹{x / 1e5:,.1f} L"

kpi_cards = [
    ("Total revenue", lakh(K["total_revenue"]), "Jan 2024 to Aug 2026"),
    ("Revenue 2025", lakh(K["revenue_2025"]), f"{K['growth_2025_vs_2024_pct']:+.0f}% vs 2024"),
    ("Revenue 2026 (Jan to Aug)", lakh(K["ytd_revenue_2026"]), f"{K['ytd_growth_2026_vs_2025_pct']:+.0f}% vs same months 2025"),
    ("Seedlings sold", f"{K['total_seedlings'] / 1e5:,.0f} lakh", f"{K['total_orders']:,} orders"),
    ("Customers", f"{K['total_customers']:,}", f"{K['retention_2024_to_2025_pct']:.0f}% of 2024 buyers returned"),
    ("Gross margin", f"{K['overall_margin_pct']:.0f}%", "after seed and raising cost"),
    ("Peak season share", f"{K['peak_season_share_pct']:.0f}%", "of revenue in June to September"),
    ("Pro-tray chilli", f"{K['chilli_protray_2026']:.0f}%", f"up from {K['chilli_protray_2024']:.0f}% in 2024"),
]
kpi_html = "\n".join(
    f'<div class="kpi"><span class="k-label">{a}</span><span class="k-value">{b}</span><span class="k-note">{c}</span></div>'
    for a, b, c in kpi_cards)

sections = [
    ("Sales and seasonality", [
        ("01_monthly_revenue_by_year", "Monthly revenue by year", "wide"),
        ("02_seasonality_heatmap", "Seasonality heatmap by crop", "wide"),
    ]),
    ("Crops and varieties", [
        ("03_crop_revenue", "Revenue by crop and revenue per 1,000 seedlings", "wide"),
        ("04_variety_pareto", "Variety revenue ranking", "wide"),
        ("05_protray_adoption", "Pro-tray adoption by crop", ""),
        ("09_margin_by_variety", "Revenue vs gross margin by variety", ""),
    ]),
    ("Customers and channels", [
        ("06_customer_segments", "Customer segments and retention", "wide"),
        ("07_village_revenue", "Revenue by village", ""),
        ("10_payments_channels", "Payments and order channels", ""),
    ]),
    ("Production and planning", [
        ("08_production_efficiency", "Germination and unsold seedlings", "wide"),
        ("11_demand_plan", "Forecast demand, September to December 2026", "wide"),
    ]),
]
sec_html = ""
for title, charts in sections:
    cards = "\n".join(f'<figure class="chart {cls}">{img(n, alt)}</figure>' for n, alt, cls in charts)
    sec_html += f'<section><h2>{title}</h2><div class="charts">{cards}</div></section>\n'

findings = "\n".join(f"<li>{html.escape(f)}</li>" for f in K["findings"])
recs = "\n".join(f"<li>{html.escape(r)}</li>" for r in K["recommendations"])
plan_rows = "\n".join(
    f"<tr><td>{p['crop']}</td><td>{p['month']}</td><td>{p['forecast_seedlings']:,.0f}</td>"
    f"<td>{p['seeds_to_sow']:,.0f}</td><td>{p['sow_by']}</td><td>{p['growth_vs_2025']}</td></tr>"
    for p in K["plan"])

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Akshar Farm And Nursery | Sales and Operations Dashboard</title>
<link rel="icon" type="image/png" href="data:image/png;base64,{FAV}">
<meta name="description" content="Data analysis dashboard for a seedling nursery in Kheda, Gujarat: seasonality, crops, customers, production efficiency and a sowing plan.">
<style>
:root{{--soil:#4A3426;--leaf:#4F7F2A;--leaf2:#86B04A;--marigold:#E39B12;--paper:#F4F6EC;--card:#fff;--ink:#2A2019;--muted:#6B5E4E;--line:#E2DFD2;
  box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
*,*::before,*::after{{box-sizing:inherit}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Segoe UI",system-ui,-apple-system,Roboto,sans-serif;line-height:1.5}}
.wrap{{width:min(1180px,100% - 2rem);margin-inline:auto}}
header{{background:var(--soil);color:#F3F5EA;padding:2.2rem 0 2rem}}
header .eyebrow{{color:var(--leaf2);font-weight:600;margin:0}}
.logo-row{{display:flex;align-items:center;gap:.8rem;margin-bottom:.6rem}} .logo-row svg{{flex:none;margin:-6px}}
h1{{margin:0;font-size:clamp(1.6rem,3.4vw,2.4rem);line-height:1.15}}
header p{{margin:.6rem 0 0;color:#D5CEBF;max-width:70ch}}
.links{{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1.1rem}}
.links a{{color:#F3F5EA;text-decoration:none;border:1.5px solid rgba(255,255,255,.35);padding:.4rem .9rem;border-radius:999px;font-weight:600;font-size:.92rem}}
.links a:hover{{background:rgba(255,255,255,.1)}}
.note{{background:#FFF7E6;border:1px solid #F1D9A6;color:#6B4A0E;border-radius:10px;padding:.8rem 1rem;margin:1.5rem 0 0;font-size:.95rem}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:.9rem;margin:1.5rem 0 0}}
.kpi{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1rem 1.1rem;display:flex;flex-direction:column;gap:.15rem}}
.k-label{{font-size:.85rem;color:var(--muted);font-weight:600}}
.k-value{{font-size:1.7rem;font-weight:800;color:var(--soil);font-variant-numeric:tabular-nums}}
.k-note{{font-size:.85rem;color:var(--leaf)}}
section{{margin:2.4rem 0 0}}
h2{{font-size:1.35rem;margin:0 0 .9rem;color:var(--soil)}}
.charts{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
.chart{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:.8rem;overflow-x:auto}}
.chart.wide{{grid-column:1 / -1}}
.chart img{{display:block;width:100%;height:auto;min-width:520px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
.panel{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1.2rem 1.4rem}}
.panel h3{{margin:0 0 .6rem;font-size:1.05rem;color:var(--soil)}}
.panel ol{{margin:0;padding-left:1.2rem}} .panel li{{margin:.45rem 0}}
.table-wrap{{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}}
table{{border-collapse:collapse;width:100%;font-size:.95rem}}
th,td{{padding:.6rem .9rem;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}}
th{{background:#EFEBDD;color:var(--soil);font-weight:700}}
td:nth-child(3),td:nth-child(4),th:nth-child(3),th:nth-child(4){{text-align:right;font-variant-numeric:tabular-nums}}
footer{{margin:3rem 0 0;padding:1.5rem 0 2rem;color:var(--muted);font-size:.9rem;border-top:1px solid var(--line)}}
@media (max-width:860px){{.kpis{{grid-template-columns:1fr 1fr}}.charts,.two{{grid-template-columns:1fr}}.k-value{{font-size:1.4rem}}}}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <div class="logo-row">{LOGO.replace('width="320" height="320"', 'width="56" height="56"')}<p class="eyebrow">Data analysis project</p></div>
    <h1>Akshar Farm And Nursery: Sales and Operations Dashboard</h1>
    <p>Seedling nursery in Jesapura Mithapura, Kheda, Gujarat. Seasonality, crop and variety performance, customers, production efficiency and a sowing plan for September to December 2026.</p>
    <div class="links">
      <a href="../website/">Business website</a>
      <a href="{REPO_URL}">Notebook and SQL on GitHub</a>
    </div>
  </div>
</header>
<main class="wrap">
  <p class="note"><strong>About the data:</strong> the business, crops, seed varieties and locations are real. The transaction data is simulated from documented assumptions (see the README), because the nursery keeps paper records. The same pipeline runs on real sales once they are logged.</p>
  <div class="kpis">{kpi_html}</div>
  {sec_html}
  <section>
    <h2>Findings and recommendations</h2>
    <div class="two">
      <div class="panel"><h3>Key findings</h3><ol>{findings}</ol></div>
      <div class="panel"><h3>Recommendations</h3><ol>{recs}</ol></div>
    </div>
  </section>
  <section>
    <h2>Sowing plan, September to December 2026</h2>
    <div class="table-wrap"><table>
      <thead><tr><th>Crop</th><th>Month</th><th>Forecast seedlings</th><th>Seeds to sow</th><th>Sow by</th><th>Growth vs 2025</th></tr></thead>
      <tbody>{plan_rows}</tbody>
    </table></div>
  </section>
  <footer>Built with Python (pandas, matplotlib) and SQL (SQLite). Analysis notebook: notebooks/akshar_nursery_analysis.ipynb.</footer>
</main>
</body>
</html>
"""
OUT.write_text(page, encoding="utf-8")
print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1e6:.1f} MB)")

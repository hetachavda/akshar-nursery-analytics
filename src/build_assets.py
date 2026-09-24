"""Build assets/banner.svg and assets/dashboard.svg for the README (numbers come from the data).

Run:  python src/build_assets.py
"""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "assets"; A.mkdir(exist_ok=True)
K = json.loads((ROOT / "reports" / "kpis.json").read_text(encoding="utf-8"))
o = pd.read_csv(ROOT / "data" / "raw" / "orders.csv", parse_dates=["order_date"])

FONT = "Segoe UI, Helvetica Neue, Arial, sans-serif"
SOIL, LEAF, LEAF2, MARI, CHILLI, PAPER, INK, MUTED = "#4A3426", "#4F7F2A", "#86B04A", "#E39B12", "#B8322A", "#F4F6EC", "#2A2019", "#6B5E4E"

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ------------------------------------------------------------------ banner
dots = "".join(f'<circle cx="{820 + c * 34 + (r % 2) * 17}" cy="{22 + r * 30}" r="9" fill="#ffffff" opacity="{0.025 + 0.015 * ((r + c) % 3)}"/>'
               for r in range(10) for c in range(12))
sprout = f'''<g transform="translate(64,62)">
  <rect width="64" height="64" rx="16" fill="{PAPER}"/>
  <path d="M32 54 V28" stroke="{LEAF2}" stroke-width="4" stroke-linecap="round"/>
  <path d="M32 33 C18 33 12 22 13 13 C25 13 32 21 32 33Z" fill="{LEAF}"/>
  <path d="M32 27 C46 27 52 16 51 7 C39 7 32 15 32 27Z" fill="{LEAF2}"/>
</g>'''
tags = ["Website", "Python", "SQL", "Dashboard", "Real business"]
tx = 64; tag_svg = ""
for t in tags:
    w = 30 + len(t) * 8.4
    tag_svg += f'<rect x="{tx}" y="228" width="{w}" height="30" rx="15" fill="none" stroke="{LEAF2}" stroke-width="1.5"/>'
    tag_svg += f'<text x="{tx + w / 2}" y="248" text-anchor="middle" font-size="14" font-weight="600" fill="#E9E4D8">{t}</text>'
    tx += w + 10
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300" font-family="{FONT}">
<defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#3A2A1F"/><stop offset="1" stop-color="#2A1E16"/></linearGradient></defs>
<rect width="1200" height="300" fill="url(#g)"/>
{dots}
<rect x="0" y="290" width="720" height="10" fill="{SOIL}"/><rect x="720" y="290" width="300" height="10" fill="{LEAF2}"/><rect x="1020" y="290" width="180" height="10" fill="{MARI}"/>
{sprout}
<text x="148" y="88" font-size="16" font-weight="600" fill="{LEAF2}">Jesapura Mithapura · Kheda, Gujarat</text>
<text x="148" y="124" font-size="34" font-weight="800" fill="#F3F5EA">Akshar Farm And Nursery</text>
<text x="64" y="176" font-size="24" font-weight="600" fill="#F3F5EA">Website + Sales &amp; Operations Data Analysis</text>
<text x="64" y="206" font-size="16" fill="#CFC7B8">Seasonality, crop and variety performance, customers, production efficiency and a sowing plan</text>
{tag_svg}
</svg>'''
(A / "banner.svg").write_text(banner, encoding="utf-8")

# ------------------------------------------------------------------ dashboard
W, H = 1200, 660
def card(x, y, w, h, fill="#FFFFFF"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#E2DFD2"/>'

kpis = [
    ("Total revenue", f"₹{K['total_revenue'] / 1e5:,.0f} L", "Jan 2024 to Aug 2026"),
    ("Growth 2025", f"+{K['growth_2025_vs_2024_pct']:.0f}%", "vs 2024"),
    ("Peak season", f"{K['peak_season_share_pct']:.0f}%", "of revenue, Jun to Sep"),
    ("Gross margin", f"{K['overall_margin_pct']:.0f}%", "after seed & raising cost"),
    ("Pro-tray chilli", f"{K['chilli_protray_2026']:.0f}%", f"up from {K['chilli_protray_2024']:.0f}% in 2024"),
    ("Customers", f"{K['total_customers']:,}", f"{K['retention_2024_to_2025_pct']:.0f}% returned next year"),
]
parts = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<rect width="{W}" height="78" fill="{SOIL}"/>',
         f'<text x="36" y="36" font-size="13" font-weight="600" fill="{LEAF2}">SALES &amp; OPERATIONS DASHBOARD</text>',
         f'<text x="36" y="62" font-size="22" font-weight="800" fill="#F3F5EA">Akshar Farm And Nursery</text>',
         f'<text x="{W - 36}" y="52" font-size="13" text-anchor="end" fill="#CFC7B8">Simulated transactions · real business, crops &amp; varieties</text>']
cw = (W - 72 - 5 * 14) / 6
for i, (lab, val, note) in enumerate(kpis):
    x = 36 + i * (cw + 14)
    parts += [card(x, 98, cw, 104), f'<text x="{x + 16}" y="124" font-size="12.5" font-weight="600" fill="{MUTED}">{lab}</text>',
              f'<text x="{x + 16}" y="160" font-size="28" font-weight="800" fill="{SOIL}">{esc(val)}</text>',
              f'<text x="{x + 16}" y="186" font-size="11.5" fill="{LEAF}">{esc(note)}</text>']

# monthly revenue 2025 vs 2024 bars
mm = o.assign(y=o.order_date.dt.year, m=o.order_date.dt.month).groupby(["y", "m"]).revenue_inr.sum()
x0, y0, cwid, chgt = 36, 222, 700, 300
parts += [card(x0, y0, cwid, chgt), f'<text x="{x0 + 20}" y="{y0 + 32}" font-size="16" font-weight="700" fill="{INK}">Monthly revenue: 2024 vs 2025</text>']
mx = max(mm[2024].max(), mm[2025].max())
bx, by, bw, bh = x0 + 36, y0 + 58, cwid - 60, 196
for mth in range(1, 13):
    gx = bx + (mth - 1) * bw / 12
    for k, (yr, col) in enumerate([(2024, "#C9BFAE"), (2025, LEAF)]):
        v = mm[yr].get(mth, 0); h = bh * v / mx
        parts.append(f'<rect x="{gx + 8 + k * 17:.1f}" y="{by + bh - h:.1f}" width="15" height="{h:.1f}" rx="3" fill="{col}"/>')
    parts.append(f'<text x="{gx + 24:.1f}" y="{by + bh + 18}" font-size="11" text-anchor="middle" fill="{MUTED}">{"JFMAMJJASOND"[mth - 1]}</text>')
parts += [f'<rect x="{x0 + cwid - 170}" y="{y0 + 22}" width="12" height="12" rx="2" fill="#C9BFAE"/><text x="{x0 + cwid - 152}" y="{y0 + 33}" font-size="12" fill="{MUTED}">2024</text>',
          f'<rect x="{x0 + cwid - 110}" y="{y0 + 22}" width="12" height="12" rx="2" fill="{LEAF}"/><text x="{x0 + cwid - 92}" y="{y0 + 33}" font-size="12" fill="{MUTED}">2025</text>']

# crop share
cs = o.groupby("crop").revenue_inr.sum().sort_values(ascending=False)
cs = 100 * cs / cs.sum()
colors = {"Chilli": CHILLI, "Tomato": "#E0603A", "Capsicum": "#2F7D32", "Brinjal": "#5B2C6F", "Marigold": MARI, "Tobacco": "#8A7F6E"}
x1 = x0 + cwid + 16; w1 = W - 36 - x1
parts += [card(x1, y0, w1, chgt), f'<text x="{x1 + 20}" y="{y0 + 32}" font-size="16" font-weight="700" fill="{INK}">Revenue share by crop</text>']
for i, (c, v) in enumerate(cs.items()):
    yy = y0 + 62 + i * 38; full = w1 - 150
    parts += [f'<text x="{x1 + 20}" y="{yy + 15}" font-size="13" fill="{INK}">{c}</text>',
              f'<rect x="{x1 + 100}" y="{yy + 2}" width="{full}" height="18" rx="9" fill="#EFEBDD"/>',
              f'<rect x="{x1 + 100}" y="{yy + 2}" width="{max(full * v / 100, 10):.1f}" height="18" rx="9" fill="{colors[c]}"/>',
              f'<text x="{x1 + 108 + max(full * v / 100, 10):.1f}" y="{yy + 16}" font-size="12" font-weight="700" fill="{INK}">{v:.0f}%</text>']

# insights strip
iy = y0 + chgt + 16; ih = H - iy - 24
ins = [(LEAF2, "Pro-tray chilli", f"{K['chilli_tray_margin_pct']:.0f}% margin vs {K['chilli_bed_margin_pct']:.0f}% for bed"),
       (MARI, "Tobacco", f"₹{K['tobacco_profit_per_1000']:.0f} profit per 1,000 vs ₹{K['chilli_tray_profit_per_1000']:.0f} chilli"),
       (CHILLI, "Unsold seedlings", f"{K['protray_unsold_pct']:.0f}% of pro-tray raised"),
       ("#25A244", "WhatsApp orders", f"{K['whatsapp_2026_pct']:.0f}% of orders in 2026")]
iw = (W - 72 - 3 * 14) / 4
for i, (col, t, d) in enumerate(ins):
    x = 36 + i * (iw + 14)
    parts += [card(x, iy, iw, ih), f'<rect x="{x + 1}" y="{iy + 14}" width="5" height="{ih - 28}" rx="2.5" fill="{col}"/>',
              f'<text x="{x + 22}" y="{iy + 42}" font-size="15" font-weight="700" fill="{SOIL}">{esc(t)}</text>',
              f'<text x="{x + 22}" y="{iy + 68}" font-size="13" fill="{MUTED}">{esc(d)}</text>']

dash = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">' + "".join(parts) + "</svg>"
(A / "dashboard.svg").write_text(dash, encoding="utf-8")
print("Wrote assets/banner.svg and assets/dashboard.svg")

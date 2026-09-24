"""
Generate a SIMULATED dataset for Akshar Farm And Nursery (Jesapura Mithapura, Kheda, Gujarat).

What is real:   the business, its crops, the seed varieties it raises (seen on seed packets
                in the nursery), its sowing methods (pro-tray and nursery beds), opening hours
                and the surrounding villages.
What is simulated: every transaction, customer, quantity, price, cost and batch below.
                Prices, costs and seasonality are reasoned assumptions, documented in
                ASSUMPTIONS so they can be checked and replaced with real records.

Run:  python src/generate_data.py      (writes CSVs to data/raw/)
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)
OUT = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

START, END = "2024-01-01", "2026-08-31"

# ---------------------------------------------------------------- varieties (real names)
# price_* = 2024 selling price per seedling (INR); seed_cost = cost per seed (INR). Assumed.
VARIETIES = [
    # id, crop, variety, brand, protray_price, bed_price, seed_cost, days_to_ready, weight_2024, weight_2026
    ("V01", "Chilli", "VNR 332 (Rani)", "VNR Seeds",       1.55, 1.10, 0.60, 32, 0.22, 0.18),
    ("V02", "Chilli", "VNR-38",         "VNR Seeds",       1.50, 1.05, 0.58, 32, 0.10, 0.09),
    ("V03", "Chilli", "US 1081",        "BASF Nunhems",    1.65, 1.15, 0.68, 33, 0.14, 0.12),
    ("V04", "Chilli", "Rise",           "BASF Nunhems",    1.70, 1.20, 0.70, 33, 0.02, 0.10),
    ("V05", "Chilli", "CCH-6300",       "HM Clause",       1.60, 1.12, 0.62, 32, 0.09, 0.08),
    ("V06", "Chilli", "CT-20",          "Kalash Seeds",    1.30, 0.90, 0.42, 31, 0.12, 0.09),
    ("V07", "Chilli", "Nisha",          "Thakar Seed",     1.25, 0.88, 0.40, 31, 0.13, 0.10),
    ("V08", "Chilli", "NS 1701 LG",     "Namdhari Seeds",  1.55, 1.10, 0.60, 32, 0.07, 0.08),
    ("V09", "Chilli", "HPH 789",        "Syngenta",        1.70, 1.20, 0.72, 33, 0.04, 0.12),
    ("V10", "Chilli", "Sitara",         "Other brands",    1.35, 0.95, 0.45, 31, 0.07, 0.04),
    ("V11", "Capsicum", "Indra",        "Syngenta",        3.20, 2.40, 1.90, 38, 1.00, 1.00),
    ("V12", "Tomato", "TO 1057",        "Syngenta",        1.80, 1.25, 0.85, 26, 1.00, 1.00),
    ("V13", "Brinjal", "F1 Brinjal (mixed brands)", "Various", 1.20, 0.80, 0.25, 30, 1.00, 1.00),
    ("V14", "Marigold", "NS 1503",      "Namdhari Seeds",  1.80, 1.30, 0.90, 25, 0.60, 0.50),
    ("V15", "Marigold", "Kavya",        "Kalash Seeds",    1.70, 1.25, 0.80, 25, 0.40, 0.50),
    ("V16", "Tobacco", "428",           "Local selection", None, 0.12, 0.002, 48, 1.00, 1.00),
]
var = pd.DataFrame(VARIETIES, columns=[
    "variety_id", "crop", "variety", "brand", "price_protray_2024", "price_bed_2024",
    "seed_cost_per_seed", "days_to_ready", "w2024", "w2026"])

# ---------------------------------------------------------------- demand assumptions
MONTH_W = {  # relative demand by month (Jan..Dec), Gujarat kharif/rabi calendar
    "Chilli":   [.30, .30, .40, .50, .90, 2.2, 2.8, 2.4, 1.4, .80, .50, .40],
    "Capsicum": [.20, .10, .10, .10, .20, .40, .80, 1.4, 1.3, .80, .30, .20],
    "Tomato":   [.40, .30, .30, .20, .30, .60, 1.1, 1.3, 1.1, 1.0, .90, .60],
    "Brinjal":  [.50, .50, .60, .50, .60, .90, 1.1, 1.0, .80, .80, .70, .60],
    "Marigold": [.30, .30, .20, .20, .30, .80, 1.6, 1.8, 1.0, .90, .50, .30],
    "Tobacco":  [0, 0, 0, 0, 0, .20, .90, 2.4, 1.9, .40, 0, 0],
}
BASE_ORDERS = {"Chilli": 3.0, "Capsicum": .6, "Tomato": 1.0, "Brinjal": .7, "Marigold": .9, "Tobacco": 1.2}
YEAR_GROWTH = {2024: 1.00, 2025: 1.17, 2026: 1.31}
PRICE_INFL = {2024: 1.00, 2025: 1.05, 2026: 1.10}
PROTRAY_SHARE = {  # share of orders taken as pro-tray seedlings
    "Chilli": {2024: .55, 2025: .65, 2026: .74}, "Capsicum": {2024: .92, 2025: .95, 2026: .97},
    "Tomato": {2024: .60, 2025: .68, 2026: .76}, "Brinjal": {2024: .45, 2025: .52, 2026: .60},
    "Marigold": {2024: .65, 2025: .72, 2026: .78}, "Tobacco": {2024: 0, 2025: 0, 2026: 0},
}
WHOLESALE_P = {"Chilli": .18, "Capsicum": .12, "Tomato": .12, "Brinjal": .10, "Marigold": .14, "Tobacco": .35}
GARDENER_P = {"Chilli": .05, "Capsicum": .04, "Tomato": .10, "Brinjal": .08, "Marigold": .12, "Tobacco": 0}
RETAIL_MEDIAN_QTY = {"Chilli": 1500, "Capsicum": 900, "Tomato": 1200, "Brinjal": 900, "Marigold": 1200, "Tobacco": 8000}

VILLAGES = {  # village: (weight, km from nursery, approx.)
    "Jesapura": (.08, 1), "Mithapura": (.08, 1), "Thasra": (.14, 9), "Dakor": (.12, 12),
    "Umreth": (.09, 22), "Sevalia": (.07, 18), "Kathlal": (.07, 35), "Mahudha": (.07, 30),
    "Nadiad": (.08, 38), "Kapadvanj": (.07, 40), "Balasinor": (.06, 28), "Anand": (.07, 42),
}
v_names = list(VILLAGES)
v_w = np.array([VILLAGES[v][0] for v in v_names]); v_w /= v_w.sum()

# ---------------------------------------------------------------- simulate orders
customers = []          # dicts
by_type = {"Retail farmer": [], "Wholesale / dealer": [], "Home gardener": []}
REPEAT_P = {"Retail farmer": .55, "Wholesale / dealer": .75, "Home gardener": .25}

def get_customer(ctype, date):
    pool = by_type[ctype]
    if pool and rng.random() < REPEAT_P[ctype]:
        return pool[rng.integers(len(pool))]
    cid = f"C{len(customers) + 1:04d}"
    village = rng.choice(v_names, p=v_w)
    customers.append({"customer_id": cid, "customer_type": ctype, "village": village,
                      "distance_km": VILLAGES[village][1], "first_order_date": date.date()})
    pool.append(cid)
    return cid

def variety_weights(crop, year):
    sub = var[var.crop == crop]
    t = {2024: 0, 2025: .5, 2026: 1}[year]
    w = (1 - t) * sub.w2024.values + t * sub.w2026.values
    return sub.variety_id.values, w / w.sum()

rows = []
for date in pd.date_range(START, END, freq="D"):
    y, m = date.year, date.month
    wk = 1.15 if date.dayofweek == 6 else 1.0
    for crop, base in BASE_ORDERS.items():
        lam = base * MONTH_W[crop][m - 1] * YEAR_GROWTH[y] * wk
        for _ in range(rng.poisson(lam)):
            r = rng.random()
            ctype = ("Wholesale / dealer" if r < WHOLESALE_P[crop]
                     else "Home gardener" if r < WHOLESALE_P[crop] + GARDENER_P[crop]
                     else "Retail farmer")
            ids, w = variety_weights(crop, y)
            vid = rng.choice(ids, p=w)
            vrow = var.set_index("variety_id").loc[vid]
            method = "Pro-tray" if rng.random() < PROTRAY_SHARE[crop][y] else "Nursery bed"
            if ctype == "Home gardener":
                qty = int(rng.integers(2, 21) * 10); method = "Pro-tray" if crop != "Tobacco" else method
            else:
                qty = rng.lognormal(np.log(RETAIL_MEDIAN_QTY[crop]), .55)
                if ctype == "Wholesale / dealer":
                    qty *= rng.uniform(3, 6)
                qty = int(max(100, round(qty / 100) * 100))
            base_price = vrow.price_protray_2024 if method == "Pro-tray" else vrow.price_bed_2024
            unit_price = round(base_price * PRICE_INFL[y] * rng.uniform(.97, 1.03), 2)
            if ctype == "Wholesale / dealer":
                disc = round(rng.uniform(8, 12), 1)
            elif qty >= 5000:
                disc = round(rng.uniform(0, 4), 1)
            else:
                disc = 0.0
            gross = qty * unit_price
            revenue = round(gross * (1 - disc / 100), 2)
            share_upi = {2024: .33, 2025: .42, 2026: .50}[y]
            credit = .35 if ctype == "Wholesale / dealer" else .12
            pay = rng.choice(["Cash", "UPI", "Credit"], p=[1 - share_upi - credit, share_upi, credit])
            wa = {2024: .14, 2025: .19, 2026: .26}[y]
            channel = rng.choice(["Walk-in", "Phone call", "WhatsApp"], p=[1 - .30 - wa, .30, wa])
            cid = get_customer(ctype, date)
            dist = next(c["distance_km"] for c in customers if c["customer_id"] == cid) if ctype != "Home gardener" else 5
            deliver_p = (.65 if qty >= 5000 else .12) * (1.2 if dist > 25 else 1)
            fulfilment = "Van delivery" if rng.random() < min(deliver_p, .95) else "Self pickup"
            rows.append([date.date(), cid, ctype, vid, crop, method, qty, unit_price, disc,
                         revenue, pay, channel, fulfilment])

orders = pd.DataFrame(rows, columns=[
    "order_date", "customer_id", "customer_type", "variety_id", "crop", "method", "quantity",
    "unit_price_inr", "discount_pct", "revenue_inr", "payment_mode", "channel", "fulfilment"])
orders.insert(0, "order_id", [f"O{i + 1:06d}" for i in range(len(orders))])

# ---------------------------------------------------------------- production batches
orders["sale_month"] = pd.to_datetime(orders.order_date).dt.to_period("M")
dem = orders.groupby(["variety_id", "method", "sale_month"], as_index=False).quantity.sum()
b = []
RAISE_COST = {"Pro-tray": .28, "Nursery bed": .08}   # cocopeat, trays, water, labour per seedling, 2024
for i, r in dem.iterrows():
    vrow = var.set_index("variety_id").loc[r.variety_id]
    germ = rng.uniform(.88, .95) if r.method == "Pro-tray" else rng.uniform(.72, .86)
    buffer = rng.uniform(1.05, 1.18)                  # planned over-production
    ready = int(np.ceil(r.quantity * buffer))
    sown = int(np.ceil(ready / germ))
    sale_start = r.sale_month.to_timestamp()
    sow = sale_start - pd.Timedelta(days=int(vrow.days_to_ready))
    yr = sale_start.year
    seed_cost = round(sown * vrow.seed_cost_per_seed, 2)
    raise_cost = round(ready * RAISE_COST[r.method] * (1 + .06 * (yr - 2024)), 2)
    b.append([f"B{i + 1:05d}", r.variety_id, r.method, sow.date(), sale_start.date(), sown, ready,
              int(r.quantity), ready - int(r.quantity), round(germ, 3), seed_cost, raise_cost])
batches = pd.DataFrame(b, columns=[
    "batch_id", "variety_id", "method", "sow_date", "ready_from", "seeds_sown", "seedlings_ready",
    "seedlings_sold", "seedlings_unsold", "germination_rate", "seed_cost_inr", "raising_cost_inr"])

orders = orders.drop(columns="sale_month")
cust = pd.DataFrame(customers)

var.drop(columns=["w2024", "w2026"]).to_csv(OUT / "varieties.csv", index=False)
cust.to_csv(OUT / "customers.csv", index=False)
orders.to_csv(OUT / "orders.csv", index=False)
batches.to_csv(OUT / "production_batches.csv", index=False)
print(f"orders {len(orders):,} | customers {len(cust):,} | batches {len(batches):,} | "
      f"revenue ₹{orders.revenue_inr.sum():,.0f}")

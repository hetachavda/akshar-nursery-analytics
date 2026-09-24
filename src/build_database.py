"""Load the CSVs in data/raw into a SQLite database (data/nursery.db).

Run:  python src/build_database.py
"""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DB = ROOT / "data" / "nursery.db"

SCHEMA = """
DROP TABLE IF EXISTS varieties;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS production_batches;

CREATE TABLE varieties (
    variety_id TEXT PRIMARY KEY, crop TEXT, variety TEXT, brand TEXT,
    price_protray_2024 REAL, price_bed_2024 REAL, seed_cost_per_seed REAL, days_to_ready INTEGER);

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY, customer_type TEXT, village TEXT,
    distance_km INTEGER, first_order_date TEXT);

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY, order_date TEXT, customer_id TEXT REFERENCES customers,
    customer_type TEXT, variety_id TEXT REFERENCES varieties, crop TEXT, method TEXT,
    quantity INTEGER, unit_price_inr REAL, discount_pct REAL, revenue_inr REAL,
    payment_mode TEXT, channel TEXT, fulfilment TEXT);

CREATE TABLE production_batches (
    batch_id TEXT PRIMARY KEY, variety_id TEXT REFERENCES varieties, method TEXT,
    sow_date TEXT, ready_from TEXT, seeds_sown INTEGER, seedlings_ready INTEGER,
    seedlings_sold INTEGER, seedlings_unsold INTEGER, germination_rate REAL,
    seed_cost_inr REAL, raising_cost_inr REAL);

CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_variety ON orders(variety_id, method);
CREATE INDEX idx_orders_customer ON orders(customer_id);
"""

def main():
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    for t in ["varieties", "customers", "orders", "production_batches"]:
        pd.read_csv(RAW / f"{t}.csv").to_sql(t, con, if_exists="append", index=False)
        n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t:<20} {n:>6,} rows")
    con.commit()
    con.close()
    print(f"Database written to {DB.relative_to(ROOT)}")

if __name__ == "__main__":
    main()

-- =====================================================================
-- Akshar Farm And Nursery: business questions answered in SQL (SQLite)
-- Database: data/nursery.db  (build with: python src/build_database.py)
-- Note: the transaction data is SIMULATED. See README.md.
-- =====================================================================

-- Q1. Monthly revenue with year-on-year growth for the same month
WITH monthly AS (
    SELECT strftime('%Y', order_date) AS yr,
           strftime('%m', order_date) AS mon,
           ROUND(SUM(revenue_inr), 0)  AS revenue
    FROM orders
    GROUP BY yr, mon
)
SELECT yr, mon, revenue,
       LAG(revenue) OVER (PARTITION BY mon ORDER BY yr) AS revenue_last_year,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (PARTITION BY mon ORDER BY yr))
             / LAG(revenue) OVER (PARTITION BY mon ORDER BY yr), 1) AS yoy_growth_pct
FROM monthly
ORDER BY yr, mon;

-- Q2. Revenue and seedlings sold by crop, with share of total
SELECT crop,
       ROUND(SUM(revenue_inr), 0)                                   AS revenue,
       SUM(quantity)                                                 AS seedlings_sold,
       ROUND(100.0 * SUM(revenue_inr) / (SELECT SUM(revenue_inr) FROM orders), 1) AS revenue_share_pct
FROM orders
GROUP BY crop
ORDER BY revenue DESC;

-- Q3. Variety ranking with cumulative revenue share (Pareto / 80-20 check)
WITH v AS (
    SELECT o.variety_id, va.crop, va.variety, va.brand, SUM(o.revenue_inr) AS revenue
    FROM orders o JOIN varieties va USING (variety_id)
    GROUP BY o.variety_id
)
SELECT RANK() OVER (ORDER BY revenue DESC) AS rnk, crop, variety, brand,
       ROUND(revenue, 0) AS revenue,
       ROUND(100.0 * SUM(revenue) OVER (ORDER BY revenue DESC) / SUM(revenue) OVER (), 1) AS cumulative_share_pct
FROM v
ORDER BY rnk;

-- Q4. Pro-tray adoption: share of seedlings sold as pro-tray, by crop and year
SELECT crop, strftime('%Y', order_date) AS yr,
       ROUND(100.0 * SUM(CASE WHEN method = 'Pro-tray' THEN quantity ELSE 0 END) / SUM(quantity), 1) AS protray_share_pct
FROM orders
WHERE crop <> 'Tobacco'
GROUP BY crop, yr
ORDER BY crop, yr;

-- Q5. Customer segments: orders, revenue share and average order value
SELECT customer_type,
       COUNT(*)                                   AS orders,
       COUNT(DISTINCT customer_id)                AS customers,
       ROUND(SUM(revenue_inr), 0)                 AS revenue,
       ROUND(100.0 * SUM(revenue_inr) / (SELECT SUM(revenue_inr) FROM orders), 1) AS revenue_share_pct,
       ROUND(AVG(revenue_inr), 0)                 AS avg_order_value
FROM orders
GROUP BY customer_type
ORDER BY revenue DESC;

-- Q6. Retention: of customers first seen in a year, how many bought again in a later year?
WITH first_year AS (
    SELECT customer_id, MIN(strftime('%Y', order_date)) AS cohort
    FROM orders GROUP BY customer_id
),
active AS (
    SELECT DISTINCT customer_id, strftime('%Y', order_date) AS yr FROM orders
)
SELECT f.cohort,
       COUNT(DISTINCT f.customer_id) AS new_customers,
       COUNT(DISTINCT CASE WHEN a.yr > f.cohort THEN f.customer_id END) AS returned_later,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN a.yr > f.cohort THEN f.customer_id END)
             / COUNT(DISTINCT f.customer_id), 1) AS return_rate_pct
FROM first_year f JOIN active a USING (customer_id)
GROUP BY f.cohort
ORDER BY f.cohort;

-- Q7. Geography: revenue by village, distance and share delivered by van
SELECT c.village, c.distance_km,
       ROUND(SUM(o.revenue_inr), 0) AS revenue,
       COUNT(*) AS orders,
       ROUND(100.0 * AVG(CASE WHEN o.fulfilment = 'Van delivery' THEN 1.0 ELSE 0 END), 1) AS van_delivery_pct
FROM orders o JOIN customers c USING (customer_id)
WHERE o.customer_type <> 'Home gardener'
GROUP BY c.village
ORDER BY revenue DESC;

-- Q8. Production efficiency: germination and unsold seedlings by crop and method
SELECT va.crop, b.method,
       ROUND(100.0 * SUM(b.seedlings_ready) / SUM(b.seeds_sown), 1)      AS germination_pct,
       ROUND(100.0 * SUM(b.seedlings_unsold) / SUM(b.seedlings_ready), 1) AS unsold_pct,
       SUM(b.seedlings_unsold)                                            AS seedlings_unsold
FROM production_batches b JOIN varieties va USING (variety_id)
GROUP BY va.crop, b.method
ORDER BY unsold_pct DESC;

-- Q9. Gross margin by variety and method (revenue minus seed and raising cost)
WITH rev AS (
    SELECT variety_id, method, SUM(revenue_inr) AS revenue, SUM(quantity) AS sold
    FROM orders GROUP BY variety_id, method
),
cost AS (
    SELECT variety_id, method, SUM(seed_cost_inr + raising_cost_inr) AS cost
    FROM production_batches GROUP BY variety_id, method
)
SELECT va.crop, va.variety, r.method,
       ROUND(r.revenue, 0)                              AS revenue,
       ROUND(c.cost, 0)                                 AS production_cost,
       ROUND(r.revenue - c.cost, 0)                     AS gross_profit,
       ROUND(100.0 * (r.revenue - c.cost) / r.revenue, 1) AS gross_margin_pct,
       ROUND((r.revenue - c.cost) / r.sold, 2)          AS profit_per_seedling
FROM rev r JOIN cost c USING (variety_id, method) JOIN varieties va USING (variety_id)
ORDER BY gross_profit DESC;

-- Q10. Credit exposure: share of revenue sold on credit, by year and customer type
SELECT strftime('%Y', order_date) AS yr, customer_type,
       ROUND(100.0 * SUM(CASE WHEN payment_mode = 'Credit' THEN revenue_inr ELSE 0 END) / SUM(revenue_inr), 1) AS credit_share_pct,
       ROUND(SUM(CASE WHEN payment_mode = 'Credit' THEN revenue_inr ELSE 0 END), 0) AS credit_revenue
FROM orders
GROUP BY yr, customer_type
ORDER BY yr, customer_type;

-- Q11. Busiest days of the week in peak season (June to September)
SELECT CASE strftime('%w', order_date)
         WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday'
         WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday' WHEN '5' THEN 'Friday'
         ELSE 'Saturday' END AS weekday,
       COUNT(*) AS orders,
       ROUND(1.0 * COUNT(*) / COUNT(DISTINCT order_date), 1) AS avg_orders_per_day
FROM orders
WHERE CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 6 AND 9
GROUP BY strftime('%w', order_date)
ORDER BY avg_orders_per_day DESC;

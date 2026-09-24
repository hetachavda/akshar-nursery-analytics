# Data dictionary

All money is in Indian rupees (INR). Dates are `YYYY-MM-DD`.

## orders (`data/raw/orders.csv`)
| Column | Type | Description |
|---|---|---|
| order_id | text | Unique order ID, e.g. `O000123` |
| order_date | date | Day the seedlings were sold |
| customer_id | text | Links to `customers.customer_id` |
| customer_type | text | `Retail farmer`, `Wholesale / dealer` or `Home gardener` |
| variety_id | text | Links to `varieties.variety_id` |
| crop | text | Chilli, Capsicum, Tomato, Brinjal, Marigold, Tobacco |
| method | text | `Pro-tray` (plastic cell trays with cocopeat) or `Nursery bed` (soil-raised) |
| quantity | integer | Number of seedlings sold |
| unit_price_inr | decimal | Price per seedling before discount |
| discount_pct | decimal | Discount given, in percent |
| revenue_inr | decimal | quantity × unit_price × (1 − discount/100) |
| payment_mode | text | Cash, UPI or Credit |
| channel | text | How the order came in: Walk-in, Phone call, WhatsApp |
| fulfilment | text | Self pickup or Van delivery |

## customers (`data/raw/customers.csv`)
| Column | Type | Description |
|---|---|---|
| customer_id | text | Unique customer ID |
| customer_type | text | As in orders |
| village | text | Customer's village or town |
| distance_km | integer | Approximate road distance from the nursery |
| first_order_date | date | Date of first purchase |

## varieties (`data/raw/varieties.csv`)
| Column | Type | Description |
|---|---|---|
| variety_id | text | Unique variety ID |
| crop | text | Crop |
| variety | text | Seed variety name (real, from seed packets at the nursery) |
| brand | text | Seed company |
| price_protray_2024 | decimal | Assumed 2024 price per pro-tray seedling (blank = not sold as pro-tray) |
| price_bed_2024 | decimal | Assumed 2024 price per nursery-bed seedling |
| seed_cost_per_seed | decimal | Assumed cost of one seed |
| days_to_ready | integer | Days from sowing until the seedling is ready to sell |

## production_batches (`data/raw/production_batches.csv`)
| Column | Type | Description |
|---|---|---|
| batch_id | text | Unique batch ID |
| variety_id | text | Links to `varieties` |
| method | text | Pro-tray or Nursery bed |
| sow_date | date | Sowing date |
| ready_from | date | First day of the month the batch was sold in |
| seeds_sown | integer | Seeds sown |
| seedlings_ready | integer | Healthy seedlings produced |
| seedlings_sold | integer | Seedlings sold from this batch |
| seedlings_unsold | integer | seedlings_ready − seedlings_sold |
| germination_rate | decimal | seedlings_ready ÷ seeds_sown |
| seed_cost_inr | decimal | seeds_sown × seed_cost_per_seed |
| raising_cost_inr | decimal | Cocopeat, trays, water and labour for the batch |

## Real data template (`data/templates/daily_sales_log_template.csv`)
One row per sale, filled in at the counter or from WhatsApp orders. `customer_phone` becomes the customer ID
(stored hashed or masked before sharing the data publicly).

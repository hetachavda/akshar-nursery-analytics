# Simulation assumptions

The nursery keeps paper records, so the transaction data in this project is **simulated**. These are the
assumptions behind it, set in [`src/generate_data.py`](../src/generate_data.py). They are reasoned estimates for
a nursery in Kheda district, not the owner's actual figures, and should be replaced with real records.

## What is real
- The business: Akshar Farm And Nursery, Jesapura Mithapura, Ta. Thasra, Dist. Kheda, Gujarat
- Crops raised: chilli, capsicum, tomato, brinjal, marigold, tobacco
- Seed varieties and brands (from seed packets photographed in the nursery)
- Methods: plastic pro-trays with cocopeat, and nursery beds; polyhouse, shade-net tunnels, sprinkler beds
- Opening hours (6 AM to 7 PM, every day) and nearby villages

## Prices and costs (2024 values)
| crop     | variety                   | brand           |   Pro-tray ₹/seedling |   Bed ₹/seedling |   Seed ₹/seed |   Days to ready |
|:---------|:--------------------------|:----------------|----------------------:|-----------------:|--------------:|----------------:|
| Chilli   | VNR 332 (Rani)            | VNR Seeds       |                  1.55 |             1.1  |         0.6   |              32 |
| Chilli   | VNR-38                    | VNR Seeds       |                  1.5  |             1.05 |         0.58  |              32 |
| Chilli   | US 1081                   | BASF Nunhems    |                  1.65 |             1.15 |         0.68  |              33 |
| Chilli   | Rise                      | BASF Nunhems    |                  1.7  |             1.2  |         0.7   |              33 |
| Chilli   | CCH-6300                  | HM Clause       |                  1.6  |             1.12 |         0.62  |              32 |
| Chilli   | CT-20                     | Kalash Seeds    |                  1.3  |             0.9  |         0.42  |              31 |
| Chilli   | Nisha                     | Thakar Seed     |                  1.25 |             0.88 |         0.4   |              31 |
| Chilli   | NS 1701 LG                | Namdhari Seeds  |                  1.55 |             1.1  |         0.6   |              32 |
| Chilli   | HPH 789                   | Syngenta        |                  1.7  |             1.2  |         0.72  |              33 |
| Chilli   | Sitara                    | Other brands    |                  1.35 |             0.95 |         0.45  |              31 |
| Capsicum | Indra                     | Syngenta        |                  3.2  |             2.4  |         1.9   |              38 |
| Tomato   | TO 1057                   | Syngenta        |                  1.8  |             1.25 |         0.85  |              26 |
| Brinjal  | F1 Brinjal (mixed brands) | Various         |                  1.2  |             0.8  |         0.25  |              30 |
| Marigold | NS 1503                   | Namdhari Seeds  |                  1.8  |             1.3  |         0.9   |              25 |
| Marigold | Kavya                     | Kalash Seeds    |                  1.7  |             1.25 |         0.8   |              25 |
| Tobacco  | 428                       | Local selection |                       |             0.12 |         0.002 |              48 |

- Prices rise 5% a year (2025) and 10% over 2024 (2026).
- Raising cost per seedling ready: ₹0.28 pro-tray, ₹0.08 nursery bed, rising 6% a year.
- Wholesale / dealer orders get 8 to 12% discount; large retail orders (5,000+) get up to 4%.

## Demand
- Seasonality follows the Gujarat kharif and rabi calendar: chilli peaks June to August, tobacco August to
  September, marigold July to August (festival season), tomato and brinjal spread across the year.
- Order volume grows 17% in 2025 and 31% over 2024 in 2026.
- Pro-tray share of orders grows each year (e.g. chilli 55% → 65% → 74% of orders); tobacco is bed-only.
- Customer mix per crop: 10 to 35% dealer orders, up to 12% home gardeners, the rest retail farmers.
- Returning customers: 55% of retail orders, 75% of dealer orders and 25% of gardener orders come from
  existing customers.

## Production
- Germination: 88 to 95% in pro-trays, 72 to 86% in nursery beds.
- The nursery sows 5 to 18% more than expected demand as a safety buffer; the excess is unsold.

## Payments and channels
- UPI share of orders grows from 33% (2024) to 50% (2026). Credit: 35% of dealer orders, 12% of others.
- WhatsApp orders grow from 14% to 26%; phone calls stay near 30%; the rest are walk-ins.

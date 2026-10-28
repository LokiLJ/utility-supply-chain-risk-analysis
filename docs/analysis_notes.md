# Analysis notes

## Decision insight

The analysis connects two procurement questions: **where is the financial exposure, and which equipment needs operational attention first?** These do not produce identical priorities. Meters ranks highest in the original category score, while selected switchgear records show much larger inventory coverage gaps. Reading the views together supports a staged response instead of treating one ranking as the answer to every decision.

This visual portfolio presents historical coursework and its analytical findings. It is not a current forecast of BC Hydro's procurement costs or operating conditions.

## Approach

The original notebook combined inventory, vendor, category-spending, risk-tolerance, trade, and logistics tables. It summarized 291 inventory records and 3,213 vendor-table records; these are supplied record counts, not a census of distinct suppliers or the utility's full inventory.

**Inventory coverage.** The analysis used Days of Supply (DoS) and average replenishment lead time (LT):

```text
Coverage ratio = DoS / LT
Coverage gap   = DoS − LT
Coverage flag  = DoS < LT
Lead-time CV   = lead-time standard deviation / LT
```

The screen flagged 40 records overall, including six of the 24 U.S.-origin records. A negative gap identifies prospective coverage pressure if replenishment takes the average lead time; it does not establish an actual stockout. Purchase-order arrival dates and inventory commitments would be needed for an operational decision. Safety-stock and reorder-point values were supplied in the workbook, rather than estimated independently from demand histories.

**Tariff scenario.** The original analysis used a 35% historical scenario assumption:

```text
Estimated annual exposure = category annual spend
                          × U.S.-origin inventory-record share
                          × 35%
```

This produced approximately **CAD 70.7 million**. Inventory-record share serves as a proxy for exposed spending, with unchanged purchasing and full tariff pass-through assumed. The result is a scenario estimate, not an actual tariff bill, a savings estimate, or a statement of current tariff policy.

**Composite Vulnerability Score.** The exploratory score combined U.S.-origin record share (25%), risk-tolerance coding (25%), normalized coverage (20%), the presence of a flagged U.S.-origin record (15%), and normalized average lead time (15%). These were judgmental weights used to organize priorities. Scores are not probabilities of disruption, and the qualitative response matrix reflects analytical judgment rather than measured adjustment costs.

## Response sequence

- **Near term:** review flagged items, confirm inbound orders and operational needs, and investigate ways to close coverage gaps.
- **Medium term:** qualify alternative suppliers against specifications, delivery capability, performance, and landed cost; consider parallel sourcing where feasible.
- **Long term:** strengthen sourcing diversity and inventory visibility for critical equipment categories.

Country-level indicators offer context, not supplier qualification. The original foreign-country MFN tariff and border-logistics comparisons are excluded from the featured figures because they do not directly measure the cost or delivery performance of sourcing those goods into Canada.

## Origin and contribution

This project was completed for **MMA 608 — Business Applications of AI (Operations and Supply Chain)** at the University of Alberta. The original group report, dated March 25, 2026, lists **Miao Jiang, Tong Xiao, and Wenchuan Zhu**. **My role was the analysis.**

The coursework used the Ivey case [*BC Hydro: Navigating Supply Chain Uncertainty amid Tariffs*](https://www.iveypublishing.ca/s/product/bc-hydro-navigating-supply-chain-uncertainty-amid-tariffs/01tOF00000BWq3ZYAT), by Michael Johnson, Jason Ho, and Kelley Hishon, product W47404. The public repository presents analysis and visual explanations; it does not redistribute the case text, source workbook, or teaching note.

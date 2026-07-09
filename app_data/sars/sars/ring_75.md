# SAR draft — Ring 75
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:40:36.987429+00:00 by qwen/qwen3-32b

- Accounts: 15  ·  Transactions: 14  ·  Total: $129,347
- Window: 2022-09-02 08:05:00 → 2022-09-10 16:50:00
- Detected typology: **GATHER-SCATTER** (confidence 0.99)
- Recommendation: **file_sar**

## Summary
Funds concentrated into hub account 23289_808839F70 ($15,521.59 inflow) then dispersed to 8 accounts ($18,532.14–$857.60) within 8 days. High GNN score (0.9887) confirms suspicious structure.

## Key evidence
- Hub account 23289_808839F70 received $15,521.59 from 228101_80A48A710
- Hub dispersed $18,532.14 to 8771_80D1AC960 and $17,519.79 to 8888_80514F5E0
- 14 transactions occurred across 15 accounts in 8-day window
- GNN score 0.9887 exceeds 99th percentile for suspiciousness

## Full narrative
```json
{
  "typology": "GATHER-SCATTER",
  "confidence": 0.99,
  "summary": "Funds concentrated into hub account 23289_808839F70 ($15,521.59 inflow) then dispersed to 8 accounts ($18,532.14–$857.60) within 8 days. High GNN score (0.9887) confirms suspicious structure.",
  "key_evidence": [
    "Hub account 23289_808839F70 received $15,521.59 from 228101_80A48A710",
    "Hub dispersed $18,532.14 to 8771_80D1AC960 and $17,519.79 to 8888_80514F5E0",
    "14 transactions occurred across 15 accounts in 8-day window",
    "GNN score 0.9887 exceeds 99th percentile for suspiciousness"
  ],
  "recommendation": "file_sar"
}
```
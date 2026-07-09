# SAR draft — Ring 72
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:37:43.501377+00:00 by qwen/qwen3-32b

- Accounts: 15  ·  Transactions: 14  ·  Total: $101,466
- Window: 2022-09-11 20:33:00 → 2022-09-18 09:55:00
- Detected typology: **GATHER-SCATTER** (confidence 0.99)
- Recommendation: **file_sar**

## Summary
Funds concentrate into hub account 29404_8041A3440 before dispersing to 12 counterparties. The hub simultaneously receives inflows from external accounts, showing dual role in aggregation and distribution.

## Key evidence
- Hub account 29404_8041A3440 received $12,641.75 from 39668_80F1F4BD0
- Hub dispersed $15,918.17 to 20248_80EBC6500 and $12,994.92 to 18049_80E3027B0 in single transactions
- 14 total transactions occurred within 6-day window (Sep 11-18 2022) across 15 accounts
- Mean GNN suspicion score of 0.9998 indicates strong structural abnormality

## Full narrative
```json
{
  "typology": "GATHER-SCATTER",
  "confidence": 0.99,
  "summary": "Funds concentrate into hub account 29404_8041A3440 before dispersing to 12 counterparties. The hub simultaneously receives inflows from external accounts, showing dual role in aggregation and distribution.",
  "key_evidence": [
    "Hub account 29404_8041A3440 received $12,641.75 from 39668_80F1F4BD0",
    "Hub dispersed $15,918.17 to 20248_80EBC6500 and $12,994.92 to 18049_80E3027B0 in single transactions",
    "14 total transactions occurred within 6-day window (Sep 11-18 2022) across 15 accounts",
    "Mean GNN suspicion score of 0.9998 indicates strong structural abnormality"
  ],
  "recommendation": "file_sar"
}
```
# SAR draft — Ring 92
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:39:47.983537+00:00 by qwen/qwen3-32b

- Accounts: 14  ·  Transactions: 13  ·  Total: $149,135
- Window: 2022-09-06 08:52:00 → 2022-09-14 14:26:00
- Detected typology: **GATHER-SCATTER** (confidence 0.99)
- Recommendation: **file_sar**

## Summary
Funds consolidate into hub account 19329_808B1C350 from 12 sources before dispersing to 7 destinations. The $149,134.59 moved across USD/EUR/AUD in 8 days shows rapid aggregation and distribution through a central node.

## Key evidence
- Hub account 19329_808B1C350 receives $83,340.53 from 12 accounts (e.g., $18,336.63 from 12004_801C152A0)
- Same hub disperses $83,340.53 to 7 accounts (e.g., $19,551.02 to 1412_809F49D20)
- All transactions occur within 8-day window (Sep 6-14 2022) via ACH format
- High GNN score of 0.9906 indicates strong structural suspiciousness

## Full narrative
```json
{
  "typology": "GATHER-SCATTER",
  "confidence": 0.99,
  "summary": "Funds consolidate into hub account 19329_808B1C350 from 12 sources before dispersing to 7 destinations. The $149,134.59 moved across USD/EUR/AUD in 8 days shows rapid aggregation and distribution through a central node.",
  "key_evidence": [
    "Hub account 19329_808B1C350 receives $83,340.53 from 12 accounts (e.g., $18,336.63 from 12004_801C152A0)",
    "Same hub disperses $83,340.53 to 7 accounts (e.g., $19,551.02 to 1412_809F49D20)",
    "All transactions occur within 8-day window (Sep 6-14 2022) via ACH format",
    "High GNN score of 0.9906 indicates strong structural suspiciousness"
  ],
  "recommendation": "file_sar"
}
```
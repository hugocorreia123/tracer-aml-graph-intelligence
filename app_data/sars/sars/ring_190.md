# SAR draft — Ring 190
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:59:29.781699+00:00 by qwen/qwen3-32b

- Accounts: 11  ·  Transactions: 19  ·  Total: $65,813
- Window: 2022-09-01 15:37:00 → 2022-09-12 14:43:00
- Detected typology: **GATHER-SCATTER** (confidence 0.95)
- Recommendation: **file_sar**

## Summary
Funds concentrate into central account 231212_80ED002D0 via multiple inflows (e.g., 28183_80A5253A0: €11,477.47) before dispersing to 8 distinct accounts in 12 days, with largest outflow of $11,734.77 to 31208_80FB8A6A0.

## Key evidence
- Account 231212_80ED002D0 receives 7 transactions totaling €11,477.47 from 28183_80A5253A0
- Central account 231212_80ED002D0 disperses to 8 unique recipients ($7,054.22 to 110_80CCC00B0, $6,461.40 to 29715_80CB11750)
- No detectable cycles in 19 transactions over 12-day window
- High GNN score of 0.9924 indicates strong structural abnormality

## Full narrative
```json
{
  "typology": "GATHER-SCATTER",
  "confidence": 0.95,
  "summary": "Funds concentrate into central account 231212_80ED002D0 via multiple inflows (e.g., 28183_80A5253A0: €11,477.47) before dispersing to 8 distinct accounts in 12 days, with largest outflow of $11,734.77 to 31208_80FB8A6A0.",
  "key_evidence": [
    "Account 231212_80ED002D0 receives 7 transactions totaling €11,477.47 from 28183_80A5253A0",
    "Central account 231212_80ED002D0 disperses to 8 unique recipients ($7,054.22 to 110_80CCC00B0, $6,461.40 to 29715_80CB11750)",
    "No detectable cycles in 19 transactions over 12-day window",
    "High GNN score of 0.9924 indicates strong structural abnormality"
  ],
  "recommendation": "file_sar"
}
```
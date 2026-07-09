# SAR draft — Ring 119
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:57:35.566048+00:00 by qwen/qwen3-32b

- Accounts: 13  ·  Transactions: 48  ·  Total: $9,115,989
- Window: 2022-09-01 00:03:00 → 2022-09-12 09:18:00
- Detected typology: **FAN-IN** (confidence 0.92)
- Recommendation: **file_sar**

## Summary
This ring exhibits a clear FAN-IN structure where 9 accounts funnel funds into account 17863_810C289B0, which receives 90% of all incoming transactions. The largest single flow (€8.99M) moves from 3242_80BECDBF0 to 228540_810E62EB0 before cascading into the central hub.

## Key evidence
- Account 17863_810C289B0 receives 9/12 total incoming transactions (in_deg=9)
- €8.99M transferred from 3242_80BECDBF0 to 228540_810E62EB0 (10x transactions)
- 12 accounts send funds to central account 17863_810C289B0 across 11 separate flows
- High GNN score of 0.895 for 13-account ring with €9.11M total volume in 12 days

## Full narrative
```json
{
  "typology": "FAN-IN",
  "confidence": 0.92,
  "summary": "This ring exhibits a clear FAN-IN structure where 9 accounts funnel funds into account 17863_810C289B0, which receives 90% of all incoming transactions. The largest single flow (€8.99M) moves from 3242_80BECDBF0 to 228540_810E62EB0 before cascading into the central hub.",
  "key_evidence": [
    "Account 17863_810C289B0 receives 9/12 total incoming transactions (in_deg=9)",
    "€8.99M transferred from 3242_80BECDBF0 to 228540_810E62EB0 (10x transactions)",
    "12 accounts send funds to central account 17863_810C289B0 across 11 separate flows",
    "High GNN score of 0.895 for 13-account ring with €9.11M total volume in 12 days"
  ],
  "recommendation": "file_sar"
}
```
# SAR draft — Ring 68
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T03:05:46.350751+00:00 by qwen/qwen3-32b

- Accounts: 15  ·  Transactions: 59  ·  Total: $2,807,834
- Window: 2022-09-01 00:13:00 → 2022-09-10 14:24:00
- Detected typology: **GATHER-SCATTER** (confidence 0.88)
- Recommendation: **file_sar**

## Summary
Funds concentrate into hub account 111141_80C5219E0 (8 inflows) before dispersing via primary distributor 18196_80B1BF360 (11 outflows). The ring moved $2.8M across 5 currencies in 10 days through layered transactions.

## Key evidence
- Account 18196_80B1BF360 sent $2.55M to 34828_80EF9A260 (14 txns)
- Hub account 111141_80C5219E0 received 8 inflows from 7 distinct senders
- Distributor 18196_80B1BF360 made 11 outgoing payments to 10 accounts
- Total network velocity: $2.8M moved in 10 days (avg $280K/day)
- No cycles detected but 11/15 accounts have zero-degree in/out patterns

## Full narrative
```json
{
  "typology": "GATHER-SCATTER",
  "confidence": 0.88,
  "summary": "Funds concentrate into hub account 111141_80C5219E0 (8 inflows) before dispersing via primary distributor 18196_80B1BF360 (11 outflows). The ring moved $2.8M across 5 currencies in 10 days through layered transactions.",
  "key_evidence": [
    "Account 18196_80B1BF360 sent $2.55M to 34828_80EF9A260 (14 txns)",
    "Hub account 111141_80C5219E0 received 8 inflows from 7 distinct senders",
    "Distributor 18196_80B1BF360 made 11 outgoing payments to 10 accounts",
    "Total network velocity: $2.8M moved in 10 days (avg $280K/day)",
    "No cycles detected but 11/15 accounts have zero-degree in/out patterns"
  ],
  "recommendation": "file_sar"
}
```
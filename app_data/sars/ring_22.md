# SAR draft — Ring 22
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T03:08:44.559430+00:00 by qwen/qwen3-32b

- Accounts: 24  ·  Transactions: 81  ·  Total: $239,810,261
- Window: 2022-09-01 00:32:00 → 2022-09-09 11:13:00
- Detected typology: **FAN-OUT / FAN-IN** (confidence 0.85)
- Recommendation: **file_sar**

## Summary
A single account (213952_808338D40) dispersed $238.6M across 15 recipients within 9 days, while account 26442_80AEBECB0 received funds from 13 distinct sources. The structure shows concentrated inflows/outflows with no clear re-gathering or layering patterns.

## Key evidence
- Account 213952_808338D40 sent $238.6M to 15+ accounts (7 transactions to 31596_80C11BB10 alone)
- Account 26442_80AEBECB0 received $1.1M from 13 different senders
- 81 transactions used 7+ currencies and 4 payment formats in 9 days
- No cycles detected but 15 accounts have zero in-degree/out-degree

## Full narrative
```json
{
  "typology": "FAN-OUT / FAN-IN",
  "confidence": 0.85,
  "summary": "A single account (213952_808338D40) dispersed $238.6M across 15 recipients within 9 days, while account 26442_80AEBECB0 received funds from 13 distinct sources. The structure shows concentrated inflows/outflows with no clear re-gathering or layering patterns.",
  "key_evidence": [
    "Account 213952_808338D40 sent $238.6M to 15+ accounts (7 transactions to 31596_80C11BB10 alone)",
    "Account 26442_80AEBECB0 received $1.1M from 13 different senders",
    "81 transactions used 7+ currencies and 4 payment formats in 9 days",
    "No cycles detected but 15 accounts have zero in-degree/out-degree"
  ],
  "recommendation": "file_sar"
}
```
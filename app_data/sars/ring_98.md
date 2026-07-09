# SAR draft — Ring 98
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T03:07:14.959854+00:00 by qwen/qwen3-32b

- Accounts: 14  ·  Transactions: 25  ·  Total: $97,877,339
- Window: 2022-09-04 22:27:00 → 2022-09-08 15:22:00
- Detected typology: **FAN-IN** (confidence 0.92)
- Recommendation: **file_sar**

## Summary
Funds from 9 distinct accounts are funneled into a central account (222664_80D7EC5F0) over 4 days, with the largest inflow of $32.3M from 123390_811006A00. The structure shows no outgoing transactions from this hub, suggesting consolidation before potential layering.

## Key evidence
- Account 222664_80D7EC5F0 receives $32.3M from 123390_811006A00 and $14.4M from 113865_809326EF0
- Central account 222664_80D7EC5F0 has 9 incoming connections but 0 outgoing transactions
- High GNN suspicion score (0.896) for $97.9M concentrated in 4 days

## Full narrative
```json
{
  "typology": "FAN-IN",
  "confidence": 0.92,
  "summary": "Funds from 9 distinct accounts are funneled into a central account (222664_80D7EC5F0) over 4 days, with the largest inflow of $32.3M from 123390_811006A00. The structure shows no outgoing transactions from this hub, suggesting consolidation before potential layering.",
  "key_evidence": [
    "Account 222664_80D7EC5F0 receives $32.3M from 123390_811006A00 and $14.4M from 113865_809326EF0",
    "Central account 222664_80D7EC5F0 has 9 incoming connections but 0 outgoing transactions",
    "High GNN suspicion score (0.896) for $97.9M concentrated in 4 days"
  ],
  "recommendation": "file_sar"
}
```
# SAR draft — Ring 62
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T03:01:53.011816+00:00 by qwen/qwen3-32b

- Accounts: 16  ·  Transactions: 54  ·  Total: $123,877
- Window: 2022-09-01 15:05:00 → 2022-09-10 18:25:00
- Detected typology: **FAN-OUT** (confidence 0.91)
- Recommendation: **file_sar**

## Summary
A single account (9679_80452D470) rapidly dispersed funds to 14 distinct accounts over 9 days, with 40 transactions concentrated to one recipient (19925_8145B2B90). The structure shows no recirculation or layered flows.

## Key evidence
- Account 9679_80452D470 sent to 14 unique accounts (out_deg=14)
- 40 transactions to 19925_8145B2B90 totaling $3,175.01
- All recipients have zero outgoing transactions within the ring

## Full narrative
```json
{
  "typology": "FAN-OUT",
  "confidence": 0.91,
  "summary": "A single account (9679_80452D470) rapidly dispersed funds to 14 distinct accounts over 9 days, with 40 transactions concentrated to one recipient (19925_8145B2B90). The structure shows no recirculation or layered flows.",
  "key_evidence": [
    "Account 9679_80452D470 sent to 14 unique accounts (out_deg=14)",
    "40 transactions to 19925_8145B2B90 totaling $3,175.01",
    "All recipients have zero outgoing transactions within the ring"
  ],
  "recommendation": "file_sar"
}
```
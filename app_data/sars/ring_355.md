# SAR draft — Ring 355
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:55:08.556761+00:00 by qwen/qwen3-32b

- Accounts: 8  ·  Transactions: 67  ·  Total: $396,783,230
- Window: 2022-09-01 04:31:00 → 2022-09-10 12:08:00
- Detected typology: **CYCLE** (confidence 0.92)
- Recommendation: **file_sar**

## Summary
Funds flow in a directed cycle among three accounts (111312_8045732A0 → 14_81016E050 → 32564_80C1EB8B0 → 111312_8045732A0) while a single account (4600_806511B40) funnels ~$396M into the ring. The 10-day window shows layered transactions across 4 currencies and 5 payment formats.

## Key evidence
- Cycle detected: 111312_8045732A0 → 14_81016E050 → 32564_80C1EB8B0 → 111312_8045732A0
- $396.7M injected into 113935_8077C0760 from 4600_806511B40 (28 transactions)
- 32564_80C1EB8B0 recirculates funds to 214_80C1ED8D0 ($5,788.74) and 111312_8045732A0 ($4,560.49)

## Full narrative
```json
{
  "typology": "CYCLE",
  "confidence": 0.92,
  "summary": "Funds flow in a directed cycle among three accounts (111312_8045732A0 → 14_81016E050 → 32564_80C1EB8B0 → 111312_8045732A0) while a single account (4600_806511B40) funnels ~$396M into the ring. The 10-day window shows layered transactions across 4 currencies and 5 payment formats.",
  "key_evidence": [
    "Cycle detected: 111312_8045732A0 → 14_81016E050 → 32564_80C1EB8B0 → 111312_8045732A0",
    "$396.7M injected into 113935_8077C0760 from 4600_806511B40 (28 transactions)",
    "32564_80C1EB8B0 recirculates funds to 214_80C1ED8D0 ($5,788.74) and 111312_8045732A0 ($4,560.49)"
  ],
  "recommendation": "file_sar"
}
```
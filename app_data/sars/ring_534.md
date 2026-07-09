# SAR draft — Ring 534
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T03:04:30.502849+00:00 by qwen/qwen3-32b

- Accounts: 7  ·  Transactions: 38  ·  Total: $115,781,221
- Window: 2022-09-01 20:11:00 → 2022-09-10 16:58:00
- Detected typology: **FAN-OUT** (confidence 0.85)
- Recommendation: **file_sar**

## Summary
Account 1_800C15DD0 rapidly dispersed $85.5M across 3 accounts (23_801FFD3E0, 1241_80121F600, 228321_80B47E690) within 10 days. Two accounts (29788_80B92D990, 13067_809888C90) acted as intermediaries in $60M+ transfers. No cycles detected, but high-velocity fund dispersion matches AML typology for layering.

## Key evidence
- Account 1_800C15DD0 sent $55.1M to 3 distinct accounts in 38 transactions
- $30M+ transfers between 29788_80B92D990 and 1_800C15DD0 in 2 days
- 23_801FFD3E0 received $28.6M then sent $26.9M to 35655_80D3B56B0
- Total ring volume ($115.8M) exceeds 10x AML threshold in <1 week

## Full narrative
```json
{
  "typology": "FAN-OUT",
  "confidence": 0.85,
  "summary": "Account 1_800C15DD0 rapidly dispersed $85.5M across 3 accounts (23_801FFD3E0, 1241_80121F600, 228321_80B47E690) within 10 days. Two accounts (29788_80B92D990, 13067_809888C90) acted as intermediaries in $60M+ transfers. No cycles detected, but high-velocity fund dispersion matches AML typology for layering.",
  "key_evidence": [
    "Account 1_800C15DD0 sent $55.1M to 3 distinct accounts in 38 transactions",
    "$30M+ transfers between 29788_80B92D990 and 1_800C15DD0 in 2 days",
    "23_801FFD3E0 received $28.6M then sent $26.9M to 35655_80D3B56B0",
    "Total ring volume ($115.8M) exceeds 10x AML threshold in <1 week"
  ],
  "recommendation": "file_sar"
}
```
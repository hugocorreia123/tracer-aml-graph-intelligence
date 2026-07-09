# SAR draft — Ring 10
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:50:31.306622+00:00 by qwen/qwen3-32b

- Accounts: 29  ·  Transactions: 169  ·  Total: $53,984,228
- Window: 2022-09-01 03:12:00 → 2022-09-13 17:59:00
- Detected typology: **CYCLE** (confidence 0.92)
- Recommendation: **file_sar**

## Summary
Funds exhibit layered cycling through multiple accounts, with 3 distinct cycles involving accounts like 119_81235E8B0, 148389_811EDAA30, and 48308_811ED7DF0. High-value transactions (e.g., $23.7M from 48308_811EDA7A0 to 251264_812D1B280) rapidly recirculate through 5-6 accounts before returning to originators.

## Key evidence
- 3 directed cycles involving 5-6 accounts each (e.g., 119_81235E8B0 → 148389_811EDAA30 → 223_811EDA940 → 48308_811ED7DF0 → 48309_81235EAA0 → 119_81235E8B0)
- $23.7M transferred from 48308_811EDA7A0 to 251264_812D1B280 then $19.4M to 119_81235E8B0 within 2 days
- Account 48308_811ED7DF0 receives 15 incoming edges but only 2 outgoing, acting as a central collection point
- 12/29 accounts have out_deg ≥ 3 while only 3 accounts have in_deg ≥ 12, showing asymmetric flow distribution

## Full narrative
```json
{
  "typology": "CYCLE",
  "confidence": 0.92,
  "summary": "Funds exhibit layered cycling through multiple accounts, with 3 distinct cycles involving accounts like 119_81235E8B0, 148389_811EDAA30, and 48308_811ED7DF0. High-value transactions (e.g., $23.7M from 48308_811EDA7A0 to 251264_812D1B280) rapidly recirculate through 5-6 accounts before returning to originators.",
  "key_evidence": [
    "3 directed cycles involving 5-6 accounts each (e.g., 119_81235E8B0 → 148389_811EDAA30 → 223_811EDA940 → 48308_811ED7DF0 → 48309_81235EAA0 → 119_81235E8B0)",
    "$23.7M transferred from 48308_811EDA7A0 to 251264_812D1B280 then $19.4M to 119_81235E8B0 within 2 days",
    "Account 48308_811ED7DF0 receives 15 incoming edges but only 2 outgoing, acting as a central collection point",
    "12/29 accounts have out_deg ≥ 3 while only 3 accounts have in_deg ≥ 12, showing asymmetric flow distribution"
  ],
  "recommendation": "file_sar"
}
```
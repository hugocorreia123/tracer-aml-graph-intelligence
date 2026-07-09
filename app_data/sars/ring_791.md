# SAR draft — Ring 791
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:51:00.153607+00:00 by qwen/qwen3-32b

- Accounts: 5  ·  Transactions: 34  ·  Total: $135,865
- Window: 2022-09-01 13:36:00 → 2022-09-10 13:24:00
- Detected typology: **FAN-OUT** (confidence 0.65)
- Recommendation: **monitor**

## Summary
Account 119_8100C5CC0 dispersed funds to three distinct accounts (43460_810140DB0, 45000_810C52B80, 130596_80B586630) via 28 transactions totaling $15,914.79. The largest single flow ($130,632.72) moved from 43049_80FDBE970 to 43460_810140DB0.

## Key evidence
- 119_8100C5CC0 sent $2,214.79 to 43460_810140DB0 (20 txns)
- 43049_80FDBE970 sent $130,632.72 to 43460_810140DB0 (6 txns)
- No cycles detected in 10-day window

## Full narrative
```json
{
  "typology": "FAN-OUT",
  "confidence": 0.65,
  "summary": "Account 119_8100C5CC0 dispersed funds to three distinct accounts (43460_810140DB0, 45000_810C52B80, 130596_80B586630) via 28 transactions totaling $15,914.79. The largest single flow ($130,632.72) moved from 43049_80FDBE970 to 43460_810140DB0.",
  "key_evidence": [
    "119_8100C5CC0 sent $2,214.79 to 43460_810140DB0 (20 txns)",
    "43049_80FDBE970 sent $130,632.72 to 43460_810140DB0 (6 txns)",
    "No cycles detected in 10-day window"
  ],
  "recommendation": "monitor"
}
```
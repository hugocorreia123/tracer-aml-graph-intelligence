# SAR draft — Ring 162
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:58:44.830757+00:00 by qwen/qwen3-32b

- Accounts: 12  ·  Transactions: 11  ·  Total: $143,930
- Window: 2022-09-01 12:36:00 → 2022-09-07 16:03:00
- Detected typology: **FAN-IN** (confidence 0.92)
- Recommendation: **file_sar**

## Summary
The ring exhibits a classic FAN-IN pattern, with 11/12 accounts funneling funds into a single central account (25866_80E27AA10). This account received 9 transactions totaling $133,920.13 (93% of total ring volume) from dispersed sources.

## Key evidence
- 25866_80E27AA10 received funds from 9 distinct accounts (in_deg=9)
- Largest single inflow: $89,127.94 from 19477_80DB25390
- 11 of 12 accounts have out_deg=1 targeting 25866_80E27AA10
- No outflows detected from central account (out_deg=0)

## Full narrative
```json
{
  "typology": "FAN-IN",
  "confidence": 0.92,
  "summary": "The ring exhibits a classic FAN-IN pattern, with 11/12 accounts funneling funds into a single central account (25866_80E27AA10). This account received 9 transactions totaling $133,920.13 (93% of total ring volume) from dispersed sources.",
  "key_evidence": [
    "25866_80E27AA10 received funds from 9 distinct accounts (in_deg=9)",
    "Largest single inflow: $89,127.94 from 19477_80DB25390",
    "11 of 12 accounts have out_deg=1 targeting 25866_80E27AA10",
    "No outflows detected from central account (out_deg=0)"
  ],
  "recommendation": "file_sar"
}
```
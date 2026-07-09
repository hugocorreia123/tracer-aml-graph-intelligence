# SAR draft — Ring 197
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:56:21.253165+00:00 by qwen/qwen3-32b

- Accounts: 11  ·  Transactions: 11  ·  Total: $101,269
- Window: 2022-09-02 19:04:00 → 2022-09-13 19:05:00
- Detected typology: **FAN-IN** (confidence 0.93)
- Recommendation: **file_sar**

## Summary
Funds from 10 distinct accounts consolidated into a single central account (225263_80E6BFD50) over 11 transactions totaling $101,269.12. All accounts show outflow to this hub with no subsequent outflow detected.

## Key evidence
- Account 225263_80E6BFD50 received 100% of all transactions ($101k total) from 10 other accounts
- All 11 accounts exhibit out_deg=1 to the central account, in_deg=0 except the hub
- Top 9 transactions represent $93,167.12 concentrated into the hub account

## Full narrative
```json
{
  "typology": "FAN-IN",
  "confidence": 0.93,
  "summary": "Funds from 10 distinct accounts consolidated into a single central account (225263_80E6BFD50) over 11 transactions totaling $101,269.12. All accounts show outflow to this hub with no subsequent outflow detected.",
  "key_evidence": [
    "Account 225263_80E6BFD50 received 100% of all transactions ($101k total) from 10 other accounts",
    "All 11 accounts exhibit out_deg=1 to the central account, in_deg=0 except the hub",
    "Top 9 transactions represent $93,167.12 concentrated into the hub account"
  ],
  "recommendation": "file_sar"
}
```
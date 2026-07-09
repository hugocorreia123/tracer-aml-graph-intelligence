# SAR draft — Ring 73
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:46:05.318176+00:00 by qwen/qwen3-32b

- Accounts: 15  ·  Transactions: 19  ·  Total: $4,647,451,856
- Window: 2022-09-01 00:06:00 → 2022-09-14 19:51:00
- Detected typology: **FAN-IN** (confidence 0.85)
- Recommendation: **file_sar**

## Summary
This ring exhibits a clear FAN-IN pattern where multiple accounts funnel funds into a central hub account (41407_80F454910), which receives 8 distinct incoming transactions from disparate sources. The structure is amplified by an initial massive transfer of $4.61 billion from 1688_800406A10 to 1_800407920, suggesting potential consolidation of illicit proceeds.

## Key evidence
- Account 41407_80F454910 receives funds from 8 unique senders (in_deg=8) with no outgoing transactions (out_deg=0)
- $4.61 billion transferred from 1688_800406A10 to 1_800407920 in single transaction (99.3% of total ring volume)
- 15 accounts/19 transactions compressed into 14-day window with high GNN score (0.7588)

## Full narrative
```json
{
  "typology": "FAN-IN",
  "confidence": 0.85,
  "summary": "This ring exhibits a clear FAN-IN pattern where multiple accounts funnel funds into a central hub account (41407_80F454910), which receives 8 distinct incoming transactions from disparate sources. The structure is amplified by an initial massive transfer of $4.61 billion from 1688_800406A10 to 1_800407920, suggesting potential consolidation of illicit proceeds.",
  "key_evidence": [
    "Account 41407_80F454910 receives funds from 8 unique senders (in_deg=8) with no outgoing transactions (out_deg=0)",
    "$4.61 billion transferred from 1688_800406A10 to 1_800407920 in single transaction (99.3% of total ring volume)",
    "15 accounts/19 transactions compressed into 14-day window with high GNN score (0.7588)"
  ],
  "recommendation": "file_sar"
}
```
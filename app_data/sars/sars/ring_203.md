# SAR draft — Ring 203
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T02:39:00.465145+00:00 by qwen/qwen3-32b

- Accounts: 11  ·  Transactions: 23  ·  Total: $69,597
- Window: 2022-09-01 03:13:00 → 2022-09-09 07:10:00
- Detected typology: **GATHER-SCATTER** (confidence 0.95)
- Recommendation: **file_sar**

## Summary
Funds consolidate into hub account 211_808E44B10 from multiple sources before dispersing to 8 different accounts. The hub received €7,924.37, £5,754.73, and $9,169.69 over 9 days, then scattered $18,533.55 and $11,900.42 in outbound payments.

## Key evidence
- Hub account 211_808E44B10 received 14 transactions totaling $9,169.69 from 220504_808396D50
- Largest outbound transfers from hub: $18,533.55 to 3144_809478870 and $11,900.42 to 23555_80BA57230
- Account 211_808E44B10 serves as both fan-in hub (receiving 6 unique senders) and fan-out hub (sending to 8 unique recipients)

## Full narrative
```json
{
  "typology": "GATHER-SCATTER",
  "confidence": 0.95,
  "summary": "Funds consolidate into hub account 211_808E44B10 from multiple sources before dispersing to 8 different accounts. The hub received €7,924.37, £5,754.73, and $9,169.69 over 9 days, then scattered $18,533.55 and $11,900.42 in outbound payments.",
  "key_evidence": [
    "Hub account 211_808E44B10 received 14 transactions totaling $9,169.69 from 220504_808396D50",
    "Largest outbound transfers from hub: $18,533.55 to 3144_809478870 and $11,900.42 to 23555_80BA57230",
    "Account 211_808E44B10 serves as both fan-in hub (receiving 6 unique senders) and fan-out hub (sending to 8 unique recipients)"
  ],
  "recommendation": "file_sar"
}
```
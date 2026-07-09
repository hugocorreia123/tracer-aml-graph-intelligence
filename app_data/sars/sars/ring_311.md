# SAR draft — Ring 311
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T03:03:42.783970+00:00 by qwen/qwen3-32b

- Accounts: 9  ·  Transactions: 13  ·  Total: $23,517
- Window: 2022-09-02 04:01:00 → 2022-09-11 08:24:00
- Detected typology: **MIXED/UNCLEAR** (confidence 0.7)
- Recommendation: **monitor**

## Summary
The ring exhibits limited transaction activity (13 tx) across 9 accounts with a hub-like account (16031_809BEDF40) dispersing funds to two recipients. While one account (215186_80598ED20) recirculates funds back to the initial sender (8798_8054C12F0), the network lacks clear cyclic patterns or layered structures typical of laundering typologies.

## Key evidence
- Account 16031_809BEDF40 sends to two distinct accounts ($2,629.60 and $2,383.39)
- Account 215186_80598ED20 returns $2,634 to original sender 8798_8054C12F0
- Only 8 edges for 9 accounts suggest sparse connectivity
- No directed cycles detected in structural analysis

## Full narrative
```json
{
  "typology": "MIXED/UNCLEAR",
  "confidence": 0.7,
  "summary": "The ring exhibits limited transaction activity (13 tx) across 9 accounts with a hub-like account (16031_809BEDF40) dispersing funds to two recipients. While one account (215186_80598ED20) recirculates funds back to the initial sender (8798_8054C12F0), the network lacks clear cyclic patterns or layered structures typical of laundering typologies.",
  "key_evidence": [
    "Account 16031_809BEDF40 sends to two distinct accounts ($2,629.60 and $2,383.39)",
    "Account 215186_80598ED20 returns $2,634 to original sender 8798_8054C12F0",
    "Only 8 edges for 9 accounts suggest sparse connectivity",
    "No directed cycles detected in structural analysis"
  ],
  "recommendation": "monitor"
}
```
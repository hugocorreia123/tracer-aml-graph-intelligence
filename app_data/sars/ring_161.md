# SAR draft — Ring 161
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T03:00:34.082328+00:00 by qwen/qwen3-32b

- Accounts: 12  ·  Transactions: 12  ·  Total: $407,930
- Window: 2022-09-02 08:36:00 → 2022-09-11 14:49:00
- Detected typology: **FAN-OUT** (confidence 0.95)
- Recommendation: **file_sar**

## Summary
A single account (11128_8045F4500) rapidly dispersed funds to 10 other accounts in the ring, with no evidence of recirculation. The central account sent $295,519.18 to 213704_805BD1400 and $44,949.46 to 210997_80C40C500 among other large transfers.

## Key evidence
- Account 11128_8045F4500 has out-degree 10 (sends to 10 accounts), in-degree 0
- $295k+ transferred from 11128_8045F4500 to 213704_805BD1400 in single transaction
- 11 of 12 accounts have out-degree=0 (no outgoing transactions)
- No cycles detected in 11-edge network

## Full narrative
```json
{
  "typology": "FAN-OUT",
  "confidence": 0.95,
  "summary": "A single account (11128_8045F4500) rapidly dispersed funds to 10 other accounts in the ring, with no evidence of recirculation. The central account sent $295,519.18 to 213704_805BD1400 and $44,949.46 to 210997_80C40C500 among other large transfers.",
  "key_evidence": [
    "Account 11128_8045F4500 has out-degree 10 (sends to 10 accounts), in-degree 0",
    "$295k+ transferred from 11128_8045F4500 to 213704_805BD1400 in single transaction",
    "11 of 12 accounts have out-degree=0 (no outgoing transactions)",
    "No cycles detected in 11-edge network"
  ],
  "recommendation": "file_sar"
}
```
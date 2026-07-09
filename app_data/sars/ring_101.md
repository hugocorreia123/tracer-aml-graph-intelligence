# SAR draft — Ring 101
**DRAFT — PENDING HUMAN REVIEW**  ·  generated 2026-07-09T03:12:07.006680+00:00 by qwen/qwen3-32b

- Accounts: 14  ·  Transactions: 20  ·  Total: $167,410
- Window: 2022-09-01 00:06:00 → 2022-09-10 18:17:00
- Detected typology: **GATHER-SCATTER** (confidence 0.75)
- Recommendation: **file_sar**

## Summary
Funds consolidate into accounts 5365_8025DCE40 and 6052_8027DE880 via multiple upstream sources, then disperse through layered transactions to 40653_80F61C2F0 and downstream accounts. The 10-day timeframe and lack of direct cycles suggest structured layering.

## Key evidence
- Account 5365_8025DCE40 receives €15,660.29 from 23_8025DC810 and CHF 11,477.04 from 22806_8027EC510
- Account 40653_80F61C2F0 sends ¥64,722.01 to 40836_80F653A20 (largest single flow)
- Account 6052_8027DE880 aggregates $1,689.15 + $530.27 + $283.81 from three sources
- No cycles detected in 13-edge network, but 4→3→2→1 transaction chaining observed

## Full narrative
```json
{
  "typology": "GATHER-SCATTER",
  "confidence": 0.75,
  "summary": "Funds consolidate into accounts 5365_8025DCE40 and 6052_8027DE880 via multiple upstream sources, then disperse through layered transactions to 40653_80F61C2F0 and downstream accounts. The 10-day timeframe and lack of direct cycles suggest structured layering.",
  "key_evidence": [
    "Account 5365_8025DCE40 receives €15,660.29 from 23_8025DC810 and CHF 11,477.04 from 22806_8027EC510",
    "Account 40653_80F61C2F0 sends ¥64,722.01 to 40836_80F653A20 (largest single flow)",
    "Account 6052_8027DE880 aggregates $1,689.15 + $530.27 + $283.81 from three sources",
    "No cycles detected in 13-edge network, but 4→3→2→1 transaction chaining observed"
  ],
  "recommendation": "file_sar"
}
```
"""Tracer — Phase 6b: cross-family judge for SAR groundedness.

A judge model from a DIFFERENT model family (openai/gpt-oss-120b, no
tools) scores each SAR draft against the ring's actual evidence:
are the accounts, amounts, flows, and timing claims in the narrative
supported by the data? Cross-family judging reduces self-preference
bias (same design validated in Voyager at kappa=0.95).

Verdicts: GROUNDED (1.0) / PARTIALLY_GROUNDED (0.5) / UNGROUNDED (0.0)

Resumable: skips ring_ids already in runs/judgments.jsonl.

Output: runs/judgments.jsonl + summary
"""

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
assert os.environ.get("GROQ_API_KEY"), "GROQ_API_KEY missing (.env)"

JUDGE_MODEL = "openai/gpt-oss-120b"
MAX_EDGES = 40

rings = {r["ring_id"]: r for r in
         json.loads(Path("data/processed/rings.json").read_text())}
eval_set = json.loads(Path("runs/eval_set.json").read_text())

done = set()
out_path = Path("runs/judgments.jsonl")
if out_path.exists():
    done = {json.loads(l)["ring_id"] for l in out_path.open()}

judge = ChatGroq(model=JUDGE_MODEL, temperature=0.0, max_retries=8)

PROMPT = """You are auditing an AI-drafted Suspicious Activity Report
(SAR) for factual groundedness. Compare the SAR's claims against the
ring evidence below. Check: cited account IDs exist in the evidence;
cited amounts/counts/dates are consistent with it; the structural
description (who pays whom) matches the flows. Judge ONLY factual
groundedness, not writing quality and not whether the typology guess
is correct.

RING EVIDENCE (source of truth):
{evidence}

SAR DRAFT UNDER AUDIT:
{sar}

Respond with EXACTLY one JSON block:
```json
{{"verdict": "GROUNDED" | "PARTIALLY_GROUNDED" | "UNGROUNDED",
  "problems": ["<specific unsupported claim>", ...]}}
```
GROUNDED = every specific claim supported. PARTIALLY_GROUNDED = minor
unsupported details. UNGROUNDED = invented accounts/amounts or a
structural description contradicted by the flows."""

SCORE = {"GROUNDED": 1.0, "PARTIALLY_GROUNDED": 0.5, "UNGROUNDED": 0.0}

results = []
for item in eval_set:
    rid = item["ring_id"]
    if rid in done:
        continue
    sar_path = Path(f"sars/ring_{rid}.json")
    if not sar_path.exists():
        continue
    sar = json.loads(sar_path.read_text())
    r = rings[rid]
    evidence = {
        "summary": {k: r[k] for k in
                    ["n_accounts", "n_edges", "n_tx", "total_amount",
                     "currencies", "formats", "t_start", "t_end"]},
        "flows": sorted(r["edges"], key=lambda e: -e["amount"])[:MAX_EDGES],
        "accounts": r["accounts"],
    }
    msg = PROMPT.format(evidence=json.dumps(evidence),
                        sar=json.dumps({"verdict": sar["verdict"],
                                        "narrative": sar["narrative"]}))
    try:
        resp = judge.invoke(msg).content
    except Exception as e:
        print(f"ring {rid}: ERROR {e} (rerun to resume)")
        continue
    m = re.search(r"```json\s*(\{.*?\})\s*```", resp, re.DOTALL)
    if not m:
        m = re.search(r"(\{.*\})", resp, re.DOTALL)
    try:
        j = json.loads(m.group(1))
    except Exception:
        print(f"ring {rid}: judge parse failure, skipping")
        continue
    rec = {"ring_id": rid, "judge_model": JUDGE_MODEL,
           "verdict": j.get("verdict"),
           "score": SCORE.get(j.get("verdict"), None),
           "problems": j.get("problems", [])}
    with out_path.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    results.append(rec)
    print(f"ring {rid}: {rec['verdict']}"
          + (f"  problems: {rec['problems'][:2]}" if rec["problems"] else ""))

# ---------------- summary ----------------
all_recs = [json.loads(l) for l in out_path.open()]
scores = [r["score"] for r in all_recs if r["score"] is not None]
from collections import Counter
print("\n" + "=" * 50)
print("JUDGE SUMMARY (evidence-groundedness)")
print("=" * 50)
print(f"SARs judged: {len(all_recs)}")
print(dict(Counter(r["verdict"] for r in all_recs)))
if scores:
    print(f"mean groundedness score: {sum(scores) / len(scores):.3f}")

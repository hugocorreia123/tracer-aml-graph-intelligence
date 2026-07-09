"""Tracer — Phase 6a: investigator evaluation batch.

1. Match rings to ground-truth attempts (>=50% of an attempt's
   accounts inside the ring -> the ring "contains" that attempt).
2. Stratified selection: up to 3 matched rings per typology
   (objective cases) + 8 weak unmatched rings (should NOT be
   escalated).
3. Run the investigator over the set (resumable: skips rings that
   already have sars/ring_{id}.json).
4. Objective metric #1: typology accuracy on matched rings
   (agent infers labels-blind; ground truth from the patterns file).
   Plus escalation behavior on weak rings.

Output: runs/eval_set.json, sars/ring_*.json|md,
        models/investigator_eval.json
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, "scripts")
from investigate import investigate, rings, to_markdown  # noqa: E402

Path("runs").mkdir(exist_ok=True)
Path("sars").mkdir(exist_ok=True)

PER_TYPOLOGY = 3
N_WEAK = 8

# ---------------- 1. match rings to attempts ----------------
patterns = pd.read_parquet("data/processed/patterns.parquet")
attempt_nodes = patterns.groupby("attempt_id").apply(
    lambda d: set(d["src"]) | set(d["dst"]), include_groups=False)
attempt_typo = patterns.groupby("attempt_id")["typology"].first()

ring_match = {}  # ring_id -> ground-truth typology (best match)
for rid, r in rings.items():
    accs = set(r["accounts"])
    best = None
    for aid, nodes in attempt_nodes.items():
        ov = len(nodes & accs) / len(nodes)
        if ov >= 0.5 and (best is None or ov > best[1]):
            best = (attempt_typo[aid], ov)
    if best:
        ring_match[rid] = best[0]

print(f"rings matched to a ground-truth attempt: {len(ring_match)}")
print(dict(Counter(ring_match.values())))

# ---------------- 2. stratified selection ----------------
if Path("runs/eval_set.json").exists():
    eval_set = json.loads(Path("runs/eval_set.json").read_text())
    print(f"reusing existing eval set ({len(eval_set)} rings)")
else:
    by_typo = defaultdict(list)
    for rid, t in ring_match.items():
        by_typo[t].append(rid)
    selected = []
    for t in sorted(by_typo):
        picks = sorted(by_typo[t],
                       key=lambda rid: -rings[rid]["mean_gnn_score"])
        selected += [{"ring_id": rid, "truth": t}
                     for rid in picks[:PER_TYPOLOGY]]
    weak = sorted(
        (r for rid, r in rings.items() if rid not in ring_match),
        key=lambda r: r["mean_gnn_score"])[:N_WEAK]
    selected += [{"ring_id": r["ring_id"], "truth": None} for r in weak]
    eval_set = selected
    Path("runs/eval_set.json").write_text(json.dumps(eval_set, indent=2))
    print(f"selected {len(eval_set)} rings "
          f"({len(eval_set) - N_WEAK} matched + {N_WEAK} weak)")

# ---------------- 3. run investigator (resumable) ----------------
for i, item in enumerate(eval_set):
    rid = item["ring_id"]
    out = Path(f"sars/ring_{rid}.json")
    if out.exists():
        print(f"[{i + 1}/{len(eval_set)}] ring {rid}: already done, skip")
        continue
    print(f"[{i + 1}/{len(eval_set)}] ring {rid} "
          f"({rings[rid]['n_accounts']} accts, truth={item['truth']}) ...")
    try:
        sar = investigate(rid)
    except Exception as e:  # rate limits etc — rerun resumes
        print(f"  ERROR: {e}")
        continue
    out.write_text(json.dumps(sar, indent=2))
    Path(f"sars/ring_{rid}.md").write_text(to_markdown(sar))
    v = sar["verdict"]
    print(f"  -> {v.get('typology')}  conf={v.get('confidence')}  "
          f"rec={v.get('recommendation')}")

# ---------------- 4. objective metrics ----------------
EQUIV = {"MIXED/UNCLEAR": "MIXED", "UNCLEAR": "MIXED"}
rows, correct, escal_weak = [], 0, 0
n_matched = n_weak_done = 0
confusion = Counter()
for item in eval_set:
    rid = item["ring_id"]
    f = Path(f"sars/ring_{rid}.json")
    if not f.exists():
        continue
    v = json.loads(f.read_text())["verdict"]
    pred = EQUIV.get(str(v.get("typology", "?")).upper(),
                     str(v.get("typology", "?")).upper())
    rec = v.get("recommendation")
    rows.append({"ring_id": rid, "truth": item["truth"], "pred": pred,
                 "confidence": v.get("confidence"), "rec": rec})
    if item["truth"]:
        n_matched += 1
        confusion[(item["truth"], pred)] += 1
        if pred == item["truth"]:
            correct += 1
    else:
        n_weak_done += 1
        if rec == "file_sar":
            escal_weak += 1

acc = correct / n_matched if n_matched else 0
print("\n" + "=" * 56)
print("INVESTIGATOR OBJECTIVE EVAL")
print("=" * 56)
print(f"typology accuracy on ground-truth rings: "
      f"{correct}/{n_matched} ({acc:.1%})")
print(f"weak rings wrongly escalated to file_sar: "
      f"{escal_weak}/{n_weak_done}")
print("\nconfusion (truth -> predicted):")
for (t, p), c in sorted(confusion.items()):
    flag = "  ok" if t == p else ""
    print(f"  {t:<16} -> {p:<16} {c}{flag}")

out = {"typology_accuracy": acc, "n_matched": n_matched,
       "correct": correct, "weak_escalated": escal_weak,
       "n_weak": n_weak_done,
       "rows": rows}
Path("models/investigator_eval.json").write_text(
    json.dumps(out, indent=2))
print("\nwrote models/investigator_eval.json")

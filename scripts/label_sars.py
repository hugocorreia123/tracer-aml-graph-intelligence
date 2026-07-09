"""Tracer — Phase 6c: blind human labels + Cohen's kappa.

You audit each SAR against the ring evidence — the SAME task the
judge did — WITHOUT seeing the judge's verdicts. Verdicts are
compared only after labeling completes.

Labels: g = GROUNDED, p = PARTIALLY_GROUNDED, u = UNGROUNDED
        s = skip for now, q = quit (progress saved, resumable)

Usage:
  uv run python scripts/label_sars.py          # label all judged rings
  uv run python scripts/label_sars.py --kappa  # just recompute kappa

Output: runs/human_labels.jsonl, models/agreement.json
"""

import argparse
import json
from collections import Counter
from pathlib import Path

LABELS = {"g": "GROUNDED", "p": "PARTIALLY_GROUNDED", "u": "UNGROUNDED"}
SCORE = {"GROUNDED": 1.0, "PARTIALLY_GROUNDED": 0.5, "UNGROUNDED": 0.0}

rings = {r["ring_id"]: r for r in
         json.loads(Path("data/processed/rings.json").read_text())}
judgments = {json.loads(l)["ring_id"]: json.loads(l)
             for l in Path("runs/judgments.jsonl").open()}

labels_path = Path("runs/human_labels.jsonl")
human = {}
if labels_path.exists():
    human = {json.loads(l)["ring_id"]: json.loads(l)
             for l in labels_path.open()}


def show(rid: int):
    r = rings[rid]
    sar = json.loads(Path(f"sars/ring_{rid}.json").read_text())
    print("\n" + "#" * 70)
    print(f"RING {rid} — {r['n_accounts']} accounts, {r['n_tx']} tx, "
          f"${r['total_amount']:,.0f}, {r['t_start']} -> {r['t_end']}")
    print(f"currencies: {r['currencies']}  formats: {r['formats']}")
    print("-" * 70)
    print("FLOWS (largest first):")
    for e in sorted(r["edges"], key=lambda e: -e["amount"])[:40]:
        print(f"  {e['src']} -> {e['dst']}  x{e['n_tx']}  "
              f"${e['amount']:,.2f}")
    if len(r["edges"]) > 40:
        print(f"  ... (+{len(r['edges']) - 40} more edges)")
    print("-" * 70)
    print("SAR NARRATIVE UNDER AUDIT:")
    print(sar["narrative"])
    print("#" * 70)


def kappa(a: list, b: list) -> float:
    n = len(a)
    cats = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def report():
    both = [rid for rid in judgments if rid in human]
    if len(both) < 2:
        print("not enough overlapping labels yet")
        return
    h = [human[rid]["verdict"] for rid in both]
    j = [judgments[rid]["verdict"] for rid in both]
    k = kappa(h, j)
    agree = sum(1 for x, y in zip(h, j) if x == y) / len(both)
    conf = Counter(zip(h, j))
    print("\n" + "=" * 56)
    print("HUMAN vs JUDGE AGREEMENT (groundedness)")
    print("=" * 56)
    print(f"n = {len(both)}   raw agreement = {agree:.1%}   "
          f"Cohen's kappa = {k:.3f}")
    print("\nconfusion (human -> judge):")
    for (hh, jj), c in sorted(conf.items()):
        flag = "  ok" if hh == jj else ""
        print(f"  {hh:<20} -> {jj:<20} {c}{flag}")
    hs = [SCORE[x] for x in h]
    js = [SCORE[x] for x in j]
    out = {"n": len(both), "raw_agreement": agree, "kappa": k,
           "human_mean_score": sum(hs) / len(hs),
           "judge_mean_score": sum(js) / len(js),
           "confusion": {f"{hh}->{jj}": c
                         for (hh, jj), c in conf.items()},
           "disagreements": [rid for rid in both
                             if human[rid]["verdict"]
                             != judgments[rid]["verdict"]]}
    Path("models/agreement.json").write_text(json.dumps(out, indent=2))
    print("\nwrote models/agreement.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--kappa", action="store_true",
                    help="skip labeling, just compute agreement")
    args = ap.parse_args()

    if not args.kappa:
        todo = [rid for rid in judgments if rid not in human]
        print(f"{len(judgments)} judged SARs, {len(human)} already "
              f"labeled, {len(todo)} to go")
        print("Audit the narrative against the evidence. Same rubric as "
              "the judge:\n  g=GROUNDED (all specific claims supported)\n"
              "  p=PARTIALLY_GROUNDED (minor unsupported details)\n"
              "  u=UNGROUNDED (invented facts / contradicted structure)\n"
              "  s=skip  q=quit (resumable)")
        for rid in todo:
            show(rid)
            while True:
                ans = input(f"ring {rid} verdict [g/p/u/s/q]: ").strip().lower()
                if ans in ("g", "p", "u", "s", "q"):
                    break
            if ans == "q":
                break
            if ans == "s":
                continue
            rec = {"ring_id": rid, "verdict": LABELS[ans]}
            with labels_path.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            human[rid] = rec

    report()

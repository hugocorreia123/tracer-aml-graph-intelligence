"""Tracer — Phase 4: ring extraction + typology motifs.

Pipeline (no training, minutes on CPU):
  1. Flag accounts with GNN score above the 70%-recall operating point.
  2. Induce the subgraph of transactions BETWEEN flagged accounts;
     each weakly-connected component (>= MIN_RING accounts) is a
     candidate ring.
  3. For each ring, detect structural motifs (cycle, fan-in, fan-out,
     gather-scatter hub) and package an evidence bundle: accounts,
     flows, amounts, timing, currencies, GNN scores.
  4. Validate against the AMLworld patterns ground truth: how many of
     the 370 labeled attempts does a candidate ring overlap?

Outputs:
  data/processed/rings.json  — evidence bundles for the investigator
  models/ring_metrics.json   — validation numbers for the README
"""

import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

MIN_RING = 3          # accounts
MAX_CYCLE_LEN = 12    # cap cycle search
TOP_SHOW = 10

print("loading ...")
trans = pd.read_parquet("data/processed/transactions.parquet")
scores = pd.read_parquet("data/processed/scores_sage_tuned.parquet")
patterns = pd.read_parquet("data/processed/patterns.parquet")
op = json.loads(Path("models/operating_point.json").read_text())

# crude but honest FX normalization (approx 2022 rates), documented
FX = {"US Dollar": 1.0, "Euro": 1.05, "UK Pound": 1.2, "Yen": 0.0072,
      "Yuan": 0.145, "Rupee": 0.0125, "Ruble": 0.0165,
      "Australian Dollar": 0.68, "Canadian Dollar": 0.75,
      "Swiss Franc": 1.05, "Brazil Real": 0.19, "Saudi Riyal": 0.27,
      "Shekel": 0.29, "Mexican Peso": 0.05, "Bitcoin": 20000.0}
trans["amount_usd"] = trans["amount_paid"] * trans["pay_currency"].map(FX)

# ---------------- 1. flag accounts ----------------
# threshold = score of the last alert at the 70%-recall point,
# computed over ALL accounts using the same alert-rate as test
r70 = next(r for r in op if r["recall"] == 0.70)
alert_rate = r70["gnn"]["alerts"] / 103_018  # test alert share
k = int(alert_rate * len(scores))
thr = np.sort(scores["gnn_score"].values)[-k]
flagged = set(scores.loc[scores["gnn_score"] >= thr, "node_id"])
score_map = dict(zip(scores["node_id"], scores["gnn_score"]))
print(f"threshold {thr:.4f} -> {len(flagged):,} flagged accounts "
      f"({100 * len(flagged) / len(scores):.2f}%)")

# ---------------- 2. rings = components among flagged ----------------
sub = trans[trans["src"].isin(flagged) & trans["dst"].isin(flagged)]
sub = sub[sub["src"] != sub["dst"]]  # self-loops are not rings
print(f"transactions between flagged accounts: {len(sub):,}")

G = nx.DiGraph()
for r in sub.itertuples(index=False):
    if G.has_edge(r.src, r.dst):
        e = G[r.src][r.dst]
        e["n_tx"] += 1
        e["amount"] += r.amount_usd
    else:
        G.add_edge(r.src, r.dst, n_tx=1, amount=r.amount_usd)

comps = [c for c in nx.weakly_connected_components(G) if len(c) >= MIN_RING]
comps.sort(key=len, reverse=True)
print(f"candidate rings (>= {MIN_RING} accounts): {len(comps)}")

MAX_RING = 60  # accounts; larger groups get recursively decomposed


def decompose(comp, res=1.0):
    if len(comp) <= MAX_RING or res > 16:
        return [comp]
    UH = G.subgraph(comp).to_undirected()
    coms = [set(c) for c in
            nx.community.louvain_communities(UH, seed=42, resolution=res)]
    if len(coms) <= 1:  # can't split further
        return [comp]
    out = []
    for c in coms:
        if len(c) >= MIN_RING:
            out.extend(decompose(c, res * 2))
    return out


final = []
for comp in comps:
    final.extend(decompose(comp))
print(f"after recursive decomposition (> {MAX_RING}): {len(final)} rings, "
      f"max size {max(len(c) for c in final)}")
comps = sorted(final, key=len, reverse=True)


# ---------------- 3. motifs + evidence ----------------
def motifs(H: nx.DiGraph) -> dict:
    out = {}
    try:
        cyc = list(nx.simple_cycles(H, length_bound=MAX_CYCLE_LEN))
        cyc = [c for c in cyc if len(c) >= 3]
        if cyc:
            out["cycles"] = sorted(cyc, key=len, reverse=True)[:3]
    except Exception:
        pass
    deg_out = dict(H.out_degree())
    deg_in = dict(H.in_degree())
    fan_out = [n for n, d in deg_out.items() if d >= 4]
    fan_in = [n for n, d in deg_in.items() if d >= 4]
    if fan_out:
        out["fan_out_hubs"] = fan_out[:5]
    if fan_in:
        out["fan_in_hubs"] = fan_in[:5]
    hubs = set(fan_out) & set(fan_in)
    if hubs:
        out["gather_scatter_hubs"] = list(hubs)[:5]
    return out


rings = []
for i, comp in enumerate(comps):
    H = G.subgraph(comp)
    tx = sub[sub["src"].isin(comp) & sub["dst"].isin(comp)]
    m = motifs(H)
    label = ("CYCLE" if "cycles" in m else
             "GATHER-SCATTER" if "gather_scatter_hubs" in m else
             "FAN-OUT" if "fan_out_hubs" in m else
             "FAN-IN" if "fan_in_hubs" in m else "MIXED")
    rings.append({
        "ring_id": i,
        "n_accounts": len(comp),
        "n_edges": H.number_of_edges(),
        "n_tx": int(len(tx)),
        "total_amount": float(tx["amount_usd"].sum()),
        "currencies": sorted(tx["pay_currency"].unique().tolist()),
        "formats": sorted(tx["payment_format"].unique().tolist()),
        "t_start": str(tx["timestamp"].min()),
        "t_end": str(tx["timestamp"].max()),
        "mean_gnn_score": float(np.mean([score_map[n] for n in comp])),
        "motif_label": label,
        "motifs": m,
        "accounts": sorted(comp),
        "edges": [{"src": u, "dst": v, "n_tx": d["n_tx"],
                   "amount": round(d["amount"], 2)}
                  for u, v, d in H.edges(data=True)],
    })

print("\nmotif labels:", dict(Counter(r["motif_label"] for r in rings)))

# ---------------- 4. validate vs ground truth ----------------
attempt_nodes = patterns.groupby("attempt_id").apply(
    lambda d: set(d["src"]) | set(d["dst"]), include_groups=False)
attempt_typo = patterns.groupby("attempt_id")["typology"].first()

ring_sets = [set(r["accounts"]) for r in rings]
hits = 0
typo_hits = Counter()
typo_total = Counter(attempt_typo.values)
for aid, nodes in attempt_nodes.items():
    covered = any(len(nodes & rs) / len(nodes) >= 0.5 for rs in ring_sets)
    if covered:
        hits += 1
        typo_hits[attempt_typo[aid]] += 1

illicit_nodes = set(
    scores.loc[scores["is_illicit"] == 1, "node_id"])
ring_nodes_all = set().union(*ring_sets) if ring_sets else set()
purity = (len(ring_nodes_all & illicit_nodes) / len(ring_nodes_all)
          if ring_nodes_all else 0)

metrics = {
    "flagged_accounts": len(flagged),
    "candidate_rings": len(rings),
    "attempts_total": int(len(attempt_nodes)),
    "attempts_covered_50pct": hits,
    "attempt_coverage": hits / len(attempt_nodes),
    "ring_node_purity": purity,
    "coverage_by_typology": {
        t: f"{typo_hits[t]}/{typo_total[t]}" for t in sorted(typo_total)},
}
print("\n" + "=" * 56)
print("RING EXTRACTION vs GROUND TRUTH")
print("=" * 56)
print(f"laundering attempts covered (>=50% of accounts in a ring): "
      f"{hits}/{len(attempt_nodes)} ({100 * hits / len(attempt_nodes):.1f}%)")
print(f"ring-node purity (share of ring accounts truly illicit): "
      f"{purity:.1%}")
print("coverage by typology:")
for t in sorted(typo_total):
    print(f"  {t:<16} {typo_hits[t]:>3}/{typo_total[t]}")

print(f"\ntop {TOP_SHOW} rings by amount:")
for r in sorted(rings, key=lambda r: -r["total_amount"])[:TOP_SHOW]:
    print(f"  ring {r['ring_id']:>3}  {r['n_accounts']:>3} accts  "
          f"{r['n_tx']:>4} tx  ${r['total_amount']:>14,.0f}  "
          f"{r['motif_label']}")

with open("data/processed/rings.json", "w") as f:
    json.dump(rings, f, indent=1)
with open("models/ring_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)
print("\nwrote data/processed/rings.json, models/ring_metrics.json")

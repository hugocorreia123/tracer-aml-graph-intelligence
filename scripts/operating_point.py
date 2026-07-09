"""Tracer — Phase 3: operating point & ROI.

At matched recall levels on the TEST split, how many false-positive
alerts does each model generate? FP reduction at fixed recall is the
number an AML team actually feels — fewer wasted investigations at
the same catch rate — and it translates directly to analyst cost.

Runs in seconds (pure numpy on saved scores).

Output: models/operating_point.json + console table
"""

import json

import lightgbm as lgb
import numpy as np
import pandas as pd

COST_PER_ALERT = (30, 70)  # $ range, industry estimates
RECALLS = [0.50, 0.60, 0.70, 0.80]

# ---------------- scores on test ----------------
feat = pd.read_parquet("data/processed/features.parquet")
test = feat[feat["split"] == "test"].reset_index(drop=True)
y = test["is_illicit"].values
n_pos = int(y.sum())
print(f"test accounts: {len(test):,}  illicit: {n_pos:,}")

# champion GNN scores (sage_tuned)
gnn = pd.read_parquet("data/processed/scores_sage_tuned.parquet")
gnn_scores = (
    test[["node_id"]].merge(gnn, on="node_id", how="left")["gnn_score"].values
)

# baseline scores (recompute from saved model — deterministic)
booster = lgb.Booster(model_file="models/baseline_lgbm.txt")
X_cols = [c for c in feat.columns
          if c not in ("node_id", "is_illicit", "split")]
lgb_scores = booster.predict(test[X_cols])


def at_recall(scores: np.ndarray, y: np.ndarray, target_r: float):
    """Smallest alert set achieving >= target recall."""
    order = np.argsort(-scores)
    y_sorted = y[order]
    tp_cum = np.cumsum(y_sorted)
    need = int(np.ceil(target_r * y.sum()))
    k = int(np.searchsorted(tp_cum, need) + 1)  # alerts needed
    tp = int(tp_cum[k - 1])
    fp = k - tp
    return {"alerts": k, "tp": tp, "fp": fp,
            "precision": tp / k, "recall": tp / y.sum()}


rows = []
print(f"\n{'recall':>7} | {'LGBM alerts':>11} {'FP':>7} | "
      f"{'GNN alerts':>10} {'FP':>7} | {'FP cut':>7}")
print("-" * 65)
for r in RECALLS:
    b = at_recall(lgb_scores, y, r)
    g = at_recall(gnn_scores, y, r)
    fp_cut = 1 - g["fp"] / b["fp"]
    rows.append({"recall": r, "lgbm": b, "gnn": g,
                 "fp_reduction": fp_cut})
    print(f"{r:>6.0%} | {b['alerts']:>11,} {b['fp']:>7,} | "
          f"{g['alerts']:>10,} {g['fp']:>7,} | {fp_cut:>6.1%}")

# ---------------- ROI translation ----------------
print("\nROI translation (at the 70% recall operating point):")
r70 = next(r for r in rows if r["recall"] == 0.70)
fp_saved = r70["lgbm"]["fp"] - r70["gnn"]["fp"]
share = fp_saved / r70["lgbm"]["fp"]
print(f"  false positives avoided at equal catch rate: {fp_saved:,} "
      f"({share:.1%} of baseline FP)")
for c in COST_PER_ALERT:
    print(f"  at ${c}/alert: ${fp_saved * c:,.0f} saved on this test set "
          f"({len(test):,} accounts, 18 days)")
print("  scaled to a bank screening 100,000 alerts/yr at the same FP "
      "reduction rate:")
for c in COST_PER_ALERT:
    yearly = 100_000 * r70["lgbm"]["fp"] / r70["lgbm"]["alerts"] * share * c
    print(f"    at ${c}/alert: ~${yearly:,.0f}/yr")

with open("models/operating_point.json", "w") as f:
    json.dump(rows, f, indent=2)
print("\nwrote models/operating_point.json")

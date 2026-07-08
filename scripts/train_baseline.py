"""Tracer — Phase 1: LightGBM tabular baseline.

Trains on the canonical split from features.parquet and reports
PR-AUC (primary), ROC-AUC, and F1/precision/recall at the
val-optimal threshold. This is the honest control every GNN
must beat on the SAME split.

Outputs:
  models/baseline_lgbm.txt      — trained model
  models/baseline_metrics.json  — metrics for the README
"""

import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import (average_precision_score, roc_auc_score,
                             precision_recall_curve)

SEED = 42
Path("models").mkdir(exist_ok=True)

feat = pd.read_parquet("data/processed/features.parquet")
drop = ["node_id", "is_illicit", "split"]
X_cols = [c for c in feat.columns if c not in drop]
print(f"{len(X_cols)} features: {X_cols}\n")

parts = {s: feat[feat["split"] == s] for s in ["train", "val", "test"]}
X = {s: p[X_cols] for s, p in parts.items()}
y = {s: p["is_illicit"].values for s, p in parts.items()}

pos_weight = (y["train"] == 0).sum() / (y["train"] == 1).sum()
print(f"scale_pos_weight = {pos_weight:.1f}")

model = lgb.LGBMClassifier(
    n_estimators=3000,
    learning_rate=0.03,
    num_leaves=127,
    min_child_samples=50,
    colsample_bytree=0.8,
    subsample=0.8,
    subsample_freq=1,
    random_state=SEED,
    n_jobs=-1,
)
model.fit(
    X["train"], y["train"],
    eval_set=[(X["val"], y["val"])],
    eval_metric="average_precision",
    callbacks=[lgb.early_stopping(200, verbose=True),
               lgb.log_evaluation(200)],
)

metrics = {}
scores = {}
for s in ["val", "test"]:
    p = model.predict_proba(X[s])[:, 1]
    scores[s] = p
    metrics[f"{s}_pr_auc"] = float(average_precision_score(y[s], p))
    metrics[f"{s}_roc_auc"] = float(roc_auc_score(y[s], p))

# Threshold chosen on VAL (max F1), applied unchanged to TEST
prec, rec, thr = precision_recall_curve(y["val"], scores["val"])
f1 = 2 * prec * rec / np.clip(prec + rec, 1e-9, None)
best = int(np.argmax(f1[:-1]))
threshold = float(thr[best])
metrics["threshold_val_maxf1"] = threshold

pred_test = (scores["test"] >= threshold).astype(int)
tp = int(((pred_test == 1) & (y["test"] == 1)).sum())
fp = int(((pred_test == 1) & (y["test"] == 0)).sum())
fn = int(((pred_test == 0) & (y["test"] == 1)).sum())
metrics["test_precision"] = tp / max(tp + fp, 1)
metrics["test_recall"] = tp / max(tp + fn, 1)
metrics["test_f1"] = (2 * metrics["test_precision"] * metrics["test_recall"]
                      / max(metrics["test_precision"]
                            + metrics["test_recall"], 1e-9))
metrics["test_alerts"] = int(pred_test.sum())
metrics["test_tp"] = tp
metrics["test_fp"] = fp
metrics["best_iteration"] = int(model.best_iteration_ or 0)

random_baseline = float(y["test"].mean())

print("\n" + "=" * 52)
print("BASELINE RESULTS (LightGBM, per-account features)")
print("=" * 52)
print(f"val  PR-AUC:  {metrics['val_pr_auc']:.4f}")
print(f"test PR-AUC:  {metrics['test_pr_auc']:.4f}   "
      f"(random = {random_baseline:.4f})")
print(f"test ROC-AUC: {metrics['test_roc_auc']:.4f}")
print(f"@ val-maxF1 threshold {threshold:.4f} on test: "
      f"P={metrics['test_precision']:.3f} "
      f"R={metrics['test_recall']:.3f} "
      f"F1={metrics['test_f1']:.3f}  "
      f"alerts={metrics['test_alerts']:,} (TP={tp:,} FP={fp:,})")

print("\ntop 10 features:")
imp = pd.Series(model.feature_importances_, index=X_cols)
for name, v in imp.sort_values(ascending=False).head(10).items():
    print(f"  {name:<24} {v}")

model.booster_.save_model("models/baseline_lgbm.txt")
with open("models/baseline_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)
print("\nwrote models/baseline_lgbm.txt, models/baseline_metrics.json")

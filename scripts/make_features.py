"""Tracer — Phase 1: per-account features + the canonical split.

Builds label-free behavioral features for every account and the
FIXED stratified train/val/test split (60/20/20, seed 42) that every
model — tabular baseline and GNNs — must use from here on.

Outputs (data/processed/):
  features.parquet — node_id, features..., is_illicit, split
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

SEED = 42
OUT = "data/processed"

print("loading ...")
trans = pd.read_parquet(f"{OUT}/transactions.parquet")
nodes = pd.read_parquet(f"{OUT}/accounts.parquet")

trans["is_self"] = (trans["src"] == trans["dst"]).astype(int)
t0 = trans["timestamp"].min()
trans["hours"] = (trans["timestamp"] - t0).dt.total_seconds() / 3600.0

# ---------------- outgoing (account as sender) ----------------
print("aggregating outgoing ...")
out_g = trans.groupby("src")
out_f = pd.DataFrame({
    "out_tx": out_g.size(),
    "out_amount_sum": out_g["amount_paid"].sum(),
    "out_amount_mean": out_g["amount_paid"].mean(),
    "out_amount_max": out_g["amount_paid"].max(),
    "out_amount_std": out_g["amount_paid"].std(),
    "out_unique_dst": out_g["dst"].nunique(),
    "out_unique_currencies": out_g["pay_currency"].nunique(),
    "out_unique_formats": out_g["payment_format"].nunique(),
    "out_self_loops": out_g["is_self"].sum(),
    "out_first_h": out_g["hours"].min(),
    "out_last_h": out_g["hours"].max(),
})

# ---------------- incoming (account as receiver) ----------------
print("aggregating incoming ...")
in_g = trans.groupby("dst")
in_f = pd.DataFrame({
    "in_tx": in_g.size(),
    "in_amount_sum": in_g["amount_received"].sum(),
    "in_amount_mean": in_g["amount_received"].mean(),
    "in_amount_max": in_g["amount_received"].max(),
    "in_amount_std": in_g["amount_received"].std(),
    "in_unique_src": in_g["src"].nunique(),
    "in_unique_currencies": in_g["recv_currency"].nunique(),
    "in_first_h": in_g["hours"].min(),
    "in_last_h": in_g["hours"].max(),
})

print("joining ...")
feat = (
    nodes.set_index("node_id")
    .join(out_f, how="left")
    .join(in_f, how="left")
)

# Derived ratios / velocities (guarding div-by-zero)
feat["active_hours"] = (
    feat[["out_last_h", "in_last_h"]].max(axis=1)
    - feat[["out_first_h", "in_first_h"]].min(axis=1)
).clip(lower=1.0)
feat["total_tx"] = feat["out_tx"].fillna(0) + feat["in_tx"].fillna(0)
feat["tx_per_day"] = feat["total_tx"] / (feat["active_hours"] / 24.0)
feat["flow_ratio"] = feat["out_amount_sum"].fillna(0) / (
    feat["in_amount_sum"].fillna(0) + 1.0
)
feat["fan_out_ratio"] = feat["out_unique_dst"].fillna(0) / (
    feat["out_tx"].fillna(0) + 1.0
)
feat["fan_in_ratio"] = feat["in_unique_src"].fillna(0) / (
    feat["in_tx"].fillna(0) + 1.0
)

feat = feat.fillna(0.0).reset_index()

# ---------------- the canonical split ----------------
print("splitting (stratified, seed=42) ...")
idx = np.arange(len(feat))
train_idx, tmp_idx = train_test_split(
    idx, test_size=0.4, random_state=SEED,
    stratify=feat["is_illicit"],
)
val_idx, test_idx = train_test_split(
    tmp_idx, test_size=0.5, random_state=SEED,
    stratify=feat["is_illicit"].iloc[tmp_idx],
)
feat["split"] = "train"
feat.loc[val_idx, "split"] = "val"
feat.loc[test_idx, "split"] = "test"

for s in ["train", "val", "test"]:
    sub = feat[feat["split"] == s]
    print(f"  {s:<5} {len(sub):>7,} accounts   "
          f"illicit {int(sub['is_illicit'].sum()):>5,} "
          f"({100 * sub['is_illicit'].mean():.4f}%)")

feat.to_parquet(f"{OUT}/features.parquet", index=False)
n_feats = feat.shape[1] - 3  # minus node_id, is_illicit, split
print(f"\nwrote {OUT}/features.parquet  "
      f"({len(feat):,} accounts x {n_feats} features)")

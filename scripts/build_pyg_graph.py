"""Tracer — Phase 2: build the PyG graph object.

Converts the parquet tables into a single torch_geometric Data object:
  - nodes = accounts, in the exact row order of features.parquet
  - node features = the same 26 tabular features (log1p on heavy-tailed
    columns, then standardized with a scaler FIT ON TRAIN NODES ONLY)
  - edges = unique directed (src, dst) pairs + reverse edges so
    message passing flows both ways (edge direction kept as a flag)
  - masks = the canonical train/val/test split from Phase 1

Same features, same split as the baseline -> any lift is attributable
to the graph structure, nothing else.

Output: data/processed/graph.pt
"""

import numpy as np
import pandas as pd
import torch
from torch_geometric.data import Data

OUT = "data/processed"

print("loading ...")
feat = pd.read_parquet(f"{OUT}/features.parquet")
trans = pd.read_parquet(f"{OUT}/transactions.parquet")

drop = ["node_id", "is_illicit", "split"]
X_cols = [c for c in feat.columns if c not in drop]

# ---------------- node index ----------------
node_ids = feat["node_id"].values
idx = {nid: i for i, nid in enumerate(node_ids)}
n = len(node_ids)
print(f"nodes: {n:,}")

# ---------------- features (leakage-safe scaling) ----------------
X = feat[X_cols].to_numpy(dtype=np.float64, copy=True)
# log1p the heavy-tailed columns (counts & amounts), keep ratios/hours
heavy = [i for i, c in enumerate(X_cols)
         if any(k in c for k in ("amount", "_tx", "unique", "self_loops",
                                 "total"))]
X[:, heavy] = np.log1p(np.clip(X[:, heavy], 0, None))

train_mask_np = (feat["split"] == "train").values
mu = X[train_mask_np].mean(axis=0)
sd = X[train_mask_np].std(axis=0)
sd[sd == 0] = 1.0
X = (X - mu) / sd
x = torch.tensor(X, dtype=torch.float32)

# ---------------- edges ----------------
print("building edges ...")
edges = trans[["src", "dst"]].drop_duplicates()
src = edges["src"].map(idx).to_numpy()
dst = edges["dst"].map(idx).to_numpy()

# forward + reverse so information flows both directions
edge_index = torch.tensor(
    np.concatenate([np.stack([src, dst]), np.stack([dst, src])], axis=1),
    dtype=torch.long,
)
# direction flag as edge feature: 1 = real direction, 0 = reversed
edge_dir = torch.cat([torch.ones(len(src)), torch.zeros(len(src))])
print(f"directed unique edges: {len(src):,}  "
      f"(edge_index with reverses: {edge_index.shape[1]:,})")

# ---------------- labels + masks ----------------
y = torch.tensor(feat["is_illicit"].values, dtype=torch.long)
masks = {}
for s in ["train", "val", "test"]:
    m = torch.tensor((feat["split"] == s).values, dtype=torch.bool)
    masks[f"{s}_mask"] = m
    print(f"  {s:<5} {int(m.sum()):>7,} nodes  "
          f"illicit {int(y[m].sum()):>5,}")

data = Data(x=x, edge_index=edge_index, y=y,
            edge_dir=edge_dir.unsqueeze(1),
            **masks)
data.node_ids = list(node_ids)  # for later ring extraction / SARs
print(data)

torch.save(data, f"{OUT}/graph.pt")
print(f"wrote {OUT}/graph.pt")

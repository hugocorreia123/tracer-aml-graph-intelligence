"""Tracer — Phase 2: GraphSAGE node classifier.

Full-batch 2-layer GraphSAGE on the account graph. Same 26 features,
same canonical split as the LightGBM baseline — the only new
information is the graph structure. Early stopping on val PR-AUC;
final report on test vs the baseline.

Outputs:
  models/gnn_sage.pt         — best model weights
  models/gnn_sage_metrics.json
  data/processed/gnn_scores.parquet — per-node scores (for Phase 4)
"""

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.metrics import average_precision_score, roc_auc_score
from torch_geometric.nn import SAGEConv

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)
Path("models").mkdir(exist_ok=True)

# ---------------- device ----------------
if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
print(f"device: {device}")

data = torch.load("data/processed/graph.pt", weights_only=False)
node_ids = data.node_ids
data = data.to(device)


class SAGE(torch.nn.Module):
    def __init__(self, d_in, d_hid=128, dropout=0.3):
        super().__init__()
        self.conv1 = SAGEConv(d_in, d_hid)
        self.conv2 = SAGEConv(d_hid, d_hid)
        self.head = torch.nn.Linear(d_hid, 2)
        self.dropout = dropout

    def forward(self, x, edge_index):
        h = F.relu(self.conv1(x, edge_index))
        h = F.dropout(h, p=self.dropout, training=self.training)
        h = F.relu(self.conv2(h, edge_index))
        h = F.dropout(h, p=self.dropout, training=self.training)
        return self.head(h)


model = SAGE(data.x.size(1)).to(device)
opt = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=5e-5)
class_weight = torch.tensor([1.0, 20.0], device=device)

best_val = -1.0
best_state = None
patience, bad = 30, 0
t0 = time.time()

for epoch in range(1, 1501):
    model.train()
    opt.zero_grad()
    out = model(data.x, data.edge_index)
    loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask],
                           weight=class_weight)
    loss.backward()
    opt.step()

    if epoch % 5 == 0 or epoch == 1:
        model.eval()
        with torch.no_grad():
            logits = model(data.x, data.edge_index)
            prob = F.softmax(logits, dim=1)[:, 1].cpu().numpy()
        yv = data.y[data.val_mask].cpu().numpy()
        pv = prob[data.val_mask.cpu().numpy()]
        val_pr = average_precision_score(yv, pv)
        marker = ""
        if val_pr > best_val:
            best_val = val_pr
            best_state = {k: v.detach().cpu().clone()
                          for k, v in model.state_dict().items()}
            bad = 0
            marker = "  *best*"
        else:
            bad += 1
        print(f"epoch {epoch:>3}  loss {loss.item():.4f}  "
              f"val PR-AUC {val_pr:.4f}{marker}")
        if bad >= patience:
            print("early stop")
            break

print(f"\ntraining time: {time.time() - t0:.0f}s")
model.load_state_dict(best_state)
model.eval()
with torch.no_grad():
    logits = model(data.x, data.edge_index)
    prob = F.softmax(logits, dim=1)[:, 1].cpu().numpy()

metrics = {"val_pr_auc": float(best_val)}
y_np = data.y.cpu().numpy()
for s in ["val", "test"]:
    m = getattr(data, f"{s}_mask").cpu().numpy()
    metrics[f"{s}_pr_auc"] = float(average_precision_score(y_np[m], prob[m]))
    metrics[f"{s}_roc_auc"] = float(roc_auc_score(y_np[m], prob[m]))

baseline = json.loads(Path("models/baseline_metrics.json").read_text())
lift = metrics["test_pr_auc"] / baseline["test_pr_auc"]

print("\n" + "=" * 52)
print("GRAPHSAGE RESULTS vs BASELINE (same features, same split)")
print("=" * 52)
print(f"test PR-AUC  GraphSAGE: {metrics['test_pr_auc']:.4f}")
print(f"test PR-AUC  LightGBM : {baseline['test_pr_auc']:.4f}")
print(f"lift: {lift:.2f}x")
print(f"test ROC-AUC GraphSAGE: {metrics['test_roc_auc']:.4f}")

torch.save(best_state, "models/gnn_sage.pt")
with open("models/gnn_sage_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)
pd.DataFrame({"node_id": node_ids, "gnn_score": prob,
              "is_illicit": y_np}).to_parquet(
    "data/processed/gnn_scores.parquet", index=False)
print("\nwrote models/gnn_sage.pt, models/gnn_sage_metrics.json, "
      "data/processed/gnn_scores.parquet")

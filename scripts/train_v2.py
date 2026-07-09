"""Tracer — Phase 3: configurable GNN trainer (SAGE / GATv2).

Every run trains on the canonical split, early-stops on val PR-AUC,
evaluates on test, and APPENDS its config+metrics to
models/experiments.json so runs are comparable side by side.

Examples:
  uv run python scripts/train_v2.py --name sage_tuned \
      --arch sage --layers 3 --hidden 256 --lr 3e-3 --pos-weight 5
  uv run python scripts/train_v2.py --name gat \
      --arch gat --layers 2 --hidden 128 --heads 4 --lr 3e-3

Outputs per run:
  models/{name}.pt, entry in models/experiments.json,
  data/processed/scores_{name}.parquet
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.metrics import average_precision_score, roc_auc_score
from torch_geometric.nn import SAGEConv, GATv2Conv

p = argparse.ArgumentParser()
p.add_argument("--name", required=True)
p.add_argument("--arch", choices=["sage", "gat"], default="sage")
p.add_argument("--layers", type=int, default=2)
p.add_argument("--hidden", type=int, default=128)
p.add_argument("--heads", type=int, default=4)          # gat only
p.add_argument("--dropout", type=float, default=0.3)
p.add_argument("--lr", type=float, default=3e-3)
p.add_argument("--weight-decay", type=float, default=5e-5)
p.add_argument("--pos-weight", type=float, default=20.0)
p.add_argument("--epochs", type=int, default=800)
p.add_argument("--patience", type=int, default=30)       # eval rounds
p.add_argument("--seed", type=int, default=42)
p.add_argument("--cpu", action="store_true")
args = p.parse_args()

torch.manual_seed(args.seed)
np.random.seed(args.seed)
Path("models").mkdir(exist_ok=True)

if args.cpu:
    device = torch.device("cpu")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
print(f"run={args.name}  device={device}")
print(vars(args))

data = torch.load("data/processed/graph.pt", weights_only=False)
node_ids = data.node_ids
data = data.to(device)


class GNN(torch.nn.Module):
    def __init__(self, d_in, a):
        super().__init__()
        self.convs = torch.nn.ModuleList()
        d = d_in
        for i in range(a.layers):
            if a.arch == "sage":
                self.convs.append(SAGEConv(d, a.hidden))
                d = a.hidden
            else:
                self.convs.append(
                    GATv2Conv(d, a.hidden // a.heads, heads=a.heads))
                d = (a.hidden // a.heads) * a.heads
        self.head = torch.nn.Linear(d, 2)
        self.dropout = a.dropout

    def forward(self, x, edge_index):
        h = x
        for conv in self.convs:
            h = F.relu(conv(h, edge_index))
            h = F.dropout(h, p=self.dropout, training=self.training)
        return self.head(h)


model = GNN(data.x.size(1), args).to(device)
n_params = sum(p_.numel() for p_ in model.parameters())
print(f"params: {n_params:,}")

opt = torch.optim.Adam(model.parameters(), lr=args.lr,
                       weight_decay=args.weight_decay)
sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs)
class_weight = torch.tensor([1.0, args.pos_weight], device=device)

best_val, best_state, bad = -1.0, None, 0
t0 = time.time()

for epoch in range(1, args.epochs + 1):
    model.train()
    opt.zero_grad()
    out = model(data.x, data.edge_index)
    loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask],
                           weight=class_weight)
    loss.backward()
    opt.step()
    sched.step()

    if epoch % 5 == 0 or epoch == 1:
        model.eval()
        with torch.no_grad():
            prob = F.softmax(model(data.x, data.edge_index),
                             dim=1)[:, 1].cpu().numpy()
        m = data.val_mask.cpu().numpy()
        val_pr = average_precision_score(data.y.cpu().numpy()[m], prob[m])
        marker = ""
        if val_pr > best_val:
            best_val, bad = val_pr, 0
            best_state = {k: v.detach().cpu().clone()
                          for k, v in model.state_dict().items()}
            marker = "  *best*"
        else:
            bad += 1
        if epoch % 25 == 0 or marker or epoch == 1:
            print(f"epoch {epoch:>4}  loss {loss.item():.4f}  "
                  f"val PR-AUC {val_pr:.4f}{marker}")
        if bad >= args.patience:
            print("early stop")
            break

train_s = time.time() - t0
print(f"training time: {train_s:.0f}s")

model.load_state_dict(best_state)
model.eval()
with torch.no_grad():
    prob = F.softmax(model(data.x, data.edge_index),
                     dim=1)[:, 1].cpu().numpy()

y_np = data.y.cpu().numpy()
res = {"name": args.name, "config": vars(args) | {"params": n_params},
       "train_seconds": round(train_s)}
for s in ["val", "test"]:
    m = getattr(data, f"{s}_mask").cpu().numpy()
    res[f"{s}_pr_auc"] = float(average_precision_score(y_np[m], prob[m]))
    res[f"{s}_roc_auc"] = float(roc_auc_score(y_np[m], prob[m]))

exp_path = Path("models/experiments.json")
exps = json.loads(exp_path.read_text()) if exp_path.exists() else []
exps = [e for e in exps if e["name"] != args.name] + [res]
exp_path.write_text(json.dumps(exps, indent=2, default=str))

torch.save(best_state, f"models/{args.name}.pt")
pd.DataFrame({"node_id": node_ids, "gnn_score": prob,
              "is_illicit": y_np}).to_parquet(
    f"data/processed/scores_{args.name}.parquet", index=False)

print("\n" + "=" * 60)
print(f"{'run':<14}{'test PR-AUC':>12}{'val PR-AUC':>12}{'time':>8}")
print("-" * 60)
print(f"{'lgbm baseline':<14}{0.3710:>12.4f}{0.3717:>12.4f}{'-':>8}")
print(f"{'sage (ph2)':<14}{0.5034:>12.4f}{0.4867:>12.4f}{'78m':>8}")
for e in exps:
    print(f"{e['name']:<14}{e['test_pr_auc']:>12.4f}"
          f"{e['val_pr_auc']:>12.4f}{str(e['train_seconds'])+'s':>8}")

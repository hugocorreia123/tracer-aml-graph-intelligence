"""Tracer — Phase 0: raw CSV -> clean parquet + account graph.

Outputs (data/processed/):
  transactions.parquet  — cleaned edges with composite node ids
  accounts.parquet      — node table (one row per (bank, account))
  patterns.parquet      — laundering-attempt ground truth with typology
  graph_stats.txt       — headline numbers for the README

Node identity: account numbers repeat across banks in AMLworld,
so a node is the composite (bank, account) pair.
"""

import re
from pathlib import Path

import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------
# 1. Transactions -> clean edge table
# ---------------------------------------------------------------
print("loading transactions ...")
trans = pd.read_csv(
    RAW / "HI-Small_Trans.csv",
    dtype={"From Bank": str, "To Bank": str,
           "Account": str, "Account.1": str},
)
trans.columns = [
    "timestamp", "from_bank", "from_acct", "to_bank", "to_acct",
    "amount_received", "recv_currency", "amount_paid", "pay_currency",
    "payment_format", "is_laundering",
]
trans["timestamp"] = pd.to_datetime(trans["timestamp"],
                                    format="%Y/%m/%d %H:%M")

# Composite node ids (bank + account)
def norm_bank(s: pd.Series) -> pd.Series:
    out = s.str.lstrip("0")
    return out.where(out != "", "0")

trans["from_bank"] = norm_bank(trans["from_bank"])
trans["to_bank"] = norm_bank(trans["to_bank"])
trans["src"] = trans["from_bank"] + "_" + trans["from_acct"]
trans["dst"] = trans["to_bank"] + "_" + trans["to_acct"]

n_rows = len(trans)
n_illicit = int(trans["is_laundering"].sum())
n_self = int((trans["src"] == trans["dst"]).sum())
print(f"  rows: {n_rows:,}  illicit: {n_illicit:,} "
      f"({100 * n_illicit / n_rows:.4f}%)  self-loops: {n_self:,}")

trans.to_parquet(OUT / "transactions.parquet", index=False)

# ---------------------------------------------------------------
# 2. Node table
# ---------------------------------------------------------------
print("building node table ...")
nodes = pd.DataFrame(
    {"node_id": pd.concat([trans["src"], trans["dst"]]).unique()}
)
# An account is "illicit" if it touches any laundering transaction
illicit_nodes = set(trans.loc[trans["is_laundering"] == 1, "src"]) | set(
    trans.loc[trans["is_laundering"] == 1, "dst"]
)
nodes["is_illicit"] = nodes["node_id"].isin(illicit_nodes).astype(int)
n_nodes = len(nodes)
n_illicit_nodes = int(nodes["is_illicit"].sum())
print(f"  nodes: {n_nodes:,}  illicit nodes: {n_illicit_nodes:,} "
      f"({100 * n_illicit_nodes / n_nodes:.4f}%)")
nodes.to_parquet(OUT / "accounts.parquet", index=False)

# ---------------------------------------------------------------
# 3. Patterns file -> typology ground truth
# ---------------------------------------------------------------
print("parsing patterns ...")
pattern_rows = []
attempt_id = -1
typology = None
begin_re = re.compile(r"^BEGIN LAUNDERING ATTEMPT - ([A-Z\- ]+?)\s*(?::|$)")

with open(RAW / "HI-Small_Patterns.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        m = begin_re.match(line)
        if m:
            attempt_id += 1
            typology = m.group(1).strip()
            continue
        if line.startswith("END LAUNDERING ATTEMPT"):
            typology = None
            continue
        if typology is not None:
            p = line.split(",")
            # timestamp,from_bank,from_acct,to_bank,to_acct,...
            pattern_rows.append({
                "attempt_id": attempt_id,
                "typology": typology,
                "timestamp": p[0],
                "src": p[1].lstrip("0") + "_" + p[2]
                       if p[1].lstrip("0") else "0_" + p[2],
                "dst": p[3].lstrip("0") + "_" + p[4]
                       if p[3].lstrip("0") else "0_" + p[4],
                "amount_paid": float(p[7]),
                "pay_currency": p[8],
            })

patterns = pd.DataFrame(pattern_rows)
patterns["timestamp"] = pd.to_datetime(patterns["timestamp"],
                                       format="%Y/%m/%d %H:%M")
print(f"  attempts: {patterns['attempt_id'].nunique():,}  "
      f"pattern transactions: {len(patterns):,}")
print("  typology counts (attempts):")
tc = patterns.groupby("typology")["attempt_id"].nunique()
for t, c in tc.sort_values(ascending=False).items():
    print(f"    {t:<16} {c:>5}")
patterns.to_parquet(OUT / "patterns.parquet", index=False)

# ---------------------------------------------------------------
# 4. Graph stats (networkx on the deduped edge list)
# ---------------------------------------------------------------
print("building graph ...")
import networkx as nx

edges = trans.groupby(["src", "dst"]).size().reset_index(name="n_tx")
G = nx.from_pandas_edgelist(edges, "src", "dst",
                            edge_attr="n_tx",
                            create_using=nx.DiGraph)
n_e = G.number_of_edges()
n_n = G.number_of_nodes()
wcc = max(nx.weakly_connected_components(G), key=len)
degs = [d for _, d in G.degree()]
stats = [
    f"nodes:                {n_n:,}",
    f"unique edges:         {n_e:,}  (from {n_rows:,} transactions)",
    f"largest weakly-connected component: {len(wcc):,} nodes "
    f"({100 * len(wcc) / n_n:.2f}%)",
    f"mean degree:          {sum(degs) / n_n:.2f}",
    f"max degree:           {max(degs):,}",
    f"illicit transactions: {n_illicit:,} ({100 * n_illicit / n_rows:.4f}%)",
    f"illicit accounts:     {n_illicit_nodes:,} "
    f"({100 * n_illicit_nodes / n_nodes:.4f}%)",
    f"laundering attempts (patterns file): "
    f"{patterns['attempt_id'].nunique():,}",
]
print()
print("=" * 50)
print("GRAPH STATS")
print("=" * 50)
for s in stats:
    print(s)
(OUT / "graph_stats.txt").write_text("\n".join(stats) + "\n")
print(f"\nwrote {OUT}/transactions.parquet, accounts.parquet, "
      f"patterns.parquet, graph_stats.txt")

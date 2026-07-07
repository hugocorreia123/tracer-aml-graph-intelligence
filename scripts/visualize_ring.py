"""Tracer — Phase 0: visualize one laundering ring.

Picks a CYCLE attempt from the patterns ground truth, pulls its
accounts plus their 1-hop legitimate neighborhood from the full
transaction graph, and draws it: ring in red, context in grey.

Output: docs/first_ring.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

OUT = Path("docs")
OUT.mkdir(exist_ok=True)

trans = pd.read_parquet("data/processed/transactions.parquet")
patterns = pd.read_parquet("data/processed/patterns.parquet")

# ---- pick a mid-sized CYCLE attempt --------------------------------
cycles = patterns[patterns["typology"] == "CYCLE"]
sizes = cycles.groupby("attempt_id").size()
attempt_id = sizes[(sizes >= 6) & (sizes <= 10)].index[0]
ring = patterns[patterns["attempt_id"] == attempt_id]
ring_nodes = set(ring["src"]) | set(ring["dst"])
print(f"attempt {attempt_id}: CYCLE with {len(ring)} transactions, "
      f"{len(ring_nodes)} accounts")

# ---- 1-hop context around the ring ---------------------------------
mask = trans["src"].isin(ring_nodes) | trans["dst"].isin(ring_nodes)
local = trans[mask]
# cap context so the plot stays readable
context_edges = (
    local[local["is_laundering"] == 0]
    .groupby(["src", "dst"]).size().reset_index(name="n")
    .head(120)
)
print(f"context: {len(context_edges)} legitimate edges around the ring")

G = nx.DiGraph()
for _, r in context_edges.iterrows():
    G.add_edge(r["src"], r["dst"], illicit=False)
for _, r in ring.iterrows():
    G.add_edge(r["src"], r["dst"], illicit=True)

pos = nx.spring_layout(G, seed=42, k=0.35)

fig, ax = plt.subplots(figsize=(11, 8))
other_nodes = [n for n in G.nodes if n not in ring_nodes]
nx.draw_networkx_nodes(G, pos, nodelist=other_nodes, node_size=25,
                       node_color="#b0b0b0", alpha=0.6, ax=ax)
nx.draw_networkx_nodes(G, pos, nodelist=list(ring_nodes), node_size=140,
                       node_color="#d62728", ax=ax)
legit = [(u, v) for u, v, d in G.edges(data=True) if not d["illicit"]]
illic = [(u, v) for u, v, d in G.edges(data=True) if d["illicit"]]
nx.draw_networkx_edges(G, pos, edgelist=legit, edge_color="#c0c0c0",
                       width=0.6, alpha=0.5, arrows=False, ax=ax)
nx.draw_networkx_edges(G, pos, edgelist=illic, edge_color="#d62728",
                       width=2.2, arrows=True, arrowsize=14, ax=ax)

ax.set_title(
    f"Money-laundering CYCLE (attempt {attempt_id}) hidden in the "
    f"transaction network\n"
    f"red = laundering ring ({len(ring)} transfers, "
    f"{len(ring_nodes)} accounts) · grey = surrounding legitimate flows",
    fontsize=11,
)
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "first_ring.png", dpi=150)
print(f"wrote {OUT}/first_ring.png")

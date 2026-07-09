"""Tracer — Phase 5: agentic SAR investigator.

A ReAct agent (LangGraph + Groq, qwen3-32b) investigates flagged
rings. Per ring it can query the evidence through tools, must
identify the laundering typology, and drafts a structured
Suspicious Activity Report. Every draft is stamped
PENDING HUMAN REVIEW — the AI suggests, a human decides & files.

Rings are ranked by mean GNN score x motif strength (purity lesson
from Phase 4: size/amount alone over-selects noise).

Usage:
  uv run python scripts/investigate.py --top 5
  uv run python scripts/investigate.py --ring-id 73

Outputs: sars/ring_{id}.json + sars/ring_{id}.md
"""

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

load_dotenv()
assert os.environ.get("GROQ_API_KEY"), "GROQ_API_KEY missing (.env)"

MODEL = "qwen/qwen3-32b"
MOTIF_STRENGTH = {"CYCLE": 1.0, "GATHER-SCATTER": 0.9, "FAN-OUT": 0.8,
                  "FAN-IN": 0.8, "MIXED": 0.4}

rings = {r["ring_id"]: r for r in
         json.loads(Path("data/processed/rings.json").read_text())}
feat = pd.read_parquet("data/processed/features.parquet").set_index(
    "node_id")

CURRENT_RING: dict = {}   # set per investigation


# ---------------- tools ----------------
@tool
def get_ring_summary() -> str:
    """Summary of the ring under investigation: size, transaction count,
    total USD amount, currencies, payment formats, time window, mean GNN
    suspicion score, and detected structural motifs."""
    r = CURRENT_RING
    return json.dumps({k: r[k] for k in
                       ["ring_id", "n_accounts", "n_edges", "n_tx",
                        "total_amount", "currencies", "formats",
                        "t_start", "t_end", "mean_gnn_score"]})


@tool
def get_flows(limit: int = 30) -> str:
    """Money flows (edges) inside the ring, largest first. Each item:
    src account, dst account, number of transactions, total USD amount."""
    edges = sorted(CURRENT_RING["edges"], key=lambda e: -e["amount"])
    return json.dumps(edges[:limit])


@tool
def get_account_profile(account_id: str) -> str:
    """Behavioral profile of one account: transaction counts, in/out
    amounts, unique counterparties, velocity, flow ratio (out/in)."""
    if account_id not in feat.index:
        return json.dumps({"error": f"unknown account {account_id}"})
    row = feat.loc[account_id]
    cols = ["out_tx", "in_tx", "out_amount_sum", "in_amount_sum",
            "out_unique_dst", "in_unique_src", "tx_per_day",
            "flow_ratio", "fan_out_ratio", "fan_in_ratio"]
    return json.dumps({c: round(float(row[c]), 3) for c in cols})

@tool
def get_structure() -> str:
    """Degree structure of the ring: per-account counts of distinct
    receivers (out_deg) and senders (in_deg) inside the ring, plus any
    directed cycles found (as account lists). Raw structure only — no
    interpretation."""
    import networkx as nx
    r = CURRENT_RING
    H = nx.DiGraph()
    for e in r["edges"]:
        H.add_edge(e["src"], e["dst"])
    cycles = []
    try:
        cycles = [c for c in nx.simple_cycles(H, length_bound=12)
                  if len(c) >= 3][:3]
    except Exception:
        pass
    return json.dumps({
        "out_deg": dict(H.out_degree()),
        "in_deg": dict(H.in_degree()),
        "cycles_found": cycles,
    })

SYSTEM = """You are an AML (anti-money-laundering) investigator agent.
You are given ONE flagged ring of accounts detected by a graph neural
network in a transaction network. Investigate it using your tools, then
produce a Suspicious Activity Report draft.

Typology definitions:
- CYCLE: funds move A->B->...->A, returning to origin (layering loop).
- FAN-OUT: one account rapidly disperses funds to many accounts.
- FAN-IN: many accounts funnel funds into one account.
- GATHER-SCATTER: funds gather into a hub, then scatter out again.
- SCATTER-GATHER: funds scatter from a source, later re-gather.
- BIPARTITE: a set of senders each pays a set of receivers (layer).
- STACK: chained bipartite layers.
- MIXED/UNCLEAR: structure does not clearly match one typology.

Rules:
- Use the tools; base EVERY claim on tool evidence. Never invent
  accounts, amounts, or dates.
- If evidence is weak or the structure looks like normal business,
  SAY SO and set recommendation to "dismiss" — false accusations
  have real costs. Not every flagged ring is laundering.
- End with EXACTLY one JSON block fenced as ```json ... ``` with keys:
  typology (string), confidence (0-1), summary (2-3 sentences),
  key_evidence (list of short strings citing accounts/amounts/timing),
  recommendation ("file_sar" | "monitor" | "dismiss").
"""

llm = ChatGroq(model=MODEL, temperature=0.0, max_retries=8,
               reasoning_format="hidden")
agent = create_react_agent(
    llm, [get_ring_summary, get_flows, get_account_profile,
          get_structure])


def investigate(ring_id: int) -> dict:
    global CURRENT_RING
    CURRENT_RING = rings[ring_id]
    task = (f"{SYSTEM}\n\nInvestigate ring {ring_id} "
            f"({CURRENT_RING['n_accounts']} accounts). "
            f"Use get_ring_summary first.")
    result = agent.invoke(
        {"messages": [("user", task)]},
        config={"recursion_limit": 40},
    )
    final = result["messages"][-1].content
    m = re.search(r"```json\s*(\{.*?\})\s*```", final, re.DOTALL)
    verdict = json.loads(m.group(1)) if m else {"parse_error": final[-500:]}
    n_tools = sum(1 for msg in result["messages"]
                  if getattr(msg, "tool_calls", None))
    return {"ring_id": ring_id,
            "status": "DRAFT — PENDING HUMAN REVIEW",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "model": MODEL,
            "agent_steps": len(result["messages"]),
            "tool_calling_turns": n_tools,
            "verdict": verdict,
            "narrative": final}


def to_markdown(sar: dict) -> str:
    v = sar["verdict"]
    r = rings[sar["ring_id"]]
    lines = [
        f"# SAR draft — Ring {sar['ring_id']}",
        f"**{sar['status']}**  ·  generated {sar['generated_at']} "
        f"by {sar['model']}",
        "",
        f"- Accounts: {r['n_accounts']}  ·  Transactions: {r['n_tx']}  "
        f"·  Total: ${r['total_amount']:,.0f}",
        f"- Window: {r['t_start']} → {r['t_end']}",
        f"- Detected typology: **{v.get('typology', '?')}** "
        f"(confidence {v.get('confidence', '?')})",
        f"- Recommendation: **{v.get('recommendation', '?')}**",
        "",
        "## Summary",
        v.get("summary", ""),
        "",
        "## Key evidence",
        *[f"- {e}" for e in v.get("key_evidence", [])],
        "",
        "## Full narrative",
        sar["narrative"],
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=0,
                    help="investigate top-N ranked rings")
    ap.add_argument("--ring-id", type=int, default=None)
    args = ap.parse_args()

    Path("sars").mkdir(exist_ok=True)
    if args.ring_id is not None:
        targets = [args.ring_id]
    else:
        ranked = sorted(
            rings.values(),
            key=lambda r: -(r["mean_gnn_score"]
                            * MOTIF_STRENGTH[r["motif_label"]]
                            * min(r["n_accounts"], 10)))
        targets = [r["ring_id"] for r in ranked[:args.top or 5]]

    print(f"investigating rings: {targets}")
    for rid in targets:
        print(f"\n--- ring {rid} "
              f"({rings[rid]['n_accounts']} accts, "
              f"{rings[rid]['motif_label']}) ---")
        sar = investigate(rid)
        Path(f"sars/ring_{rid}.json").write_text(
            json.dumps(sar, indent=2))
        Path(f"sars/ring_{rid}.md").write_text(to_markdown(sar))
        v = sar["verdict"]
        print(f"  typology: {v.get('typology')}  "
              f"confidence: {v.get('confidence')}  "
              f"recommendation: {v.get('recommendation')}  "
              f"({sar['tool_calling_turns']} tool turns)")
    print("\nwrote sars/ring_*.json + .md")

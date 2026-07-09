"""Tracer — Phase 7 (slim): serving API.

Lean FastAPI over the precomputed artifacts:
  GET  /health                     — status + model/artifact versions
  GET  /score/{node_id}            — GNN suspicion score for an account
  GET  /rings?limit=20             — top rings by investigation priority
  GET  /rings/{ring_id}            — full evidence bundle for one ring
  POST /rings/{ring_id}/sar        — run the investigator, return the
                                     SAR draft (PENDING HUMAN REVIEW)

Run:  uv run uvicorn scripts.serve:app --port 8000
Docs: http://localhost:8000/docs
"""

import json
import sys
import time
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException

sys.path.insert(0, "scripts")

app = FastAPI(title="Tracer — AML Graph Intelligence",
              description="GNN ring detection + agentic SAR drafting. "
                          "AI suggests; a human decides and files.",
              version="0.1.0")

MOTIF_STRENGTH = {"CYCLE": 1.0, "GATHER-SCATTER": 0.9, "FAN-OUT": 0.8,
                  "FAN-IN": 0.8, "MIXED": 0.4}

scores = pd.read_parquet(
    "data/processed/scores_sage_tuned.parquet").set_index("node_id")
rings = {r["ring_id"]: r for r in
         json.loads(Path("data/processed/rings.json").read_text())}
for r in rings.values():
    r["priority"] = (r["mean_gnn_score"]
                     * MOTIF_STRENGTH[r["motif_label"]]
                     * min(r["n_accounts"], 10))
ranked = sorted(rings.values(), key=lambda r: -r["priority"])

_investigate = None  # lazy import: agent deps only load if SAR requested


@app.get("/health")
def health():
    return {"status": "ok", "detector": "sage_tuned (test PR-AUC 0.519)",
            "n_accounts_scored": int(len(scores)),
            "n_rings": len(rings)}


@app.get("/score/{node_id}")
def score(node_id: str):
    if node_id not in scores.index:
        raise HTTPException(404, f"unknown account {node_id}")
    return {"node_id": node_id,
            "gnn_score": float(scores.loc[node_id, "gnn_score"])}


@app.get("/rings")
def list_rings(limit: int = 20):
    return [{k: r[k] for k in
             ["ring_id", "n_accounts", "n_tx", "total_amount",
              "motif_label", "mean_gnn_score", "priority"]}
            for r in ranked[:limit]]


@app.get("/rings/{ring_id}")
def ring_detail(ring_id: int):
    if ring_id not in rings:
        raise HTTPException(404, f"unknown ring {ring_id}")
    return rings[ring_id]


@app.post("/rings/{ring_id}/sar")
def draft_sar(ring_id: int):
    global _investigate
    if ring_id not in rings:
        raise HTTPException(404, f"unknown ring {ring_id}")
    cached = Path(f"sars/ring_{ring_id}.json")
    if cached.exists():
        return json.loads(cached.read_text())
    if _investigate is None:
        from investigate import investigate as _inv  # noqa: PLC0415
        _investigate = _inv
    t0 = time.time()
    sar = _investigate(ring_id)
    sar["latency_s"] = round(time.time() - t0, 1)
    Path("sars").mkdir(exist_ok=True)
    cached.write_text(json.dumps(sar, indent=2))
    return sar

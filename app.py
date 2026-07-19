"""Tracer — AML Graph Intelligence: interactive demo.

Ring explorer (network view + SAR panel) and the evaluation results.
Reads committed artifacts from app_data/ and models/ — no training,
no data downloads. Live SAR drafting activates only when a
GROQ_API_KEY is configured; otherwise pre-drafted SARs are shown.

Run:  uv run streamlit run app.py
"""

import json
import os
from pathlib import Path

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Tracer — AML Graph Intelligence",
                   layout="wide", page_icon="🕸️")

import tracer_theme as th
th.inject()

MOTIF_STRENGTH = {"CYCLE": 1.0, "GATHER-SCATTER": 0.9, "FAN-OUT": 0.8,
                  "FAN-IN": 0.8, "MIXED": 0.4}


@st.cache_data
def load():
    rings = {r["ring_id"]: r for r in
             json.loads(Path("app_data/rings.json").read_text())}
    for r in rings.values():
        r["priority"] = (r["mean_gnn_score"]
                         * MOTIF_STRENGTH[r["motif_label"]]
                         * min(r["n_accounts"], 10))
    op = json.loads(Path("models/operating_point.json").read_text())
    exps = json.loads(Path("models/experiments.json").read_text())
    agree = json.loads(Path("models/agreement.json").read_text())
    inv = json.loads(Path("models/investigator_eval.json").read_text())
    return rings, op, exps, agree, inv


rings, op, exps, agree, inv = load()

import tracer_friendly as tf

if not tf.show_welcome():
    st.stop()

th.hero(
    "AML Graph Intelligence",
    "Tracer",
    "GraphSAGE finds money-laundering rings in a 515,088-account "
    "transaction network; a ReAct agent drafts the Suspicious Activity "
    "Report. AI suggests — a human decides and files.",
    "Synthetic data · IBM AMLworld HI-Small · every number measured",
)

# ---------------- active case — one selector drives every panel ----------------
ranked = sorted(rings.values(), key=lambda r: -r["priority"])
rank_of = {r["ring_id"]: i + 1 for i, r in enumerate(ranked)}
sar_dir = Path("app_data/sars")
investigated = {int(p.stem.split("_")[1])
                for p in sar_dir.glob("ring_*.json")}

options = [r["ring_id"] for r in ranked[:200]]
# surface investigated rings first so the demo has instant SARs
options = sorted(options,
                 key=lambda rid: (rid not in investigated,
                                  -rings[rid]["priority"]))


def fmt(rid):
    r = rings[rid]
    tag = " · SAR ready" if rid in investigated else ""
    return (f"Ring {rid} — {r['motif_label']} · "
            f"{r['n_accounts']} accts · ${r['total_amount']:,.0f}"
            f"{tag}")


rid = st.selectbox("🎯 Active case — pick a flagged ring; every panel "
                   "below follows it", options, format_func=fmt)
r = rings[rid]
_sar_file = sar_dir / f"ring_{rid}.json"
_sar = json.loads(_sar_file.read_text()) if _sar_file.exists() else None


def ring_vitals(r, rank, total, sar):
    """The selected ring's vitals — these change with the case above."""
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Investigation priority", f"#{rank} of {total:,}",
                  r["motif_label"], delta_color="off")
        st.caption("**Means:** where this ring sits in the queue — "
                   "suspicion × motif strength × size.")
    with c2:
        st.metric("Suspicion (mean GNN score)",
                  f"{r['mean_gnn_score']:.3f}")
        st.caption("**Means:** how strongly the graph model flags these "
                   "accounts, averaged over the ring.")
    with c3:
        st.metric("Money moved", f"${r['total_amount']:,.0f}",
                  f"{r['n_accounts']} accts · {r['n_tx']} tx",
                  delta_color="off")
        st.caption(f"**Means:** USD-normalized flow inside the ring, "
                   f"{str(r['t_start'])[:10]} → {str(r['t_end'])[:10]}.")
    with c4:
        if sar:
            v = sar.get("verdict", {})
            rec = str(v.get("recommendation", "?")).replace("_", " ").upper()
            st.metric("Agent recommendation", rec,
                      f"confidence {v.get('confidence', 0):.2f}",
                      delta_color="off")
            st.caption("**Means:** the drafted SAR's call — pending "
                       "human review, never auto-filed.")
        else:
            st.metric("Agent recommendation", "NOT DRAFTED")
            st.caption("**Means:** no SAR for this ring yet — pick one "
                       "marked 'SAR ready', or run the live agent in "
                       "the explorer.")


ring_vitals(r, rank_of[rid], len(rings), _sar)
st.divider()

tab_explore, tab_results, tab_about, tab_help = st.tabs(
    ["🔍 Ring explorer", "📊 Results", "ℹ️ Method", "❓ Help"])

# ------------------------------------------------------------------
with tab_explore:
    left, right = st.columns([3, 2], gap="large")

    with left:
        # ---- network figure ----
        H = nx.DiGraph()
        for e in r["edges"]:
            H.add_edge(e["src"], e["dst"], amount=e["amount"],
                       n_tx=e["n_tx"])
        pos = nx.spring_layout(H, seed=42, k=0.9)

        edge_traces = []
        annotations = []
        for u, v, d in H.edges(data=True):
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_traces.append(go.Scatter(
                x=[x0, x1], y=[y0, y1], mode="lines",
                line=dict(width=max(1, min(6, d["amount"] ** 0.5 / 300)),
                          color="rgba(180,60,60,0.55)"),
                hoverinfo="text",
                text=f"{u} → {v}<br>${d['amount']:,.0f} "
                     f"({d['n_tx']} tx)"))
            annotations.append(dict(
                ax=x0, ay=y0, x=x0 + 0.82 * (x1 - x0),
                y=y0 + 0.82 * (y1 - y0), xref="x", yref="y",
                axref="x", ayref="y", showarrow=True,
                arrowhead=3, arrowsize=1.2, arrowwidth=1.3,
                arrowcolor="rgba(180,60,60,0.75)"))

        deg_in = dict(H.in_degree())
        deg_out = dict(H.out_degree())
        node_x, node_y, node_text = [], [], []
        for n in H.nodes():
            node_x.append(pos[n][0])
            node_y.append(pos[n][1])
            node_text.append(f"{n}<br>in {deg_in[n]} / out {deg_out[n]}")
        node_trace = go.Scatter(
            x=node_x, y=node_y, mode="markers",
            marker=dict(size=[10 + 3 * (deg_in[n] + deg_out[n])
                              for n in H.nodes()],
                        color="#d62728",
                        line=dict(width=1, color="white")),
            hoverinfo="text", text=node_text)

        fig = go.Figure(data=edge_traces + [node_trace])
        fig.update_layout(showlegend=False, annotations=annotations,
                          margin=dict(l=10, r=10, t=10, b=10),
                          height=520,
                          xaxis=dict(visible=False),
                          yaxis=dict(visible=False),
                          plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"{r['n_accounts']} accounts · {r['n_tx']} transactions "
                   f"· ${r['total_amount']:,.0f} (USD-normalized) · "
                   f"{r['t_start']} → {r['t_end']} · mean GNN score "
                   f"{r['mean_gnn_score']:.3f}")

    with right:
        st.subheader("SAR draft")
        sar_path = sar_dir / f"ring_{rid}.json"
        if sar_path.exists():
            sar = json.loads(sar_path.read_text())
            v = sar["verdict"]
            st.error(f"**{sar['status']}**", icon="🧑‍⚖️")
            a, b, c = st.columns(3)
            a.metric("Typology", str(v.get("typology", "?")))
            b.metric("Confidence", f"{v.get('confidence', 0):.2f}")
            c.metric("Recommendation",
                     str(v.get("recommendation", "?")))
            st.markdown("**Summary.** "
                        + str(v.get("summary", "")).replace("$", "\\$"))
            if v.get("key_evidence"):
                st.markdown("**Key evidence**")
                for e in v["key_evidence"]:
                    st.markdown(f"- {str(e).replace('$', chr(92) + '$')}")
            st.caption(f"drafted by {sar['model']} · "
                       f"{sar['tool_calling_turns']} tool-calling turns "
                       f"· generated {sar['generated_at'][:19]}")
        elif os.environ.get("GROQ_API_KEY"):
            if st.button("🔎 Investigate this ring (live agent)"):
                with st.spinner("agent investigating ..."):
                    import sys
                    sys.path.insert(0, "scripts")
                    from investigate import investigate
                    sar = investigate(rid)
                    sar_dir.mkdir(exist_ok=True)
                    sar_path.write_text(json.dumps(sar, indent=2))
                    st.rerun()
        else:
            st.info("No pre-drafted SAR for this ring. Pick one marked "
                    "**SAR ready**, or set GROQ_API_KEY to enable live "
                    "investigation.")

# ------------------------------------------------------------------
with tab_results:
    tf.show_metrics_live(op, agree, inv)
    st.caption("Portfolio-level evaluation — fixed test-set numbers. "
               "The cards above the tabs follow the selected ring.")
    st.divider()
    a, b = st.columns(2)
    with a:
        st.subheader("Detector: PR-AUC (identical features & split)")
        rows = [{"model": "LightGBM (tabular)", "test PR-AUC": 0.371},
                {"model": "GraphSAGE (ph2)", "test PR-AUC": 0.503}]
        rows += [{"model": e["name"], "test PR-AUC": e["test_pr_auc"]}
                 for e in exps]
        df = pd.DataFrame(rows)
        order = ["LightGBM (tabular)", "GraphSAGE (ph2)", "gat", "sage_tuned"]
        df["model"] = pd.Categorical(df["model"], categories=order, ordered=True)
        df = df.sort_values("model")

        df = df.sort_values("model")
        st.bar_chart(df.set_index("model"), height=300)
        st.caption("Random baseline = 0.0123. The +40% lift of "
                   "sage_tuned comes purely from graph structure.")

        st.subheader("False positives at fixed recall (test)")
        df_op = pd.DataFrame(
            [{"recall": f"{r['recall']:.0%}",
              "LightGBM FP": r["lgbm"]["fp"],
              "GraphSAGE FP": r["gnn"]["fp"]} for r in op])
        st.bar_chart(df_op.set_index("recall"), height=300, stack=False)
        st.caption("At 70% recall the GNN produces 47% fewer false "
                   "positives — ≈\\$1.3–3.0M/yr illustrative at 100K "
                   "alerts and \\$30–70/alert.")
    with b:
        st.subheader("Investigator evaluation")
        st.markdown(f"""
| metric | result |
|---|---|
| typology inferred labels-blind | **{inv['correct']}/{inv['n_matched']}** ({inv['typology_accuracy']:.0%}, 3× random over 8 classes) |
| weak rings wrongly escalated | **{inv['weak_escalated']}/{inv['n_weak']}** |
| SAR groundedness (judge mean) | **{agree['judge_mean_score']:.2f}** |
| judge vs blind human labels | **κ = {agree['kappa']:.3f}** (n={agree['n']}, {agree['raw_agreement']:.0%} raw) |
""")
        st.markdown(
            "**Honest finding:** the agent classifies ring structure "
            "well and never over-escalates weak evidence, but its "
            "narratives contain arithmetic or directional errors in "
            "roughly two-thirds of drafts (judge-verified, "
            "human-validated). That measured error rate is exactly why "
            "the human-review gate is architectural, not decorative.")

# ------------------------------------------------------------------
with tab_about:
    tf.show_how_it_works()
    st.markdown("""
**Pipeline.** 5.08M synthetic bank transactions (IBM AMLworld HI-Small)
→ 515K-account directed graph → 3-layer GraphSAGE node scorer (PyTorch
Geometric) → threshold at the 70%-recall operating point → suspicious
subgraphs decomposed into ≤60-account **rings** (recursive Louvain) →
ReAct agent (LangGraph + Groq qwen3-32b) investigates each ring through
evidence tools — typology labels withheld — and drafts a SAR →
**human review**.

**Evaluation.** Detector: PR-AUC on a fixed stratified split vs a
LightGBM baseline on identical features. Investigator: typology
accuracy vs AMLworld ground truth; SAR factual groundedness scored by a
cross-family judge (gpt-oss-120b) validated against blind human labels
(Cohen's κ = 0.94). Methodology reused from
[Voyager](https://github.com/hugocorreia123/voyager).

**Limits.** Synthetic data; single seed; ring decomposition trades
coverage of diffuse typologies (STACK/BIPARTITE) for investigability;
FX normalization uses fixed approximate rates.

Code: [github.com/hugocorreia123/tracer-aml-graph-intelligence](https://github.com/hugocorreia123/tracer-aml-graph-intelligence)
· Hugo Correia — [LinkedIn](https://www.linkedin.com/in/hugogncorreia)
""")

# ------------------------------------------------------------------
with tab_help:
    tf.show_help()

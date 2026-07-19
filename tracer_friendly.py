"""Tracer — the friendly layer.

Drop this next to app.py alongside friendly.py, then add three calls
to app.py (see WIRING at the bottom of this file).

The audience is not an ML engineer. It is a financial-crime analyst,
a compliance officer, or a hiring manager who has thirty seconds. So:
no PR-AUC in the first sentence, no GraphSAGE in the first paragraph.
Say what it does. Then show the number.
"""

import friendly as fr
import streamlit as st

KEY = "tracer"
REPO = "https://github.com/hugocorreia123/tracer-aml-graph-intelligence"


def show_welcome() -> bool:
    """Returns True once dismissed — render the app after that."""
    return fr.welcome(
        key=KEY,
        headline="New here? 30-second tour",
        what_it_does=(
            "**Money laundering doesn't look suspicious one account at "
            "a time.** It looks like a *ring* — money moving in a "
            "circle through a dozen accounts that each look ordinary "
            "on their own. Standard fraud systems check accounts one "
            "by one, so the ring is invisible to them. **Tracer looks "
            "at the network.**"
        ),
        steps=[
            "🕸️ **Pick a flagged account.** You'll see the accounts it "
            "moves money with, and the ones *they* move money with — "
            "the shape is the evidence.",
            "🔍 **The model reads the shape, not the account.** It was "
            "trained on a 515,000-account transaction network, and it "
            "finds rings that account-by-account models miss entirely.",
            "📝 **An AI investigator writes the report** — a draft "
            "Suspicious Activity Report citing the specific "
            "transactions it relied on.",
            "✍️ **You decide.** Nothing is ever filed automatically. "
            "Every draft is stamped for human review, because we "
            "*measured* how often it gets details wrong.",
        ],
        big_idea=(
            "Catching more fraud is easy — flag everything. The hard "
            "part is catching more while crying wolf **less**, because "
            "every false alarm costs an analyst an hour. That's the "
            "number to watch."
        ),
    )


def show_metrics() -> None:
    """The results, in sentences a compliance officer can act on."""
    fr.explain([
        fr.Metric(
            label="Rings found vs the standard approach",
            value="+40%",
            means="It finds substantially more laundering rings than "
                  "an account-by-account model on the same data.",
            good=True,
            technical="Test PR-AUC 0.519 (GraphSAGE) vs 0.371 "
                      "(tabular LightGBM baseline). PR-AUC is the "
                      "right metric under extreme class imbalance.",
        ),
        fr.Metric(
            label="Fewer false alarms",
            value="47% fewer",
            means="At the same catch rate, analysts chase roughly half "
                  "as many dead ends. That is the number that decides "
                  "whether a system gets used.",
            good=True,
            technical="47% reduction in false positives at 70% recall.",
        ),
        fr.Metric(
            label="Is the AI's grader trustworthy?",
            value="κ = 0.94",
            means="A second AI grades the reports, and I checked it "
                  "against my own blind labels. They almost always "
                  "agree — so the grade means something.",
            good=True,
            technical="Cohen's κ = 0.942 between a cross-family "
                      "LLM judge (gpt-oss-120b) and blind human "
                      "labels. Chance-corrected agreement.",
        ),
    ])


def show_how_it_works() -> None:
    st.markdown("#### Why a network, and not a checklist")
    st.markdown(
        "Every account in a laundering ring looks *fine* on its own: "
        "amounts under the threshold, a plausible business, no single "
        "red flag. The crime is the **shape** — money leaving account "
        "A and arriving back near A through eight hops. You cannot see "
        "a shape by looking at one point.\n\n"
        "Tracer builds the transaction network and learns from a "
        "node's **neighbourhood**: who it pays, who they pay, and how "
        "that pattern compares to normal. That is why it finds what "
        "row-by-row models cannot."
    )

    st.markdown("#### The honest comparison")
    st.markdown(
        "I didn't compare against a strawman. The baseline is a tuned "
        "gradient-boosting model with hand-engineered features — the "
        "thing a good team would actually build. **The graph model "
        "beats it by 40%, and I'd have reported it if it hadn't.**"
    )

    st.markdown("#### Why a human still signs off")
    st.markdown(
        "The AI investigator writes a solid report and gets details "
        "wrong often enough that a person must read it. I know that "
        "because I measured it rather than assumed it — and then I "
        "checked the grader too, by hand-labelling reports blind "
        "before looking at its verdicts. **A grader nobody validated "
        "is an opinion with a number on it.**"
    )

    fr.honesty(points=[
        "**Synthetic data.** The transaction network is IBM's AMLSim "
        "benchmark, not a real bank's ledger — real laundering is "
        "messier and rarer.",
        "**A draft, not a filing.** Every report is stamped for human "
        "review. Nothing here files anything.",
        "**The judge is validated, not infallible.** κ = 0.94 is high "
        "agreement, not proof of correctness — it means the human and "
        "the grader see the same thing, not that both are right.",
        "**Not financial-crime advice.** This is an engineering "
        "demonstration.",
    ])


def show_help() -> None:
    fr.help_tab(
        key=KEY,
        what=(
            "**Tracer** finds money-laundering **rings** — groups of "
            "accounts moving money in circles — in a network of "
            "515,000 accounts, and drafts the report an analyst would "
            "otherwise write by hand."
        ),
        how_to=[
            "Pick a flagged account from the list.",
            "Look at the **network** around it — the ring is the "
            "shape, not any single account.",
            "Read the **AI-drafted report** and the transactions it "
            "cites.",
            "Check the **evaluation** tab to see how often it's wrong, "
            "and how I know.",
        ],
        faq=[
            ("Is this real bank data?",
             "No — it's IBM's AMLSim benchmark, a synthetic "
             "transaction network. Real ledgers aren't public, for "
             "obvious reasons."),
            ("What's a 'ring'?",
             "Money leaving an account and returning near it through "
             "several hops, to disguise its origin. Each hop looks "
             "innocent; the loop doesn't."),
            ("Why not just flag more accounts?",
             "Because every false alarm costs an analyst an hour. "
             "Catching more while crying wolf less is the whole "
             "problem — that's why the false-positive number matters "
             "more than the catch rate."),
            ("Does it file reports automatically?",
             "No, and it shouldn't. I measured how often the AI gets "
             "details wrong; that error rate is exactly why a human "
             "reviews every draft."),
            ("Who built this?",
             "Hugo Correia — Data Scientist / ML & AI Engineer, "
             "Lisbon. One of four portfolio projects spanning "
             "finance, industry and law."),
        ],
        built_by="Every error rate in this demo is published, "
                 "including the ones that aren't flattering.",
        repo=REPO,
    )


# ======================================================== WIRING
#
# In app.py, add three things:
#
#   1. at the top, after st.set_page_config(...):
#
#        import tracer_friendly as tf
#        if not tf.show_welcome():
#            st.stop()
#
#      (st.stop() is what makes the tour the first thing a stranger
#       sees rather than a panel they scroll past.)
#
#   2. where the metrics are, replace the bare st.metric row with:
#
#        tf.show_metrics()
#
#   3. add two tabs:
#
#        tab_how, tab_help = st.tabs(["🔬 How it works", "❓ Help"])
#        with tab_how:  tf.show_how_it_works()
#        with tab_help: tf.show_help()
#
# Files to copy into the repo root: friendly.py, tracer_friendly.py


def show_metrics_live(op, agree, inv):
    """Headline metrics computed from the loaded artifacts, with a
    plain-language line under each. Values are never hardcoded."""
    import streamlit as st
    r70 = next(r for r in op if r["recall"] == 0.70)
    fp_cut = 1 - r70["gnn"]["fp"] / r70["lgbm"]["fp"]
    avoided = r70["lgbm"]["fp"] - r70["gnn"]["fp"]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("GNN vs tabular (test PR-AUC)", "0.519 vs 0.371", "+40%")
        st.caption("**Means:** identical features, identical split — the entire lift comes from the network structure.")
    with c2:
        st.metric("False positives @ 70% recall", f"\u2212{fp_cut:.0%}", f"{avoided:,} alerts avoided")
        st.caption(f"**Means:** at the same catch rate, {avoided:,} wasted investigations simply disappear.")
    with c3:
        st.metric("Judge validity (Cohen's \u03ba)", f"{agree['kappa']:.3f}", f"n={agree['n']} blind human labels")
        st.caption("**Means:** the AI judge grading the SARs was itself checked against blind human labels — near-perfect agreement, so its scores can be trusted.")
    with c4:
        st.metric("Weak rings wrongly escalated", f"{inv['weak_escalated']}/{inv['n_weak']}")
        st.caption("**Means:** none of the deliberately weak control rings was pushed to filing — the agent knows when not to escalate.")

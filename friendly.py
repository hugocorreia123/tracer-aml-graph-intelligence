"""friendly — a plain-language layer for technical demos.

The problem this solves, learned the hard way on four projects: the
people who would actually buy or hire for this work are not ML
engineers. They are lawyers, compliance officers, maintenance
planners, fraud analysts and recruiters. A demo that opens with
"PR-AUC 0.519 vs 0.371" has already lost them — not because they are
incapable, but because nobody arrives knowing your vocabulary.

The fix is not dumbing down. It is ordering: say what the thing DOES,
then what to WATCH FOR, then let the numbers land on a reader who now
has somewhere to put them.

Five components, each learned from a real mistake:

  welcome()      a tour that appears once and can be replayed. It
                 survives st.rerun because it lives in session state,
                 not in a flag someone forgets to set.
  explain()      a metric with its plain-language meaning attached —
                 because a number without a sentence is decoration.
  ladder()       a capability table with a "does this affect me?"
                 column. On the legal demo that column was "does my
                 document leave the machine?" and it was the only one
                 anyone read.
  honesty()      the limitations box. Every demo has one; most hide
                 it. Putting it in the UI is the differentiator, not
                 the risk.
  help_tab()     "what am I looking at", the FAQ, and the replay
                 button.

Drop this file next to your app and import it. No dependencies beyond
streamlit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import streamlit as st


# ---------------------------------------------------------- welcome
def welcome(
    *,
    key: str,
    headline: str,
    what_it_does: str,
    steps: list[str],
    big_idea: Optional[str] = None,
    button: str = "Got it — let's go",
    where_to_replay: str = "the **Help** tab",
) -> bool:
    """A tour shown once per session, replayable, that BLOCKS the app
    until dismissed.

    Blocking is deliberate. A tour in a sidebar is a tour nobody
    reads; the whole point is that the first thing a stranger sees is
    an explanation, not a control panel.

    Returns True when the tour has been dismissed (i.e. render the
    rest of the app).
    """
    flag = f"_seen_{key}"
    if flag not in st.session_state:
        st.session_state[flag] = False
    if st.session_state[flag]:
        return True

    with st.container(border=True):
        st.markdown(f"### 👋 {headline}")
        st.markdown(what_it_does)
        st.markdown("**What makes it different — try it and watch:**")
        for i, s in enumerate(steps, 1):
            st.markdown(f"{i}. {s}")
        if big_idea:
            st.markdown(f"> **The big idea:** {big_idea}")
        c1, c2 = st.columns([1, 4])
        if c1.button(button, type="primary", key=f"btn_{key}"):
            st.session_state[flag] = True
            st.rerun()
        c2.caption(f"You can reopen this anytime from {where_to_replay}.")
    return False


def replay_button(key: str, label: str = "🔄 Replay the welcome tour"):
    if st.button(label, key=f"replay_{key}"):
        st.session_state[f"_seen_{key}"] = False
        st.rerun()


# ---------------------------------------------------------- metrics
@dataclass
class Metric:
    """A number and the sentence that makes it mean something."""
    label: str          # plain language, not the variable name
    value: str
    means: str          # what a reader should conclude
    good: Optional[bool] = None      # colour the conclusion
    technical: str = ""              # the jargon, for those who want it


def explain(metrics: list[Metric], columns: int = 0) -> None:
    """Metrics with their meaning attached.

    st.metric alone shows "0.519" and trusts the reader to know that
    is good. Most don't. The `means` line is the component.
    """
    cols = st.columns(columns or len(metrics))
    for c, m in zip(cols, metrics):
        with c:
            st.metric(m.label, m.value,
                      help=m.technical or None)
            icon = ("✅" if m.good else "⚠️") if m.good is not None else ""
            st.caption(f"{icon} {m.means}")


# ----------------------------------------------------------- ladder
@dataclass
class Rung:
    name: str
    what_it_is: str
    matters: str        # the column a non-technical reader reads
    available: Optional[bool] = None


def ladder(rungs: list[Rung], *, matters_header: str,
           intro: str = "", note: str = "") -> None:
    """A capability table whose third column answers 'does this affect
    me?'.

    On the legal demo that column was "does my document leave the
    machine?" — and it was the only column anyone read. Pick the
    question your reader actually has; it is rarely 'which model'.
    """
    if intro:
        st.markdown(intro)
    header = f"| Mode | What it is | {matters_header} |"
    sep = "|---|---|---|"
    rows = []
    for r in rungs:
        mark = ""
        if r.available is not None:
            mark = " 🟢" if r.available else " ⚫"
        rows.append(f"| {r.name}{mark} | {r.what_it_is} | {r.matters} |")
    st.markdown("\n".join([header, sep] + rows))
    if note:
        st.caption(note)


# ---------------------------------------------------------- honesty
def honesty(*, title: str = "What this demo is — and isn't",
            points: list[str], closing: str = "") -> None:
    """The limitations box, IN the UI.

    Every project has limitations; most bury them in a README section
    nobody scrolls to. Putting them on the screen is the
    differentiator, not the risk: a demo that names its own edges is
    the only kind a professional trusts.
    """
    with st.expander(f"⚖️ {title}"):
        for p in points:
            st.markdown(f"- {p}")
        if closing:
            st.markdown(f"\n{closing}")


# --------------------------------------------------------- help tab
def help_tab(*, key: str, what: str, how_to: list[str],
             faq: list[tuple[str, str]], built_by: str,
             repo: Optional[str] = None,
             more: Optional[str] = None) -> None:
    """'What am I looking at', the FAQ, and the replay button."""
    st.markdown("#### What am I looking at?")
    st.markdown(what)
    st.markdown("**How to use this demo**")
    for i, s in enumerate(how_to, 1):
        st.markdown(f"{i}. {s}")
    st.markdown("**Common questions**")
    for q, a in faq:
        st.markdown(f"- **{q}** {a}")
    if more:
        st.markdown(more)
    st.markdown(f"*{built_by}*")
    replay_button(key)
    if repo:
        st.markdown(f"[⭐ View the code on GitHub]({repo})")


# ------------------------------------------------------ house style
def header(*, icon: str, title: str, one_liner: str,
           status: str = "") -> None:
    """One line that says what the thing does, in words a stranger
    knows. Not the tagline — the function."""
    st.markdown(
        f"<h1 style='margin-bottom:0'>{icon} {title}</h1>"
        f"<p style='color:#8b949e;margin-top:2px;font-size:1.05rem'>"
        f"{one_liner}</p>", unsafe_allow_html=True)
    if status:
        st.caption(status)


def caveat(text: str) -> None:
    """A one-line honesty note under a result. Use it often."""
    st.caption(f"⚖️ {text}")

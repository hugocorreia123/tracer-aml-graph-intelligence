"""Tracer — AML Graph Intelligence — visual theme.

Palette, type and signature backdrop for this project's live demo.
Streamlit only. Pair with .streamlit/config.toml (base widget theme).
"""

import streamlit as st

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@600;800&family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Archivo', sans-serif; letter-spacing: .01em; }

.stApp {
  background:
    url('data:image/svg+xml;utf8,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%22360%22%20height%3D%22360%22%3E%3Cg%20stroke%3D%22%238FA8C4%22%20stroke-opacity%3D%220.07%22%20fill%3D%22none%22%3E%3Cpath%20d%3D%22M20%2060%20L120%2030%20L210%2090%20L330%2050%22/%3E%3Cpath%20d%3D%22M40%20300%20L150%20250%20L260%20320%20L340%20270%22/%3E%3Cpath%20d%3D%22M120%2030%20L150%20250%20M210%2090%20L260%20320%22/%3E%3C/g%3E%3Cg%20fill%3D%22%238FA8C4%22%20fill-opacity%3D%220.10%22%3E%3Ccircle%20cx%3D%2220%22%20cy%3D%2260%22%20r%3D%223%22/%3E%3Ccircle%20cx%3D%22120%22%20cy%3D%2230%22%20r%3D%224%22/%3E%3Ccircle%20cx%3D%22210%22%20cy%3D%2290%22%20r%3D%223%22/%3E%3Ccircle%20cx%3D%22330%22%20cy%3D%2250%22%20r%3D%224%22/%3E%3Ccircle%20cx%3D%2240%22%20cy%3D%22300%22%20r%3D%224%22/%3E%3Ccircle%20cx%3D%22150%22%20cy%3D%22250%22%20r%3D%223%22/%3E%3Ccircle%20cx%3D%22260%22%20cy%3D%22320%22%20r%3D%224%22/%3E%3Ccircle%20cx%3D%22340%22%20cy%3D%22270%22%20r%3D%223%22/%3E%3C/g%3E%3Cg%20stroke%3D%22%23E5484D%22%20stroke-opacity%3D%220.10%22%20fill%3D%22none%22%3E%3Cpath%20d%3D%22M90%20160%20L170%20130%20L230%20180%20L180%20220%20L100%20205%20Z%22/%3E%3C/g%3E%3Cg%20fill%3D%22%23E5484D%22%20fill-opacity%3D%220.14%22%3E%3Ccircle%20cx%3D%2290%22%20cy%3D%22160%22%20r%3D%223.5%22/%3E%3Ccircle%20cx%3D%22170%22%20cy%3D%22130%22%20r%3D%223.5%22/%3E%3Ccircle%20cx%3D%22230%22%20cy%3D%22180%22%20r%3D%223.5%22/%3E%3Ccircle%20cx%3D%22180%22%20cy%3D%22220%22%20r%3D%223.5%22/%3E%3Ccircle%20cx%3D%22100%22%20cy%3D%22205%22%20r%3D%223.5%22/%3E%3C/g%3E%3C/svg%3E') repeat,
    radial-gradient(1100px 500px at 85% -10%, rgba(90,169,230,0.10), transparent 60%),radial-gradient(900px 500px at -10% 110%, rgba(229,72,77,0.06), transparent 55%),linear-gradient(180deg, #0D1B2A 0%, #0B1624 100%);
  background-attachment: fixed;
}
[data-testid="stHeader"] { background: transparent; }

/* hero */
.tr-hero {
  border-radius: 18px;
  padding: 26px 30px 24px 30px;
  margin: 4px 0 14px 0;
  background: linear-gradient(135deg, rgba(23,41,61,0.92) 0%, rgba(13,27,42,0.92) 70%);
  border: 1px solid #5AA9E640;
  box-shadow: 0 12px 40px -18px #5AA9E659;
}
.tr-hero .eyebrow {
  font-family: 'Inter', sans-serif;
  font-size: .72rem; font-weight: 700; letter-spacing: .22em;
  text-transform: uppercase; color: #5AA9E6; margin-bottom: 6px;
}
.tr-hero h1 {
  font-family: 'Archivo', sans-serif;
  font-size: clamp(1.7rem, 3.2vw, 2.5rem); font-weight: 800;
  margin: 0 0 8px 0; padding: 0; color: #E8F1F8; line-height: 1.08;
}
.tr-hero .tag { color: #9FB4C8; font-size: 1.0rem; max-width: 72ch; margin: 0; }
.tr-hero .meta { color: #9FB4C8; opacity: .8; font-size: .8rem; margin-top: 10px; letter-spacing: .04em; }

/* metric cards */
[data-testid="stMetric"] {
  background: rgba(23, 41, 61, 0.55);
  border: 1px solid #ffffff1c;
  border-left: 3px solid #5AA9E6;
  border-radius: 14px;
  padding: 14px 16px 12px 16px;
}
[data-testid="stMetricLabel"] p {
  text-transform: uppercase; letter-spacing: .07em;
  font-size: .74rem; font-weight: 700; color: #9FB4C8;
}
[data-testid="stMetricValue"] { font-family: 'Archivo', sans-serif; color: #E8F1F8; }

/* tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #ffffff1c; }
.stTabs [data-baseweb="tab"] {
  padding: 10px 16px; font-weight: 600; border-radius: 10px 10px 0 0;
}
.stTabs [aria-selected="true"] {
  color: #5AA9E6 !important;
  box-shadow: inset 0 -2px 0 #5AA9E6;
  background: #5AA9E614;
}

/* buttons */
.stButton > button { border-radius: 12px; font-weight: 600; }
button[kind="primary"], [data-testid="stBaseButton-primary"] {
  background: linear-gradient(135deg, #5AA9E6 0%, #3E7BC0 100%);
  color: #07121F; border: 0;
}
button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
  filter: brightness(1.08);
}

/* containers */
[data-testid="stExpander"] {
  border: 1px solid #ffffff1c; border-radius: 12px; background: rgba(23, 41, 61, 0.55);
}
[data-testid="stImage"] img { border-radius: 12px; border: 1px solid #ffffff1c; }
[data-testid="stCaptionContainer"], .stCaption { color: #9FB4C8; }
[data-testid="stSidebar"] { background: #0B1826; border-right: 1px solid #ffffff1c; }
hr { border-color: #ffffff1c; }
[data-testid="stDataFrame"] { border: 1px solid #ffffff1c; border-radius: 12px; }

/* ---------- motion layer: Apple-quiet, minimal ---------- */
html { scroll-behavior: smooth; }

.tr-hero, [data-testid="stMetric"], [data-testid="stExpander"] {
  backdrop-filter: blur(12px) saturate(1.15);
  -webkit-backdrop-filter: blur(12px) saturate(1.15);
}

[data-testid="stMetric"], .stButton > button, [data-testid="stExpander"] {
  transition: transform .28s cubic-bezier(.22,.61,.36,1),
              box-shadow .28s cubic-bezier(.22,.61,.36,1),
              border-color .28s ease, filter .2s ease;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-3px);
  border-color: #5AA9E666;
  box-shadow: 0 16px 38px -18px #5AA9E659;
}
.stButton > button:hover { transform: translateY(-1px); }
.stButton > button:active { transform: translateY(0) scale(.99); }

@media (prefers-reduced-motion: no-preference) {
  @keyframes tr-rise {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: none; }
  }
  @keyframes tr-fade { from { opacity: 0; } to { opacity: 1; } }

  .tr-hero { animation: tr-rise .7s cubic-bezier(.22,.61,.36,1) both; }
  [data-testid="stMetric"] { animation: tr-rise .6s cubic-bezier(.22,.61,.36,1) both; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] { animation-delay: .06s; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] { animation-delay: .14s; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] { animation-delay: .22s; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(4) [data-testid="stMetric"] { animation-delay: .30s; }
  .stTabs { animation: tr-fade .5s ease-out both; animation-delay: .15s; }

  @supports (animation-timeline: view()) {
    [data-testid="stPlotlyChart"], [data-testid="stImage"],
    [data-testid="stExpander"], [data-testid="stDataFrame"] {
      animation: tr-rise .7s cubic-bezier(.22,.61,.36,1) both;
      animation-timeline: view();
      animation-range: entry 0% entry 38%;
    }
  }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
"""


def inject() -> None:
    """Apply the theme. Call once, right after st.set_page_config."""
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


def hero(eyebrow: str, title: str, tag: str, meta: str = "") -> None:
    """The styled header banner. Replaces st.title + st.caption."""
    meta_html = f'<div class="meta">{meta}</div>' if meta else ""
    st.markdown(
        f'''<div class="tr-hero">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{title}</h1>
  <p class="tag">{tag}</p>
  {meta_html}
</div>''',
        unsafe_allow_html=True,
    )

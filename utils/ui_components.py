"""
utils/ui_components.py
Reusable HTML/CSS components rendered via st.markdown.
"""

import streamlit as st
from pathlib import Path


# ── Load CSS ──────────────────────────────────────────────────────────────────
def load_css():
    css_path = Path(__file__).parent.parent / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ── Navigation bar ────────────────────────────────────────────────────────────
def render_navbar(active_page: str = "Home"):
    pages = ["Home", "About", "Features", "Prediction", "Contact"]
    links_html = ""
    for p in pages:
        active_cls = "active" if p == active_page else ""
        links_html += f'<span class="cg-nav-link {active_cls}">{p}</span>'

    st.markdown(f"""
    <div class="cg-nav">
      <div class="cg-nav-logo">❤️ Cardio<span>Guard</span> AI</div>
      <div class="cg-nav-links" style="display:none;">{links_html}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
def render_footer():
    st.markdown("""
    <div class="cg-footer">
      <div>
        <div style="font-family:var(--font-head);font-weight:700;color:var(--white);margin-bottom:.25rem;">
          ❤️ CardioGuard <span style="color:var(--teal)">AI</span>
        </div>
        <div class="cg-footer-copy">
          AI-Powered Cardiovascular Risk Prediction · Built with Streamlit &amp; scikit-learn
        </div>
      </div>
      <div class="cg-footer-copy">© 2025 CardioGuard AI. For educational use only.</div>
    </div>
    """, unsafe_allow_html=True)


# ── Section header ────────────────────────────────────────────────────────────
def section_header(title: str, subtitle: str = ""):
    sub_html = f'<div class="cg-subheading anim-fade-up">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    {sub_html}
    <div class="cg-section-title anim-fade-up anim-delay-1">{title}</div>
    <div class="cg-divider"></div>
    """, unsafe_allow_html=True)


# ── Feature card ──────────────────────────────────────────────────────────────
def feature_card(icon: str, title: str, desc: str, color: str = "teal"):
    st.markdown(f"""
    <div class="cg-card cg-card-{color} anim-fade-up"
         style="display:flex;gap:1rem;align-items:flex-start;margin-bottom:.8rem;">
      <div class="cg-icon-circle">{icon}</div>
      <div>
        <div style="font-family:var(--font-head);font-weight:700;font-size:1rem;
                    margin-bottom:.4rem;color:var(--white);">{title}</div>
        <div class="cg-body">{desc}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Stat card ─────────────────────────────────────────────────────────────────
def stat_card(value: str, label: str, icon: str = ""):
    st.markdown(f"""
    <div class="cg-metric">
      <div style="font-size:1.6rem;margin-bottom:.3rem;">{icon}</div>
      <div class="cg-metric-value">{value}</div>
      <div class="cg-metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Progress bar ──────────────────────────────────────────────────────────────
def progress_bar(pct: float, color: str = "teal", label: str = ""):
    # pct can be 0-1 or 0-100; normalise to 0-100
    if pct <= 1.0:
        width = round(min(100, max(0, pct * 100)), 1)
    else:
        width = round(min(100, max(0, pct)), 1)

    st.markdown(f"""
    <div style="margin-bottom:.5rem;">
      <div style="display:flex;justify-content:space-between;font-size:.82rem;
           color:rgba(244,248,255,.65);margin-bottom:.35rem;">
        <span>{label}</span><span>{width}%</span>
      </div>
      <div class="cg-progress-wrap">
        <div class="cg-progress-bar cg-progress-{color}" style="width:{width}%"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Info box ─────────────────────────────────────────────────────────────────
def info_box(text: str, color: str = "teal"):
    palette = {
        "teal":   ("rgba(0,201,177,.12)",  "rgba(0,201,177,.35)",  "var(--teal)"),
        "red":    ("rgba(232,69,69,.12)",   "rgba(232,69,69,.35)",   "var(--red)"),
        "green":  ("rgba(46,204,113,.12)",  "rgba(46,204,113,.35)",  "var(--green)"),
        "orange": ("rgba(243,156,18,.12)",  "rgba(243,156,18,.35)",  "var(--orange)"),
    }
    bg, bdr, clr = palette.get(color, palette["teal"])
    st.markdown(f"""
    <div style="background:{bg};border:1px solid {bdr};border-radius:10px;
                padding:.9rem 1.2rem;color:{clr};font-size:.9rem;margin:.4rem 0;">
      {text}
    </div>
    """, unsafe_allow_html=True)

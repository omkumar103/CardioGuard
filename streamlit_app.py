"""
app.py — CardioGuard AI Main Entry Point
Animated landing screen → multi-page navigation.
"""

import time
import streamlit as st
from utils.ui_components import load_css, render_navbar

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardioGuard AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load global CSS ────────────────────────────────────────────────────────────
load_css()

# ── Health facts for landing screen ───────────────────────────────────────────
HEALTH_FACTS = [
    "Heart disease is the leading cause of death globally — 18 million lives annually.",
    "Regular exercise reduces cardiovascular risk by up to 35%.",
    "High blood pressure affects 1 in 3 adults worldwide.",
    "80% of premature heart attacks and strokes are preventable.",
]

# ── Session state defaults ─────────────────────────────────────────────────────
if "landing_done" not in st.session_state:
    st.session_state.landing_done = False
if "page" not in st.session_state:
    st.session_state.page = "Home"


# ══════════════════════════════════════════════════════════════════════════════
#  LANDING SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.landing_done:
    placeholder = st.empty()

    for i, fact in enumerate(HEALTH_FACTS):
        pct = int((i + 1) / len(HEALTH_FACTS) * 100)
        with placeholder.container():
            st.markdown(f"""
            <style>
              section[data-testid="stSidebar"] {{ display: none !important; }}
              .block-container {{ padding: 0 !important; }}
            </style>

            <div style="
              display:flex; flex-direction:column; align-items:center; justify-content:center;
              min-height:100vh; padding:2rem;
              background: radial-gradient(ellipse at 50% 40%, rgba(0,201,177,.10) 0%, transparent 70%),
                          var(--navy);
            ">
              <div class="anim-heart" style="font-size:5rem; margin-bottom:1.5rem;">❤️</div>

              <div class="cg-heading" style="font-size:3.2rem; margin-bottom:.6rem; text-align:center;">
                CardioGuard AI
              </div>
              <div style="font-size:1.1rem; color:rgba(244,248,255,.6); margin-bottom:3rem; text-align:center;
                           letter-spacing:.06em; font-family:var(--font-head);">
                AI-POWERED CARDIOVASCULAR RISK PREDICTION
              </div>

              <div style="
                max-width:600px; width:100%;
                background:rgba(0,201,177,.07); border:1px solid rgba(0,201,177,.25);
                border-radius:16px; padding:1.6rem 2rem; text-align:center;
                margin-bottom:3rem; animation: fadeInUp .6s ease;
              ">
                <div style="font-size:.72rem; color:var(--teal); letter-spacing:.14em;
                     font-weight:700; margin-bottom:.6rem; font-family:var(--font-head);">
                  DID YOU KNOW?
                </div>
                <div style="font-size:1.05rem; color:var(--white); line-height:1.7;">
                  {fact}
                </div>
              </div>

              <div style="width:320px; max-width:90vw;">
                <div style="display:flex; justify-content:space-between; font-size:.78rem;
                     color:rgba(244,248,255,.45); margin-bottom:.5rem;">
                  <span>Loading CardioGuard AI…</span>
                  <span>{pct}%</span>
                </div>
                <div style="background:rgba(255,255,255,.08); border-radius:99px; height:6px; overflow:hidden;">
                  <div style="width:{pct}%; height:100%; border-radius:99px;
                       background:linear-gradient(90deg, var(--teal-dim), var(--teal));"></div>
                </div>
              </div>

              <div style="margin-top:1.5rem; font-size:.75rem; color:rgba(244,248,255,.3);
                   letter-spacing:.08em; font-family:var(--font-head);">
                FACT {i+1} OF {len(HEALTH_FACTS)}
              </div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.85)

    placeholder.empty()
    st.session_state.landing_done = True
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════════════════════

render_navbar(active_page=st.session_state.page)

NAV_PAGES = ["Home", "About", "Features", "Prediction", "Contact"]

# ── Functional tab navigation ──────────────────────────────────────────────────
st.radio(
    label="Navigation",
    options=NAV_PAGES,
    index=NAV_PAGES.index(st.session_state.page),
    horizontal=True,
    label_visibility="collapsed",
    key="nav_radio",
)
if st.session_state.nav_radio != st.session_state.page:
    st.session_state.page = st.session_state.nav_radio
    st.rerun()

# ── Global UI Cleanup ────────────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container { padding-top: 1rem !important; }
  header[data-testid="stHeader"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── Route to page ──────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "Home":
    from pages import home
    home.render()
elif page == "About":
    from pages import about
    about.render()
elif page == "Features":
    from pages import features
    features.render()
elif page == "Prediction":
    from pages import prediction
    prediction.render()
elif page == "Contact":
    from pages import contact
    contact.render()

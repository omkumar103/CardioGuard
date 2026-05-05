"""
pages/home.py
Premium hero dashboard homepage.
"""

import streamlit as st
from utils.ui_components import render_footer, section_header, feature_card


def render():
    # ── Hero section ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="cg-hero">
      <div class="anim-fade-up">
        <div class="cg-badge">🏥 AI-Powered Health Technology</div>
      </div>

      <h1 class="cg-heading anim-fade-up anim-delay-1"
          style="font-size:clamp(2.4rem,5vw,3.5rem);margin:.8rem 0;">
        CardioGuard AI
      </h1>

      <p class="anim-fade-up anim-delay-2"
         style="font-size:1.15rem;color:rgba(244,248,255,.65);
                max-width:560px;line-height:1.7;margin-bottom:2rem;">
        Predict your cardiovascular disease risk in seconds using
        state-of-the-art machine learning. Enter your vitals — get
        instant, interpretable insights.
      </p>

      <div class="anim-fade-up anim-delay-3"
           style="display:flex;gap:.8rem;flex-wrap:wrap;margin-bottom:3rem;">
        <div class="cg-badge" style="font-size:.88rem;padding:.45rem 1.2rem;">
          ✅ 72.9% Model Accuracy
        </div>
        <div class="cg-badge"
             style="font-size:.88rem;padding:.45rem 1.2rem;
                    background:rgba(46,204,113,.12);
                    border-color:rgba(46,204,113,.35);color:var(--green);">
          🔬 Gradient Boosting + Random Forest
        </div>
        <div class="cg-badge"
             style="font-size:.88rem;padding:.45rem 1.2rem;
                    background:rgba(243,156,18,.12);
                    border-color:rgba(243,156,18,.35);color:var(--orange);">
          ⚡ Real-Time Prediction
        </div>
      </div>

      <!-- ECG decorative line -->
      <svg viewBox="0 0 800 60" xmlns="http://www.w3.org/2000/svg"
           style="position:absolute;bottom:0;left:0;right:0;width:100%;opacity:.18;pointer-events:none;">
        <polyline
          points="0,30 60,30 80,30 100,10 110,50 120,10 130,50 140,30 200,30 260,30
                  280,30 300,10 310,50 320,10 330,50 340,30 400,30 460,30
                  480,30 500,10 510,50 520,10 530,50 540,30 600,30 660,30
                  680,30 700,10 710,50 720,10 730,50 740,30 800,30"
          fill="none" stroke="#00C9B1" stroke-width="2"/>
      </svg>
    </div>
    """, unsafe_allow_html=True)

    # ── Key metrics row ────────────────────────────────────────────────────────
    st.markdown('<div class="cg-section" style="padding-top:2rem;padding-bottom:1rem;">',
                unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="cg-metric anim-fade-up">
          <div style="font-size:1.4rem">🌍</div>
          <div class="cg-metric-value">18M+</div>
          <div class="cg-metric-label">Annual CVD Deaths</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="cg-metric anim-fade-up anim-delay-1">
          <div style="font-size:1.4rem">🤖</div>
          <div class="cg-metric-value">72.9%</div>
          <div class="cg-metric-label">Prediction Accuracy</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="cg-metric anim-fade-up anim-delay-2">
          <div style="font-size:1.4rem">📊</div>
          <div class="cg-metric-value">13</div>
          <div class="cg-metric-label">Health Features Analysed</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="cg-metric anim-fade-up anim-delay-3">
          <div style="font-size:1.4rem">⚡</div>
          <div class="cg-metric-value">&lt;1s</div>
          <div class="cg-metric-label">Prediction Time</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Why CardioGuard ────────────────────────────────────────────────────────
    st.markdown('<div class="cg-section">', unsafe_allow_html=True)
    section_header("Why CardioGuard AI?", "BUILT FOR IMPACT")

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        feature_card("⚡", "Instant Predictions",
                     "Get cardiovascular risk assessment in under a second, powered by "
                     "an ensemble of trained ML models.", "teal")
        feature_card("🧠", "AI-Based Analysis",
                     "Gradient Boosting & Random Forest models trained on 70,000 clinical "
                     "health records for reliable insights.", "teal")

    with col_b:
        feature_card("📈", "Health Insights",
                     "Beyond predictions — understand your BMI, blood pressure category, "
                     "pulse pressure, and key risk drivers.", "green")
        feature_card("🔒", "Privacy First",
                     "All analysis happens locally in your session. No health data is "
                     "stored or transmitted anywhere.", "orange")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── CTA ────────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:3rem 2rem 2rem;">
      <div class="cg-heading" style="font-size:2rem;margin-bottom:1rem;">
        Ready to check your heart health?
      </div>
      <div class="cg-body"
           style="margin-bottom:2rem;max-width:480px;margin-left:auto;margin-right:auto;">
        Navigate to the <strong style="color:var(--teal)">Prediction</strong> page and enter
        your health vitals to get an instant AI-powered cardiovascular risk assessment.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA button (functional Streamlit button) ───────────────────────────────
    col_cta = st.columns([2, 1, 2])[1]
    with col_cta:
        if st.button("🔮  Start Prediction Now", use_container_width=True):
            st.session_state.page = "Prediction"
            st.rerun()

    render_footer()

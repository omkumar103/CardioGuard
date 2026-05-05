"""
pages/contact.py
Clean contact / developer info page.
"""

import streamlit as st
from utils.ui_components import render_footer, section_header


def render():
    st.markdown('<div class="cg-section">', unsafe_allow_html=True)
    section_header("Get In Touch", "CONTACT")

    col_a, col_b = st.columns([2, 1], gap="large")

    with col_a:
        st.markdown("""
        <div class="cg-card anim-fade-up">
          <div class="cg-subheading" style="margin-bottom:.8rem;">👋 About the Developer</div>
          <div class="cg-body">
            CardioGuard AI was designed and built as a demonstration of applying machine
            learning to preventive healthcare. The project combines clinical domain
            knowledge with modern data science techniques to build an accessible,
            interpretable risk prediction tool.
          </div>
          <div class="cg-body" style="margin-top:.8rem;">
            Feel free to reach out for collaborations, feedback, or queries related to
            the project.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        contacts = [
            ("📧", "Email",    "om084547@gmail.com",      "mailto:om084547@gmail.com"),
            ("💼", "LinkedIn", "linkedin.com/in/dev",      "https://www.linkedin.com/in/om-kumar-96bb11294/"),
            ("🐙", "GitHub",   "github.com/cardioguard",   "https://github.com/omkumar103/CardioGuard"),
        ]

        for icon, label, display, href in contacts:
            st.markdown(f"""
            <a href="{href}" target="_blank" style="text-decoration:none;">
              <div class="cg-card anim-fade-up"
                   style="display:flex;align-items:center;gap:1.2rem;
                          padding:1rem 1.5rem;margin-bottom:.6rem;cursor:pointer;">
                <div class="cg-icon-circle" style="flex-shrink:0;">{icon}</div>
                <div>
                  <div class="cg-label">{label}</div>
                  <div style="font-weight:600;color:var(--teal);margin-top:.15rem;">
                    {display}
                  </div>
                </div>
                <div style="margin-left:auto;color:rgba(244,248,255,.35);font-size:.9rem;">
                  →
                </div>
              </div>
            </a>
            """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="cg-card cg-card-teal anim-fade-up"
             style="text-align:center;padding:2rem 1.2rem;">
          <div style="font-size:3rem;margin-bottom:.8rem;">🏥</div>
          <div style="font-family:var(--font-head);font-weight:800;
                      font-size:1.2rem;margin-bottom:.5rem;color:var(--white);">
            CardioGuard AI
          </div>
          <div class="cg-body" style="font-size:.88rem;">
            AI-Powered Cardiovascular Risk Prediction
          </div>
          <div class="cg-divider"></div>
          <div style="display:flex;flex-direction:column;gap:.5rem;">
            <div class="cg-badge" style="justify-content:center;">🐍 Python</div>
            <div class="cg-badge" style="justify-content:center;">🎈 Streamlit</div>
            <div class="cg-badge" style="justify-content:center;">🤖 scikit-learn</div>
            <div class="cg-badge" style="justify-content:center;">📊 Ensemble ML</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="cg-card anim-fade-up anim-delay-1">
          <div class="cg-subheading">Project Stats</div>
          <div style="display:flex;flex-direction:column;gap:.4rem;margin-top:.6rem;">
            <div style="display:flex;justify-content:space-between;padding:.4rem 0;
                 border-bottom:1px solid var(--border);">
              <span class="cg-body" style="font-size:.85rem;">Version</span>
              <span style="color:var(--teal);font-weight:600;">1.0.0</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:.4rem 0;
                 border-bottom:1px solid var(--border);">
              <span class="cg-body" style="font-size:.85rem;">Best Accuracy</span>
              <span style="color:var(--green);font-weight:600;">72.9%</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:.4rem 0;
                 border-bottom:1px solid var(--border);">
              <span class="cg-body" style="font-size:.85rem;">Models</span>
              <span style="color:var(--teal);font-weight:600;">2</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:.4rem 0;">
              <span class="cg-body" style="font-size:.85rem;">License</span>
              <span style="color:var(--white);font-weight:600;">MIT</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── FAQ ────────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    section_header("Frequently Asked Questions", "FAQ")

    faqs = [
        ("Is my health data stored?",
         "No. All predictions happen entirely within your browser session. No data is "
         "saved, logged, or sent to any external server."),
        ("How accurate is the prediction?",
         "The best model (Gradient Boosting) achieves 72.9% accuracy on the test set. "
         "While this is a clinically reasonable benchmark, it is not a substitute for "
         "professional diagnosis."),
        ("What dataset was used?",
         "The model was trained on the Cardiovascular Disease Dataset (Kaggle), "
         "containing 70,000 patient records with 11 clinical and lifestyle features."),
        ("Can I use this for medical decisions?",
         "No. CardioGuard AI is for educational and awareness purposes only. Always "
         "consult a qualified healthcare provider for medical advice and diagnosis."),
    ]

    col_l, col_r = st.columns(2, gap="medium")
    for i, (q, a) in enumerate(faqs):
        col = col_l if i % 2 == 0 else col_r
        with col:
            with st.expander(f"❓ {q}"):
                st.markdown(f'<div class="cg-body">{a}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    render_footer()

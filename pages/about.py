"""
pages/about.py
Project overview, dataset, and ML workflow.
"""

import streamlit as st
from utils.ui_components import render_footer, section_header, feature_card, info_box


def render():
    st.markdown('<div class="cg-section">', unsafe_allow_html=True)

    # ── Project Overview ───────────────────────────────────────────────────────
    section_header("About CardioGuard AI", "THE PROJECT")

    col1, col2 = st.columns([2, 1], gap="large")
    with col1:
        st.markdown("""
        <div class="cg-card anim-fade-up">
          <div class="cg-subheading">Overview</div>
          <p class="cg-body" style="margin-top:.5rem;">
            <strong style="color:var(--white)">CardioGuard AI</strong> is a
            machine-learning-powered web application designed to predict an individual's
            risk of cardiovascular disease (CVD) based on clinical and lifestyle
            indicators. The system uses ensemble learning techniques to deliver fast,
            accurate, and interpretable predictions.
          </p>
          <p class="cg-body" style="margin-top:.8rem;">
            The application was built to bridge the gap between complex clinical data and
            accessible health awareness — empowering users to understand their heart
            health risk before it becomes a critical issue.
          </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="cg-card cg-card-teal anim-fade-up anim-delay-1"
             style="text-align:center;">
          <div style="font-size:3rem;margin-bottom:.5rem;" class="anim-heart">❤️</div>
          <div class="cg-metric-value" style="font-size:2.5rem;">72.9%</div>
          <div class="cg-label">Best Model Accuracy</div>
          <div style="height:1rem;"></div>
          <div style="font-size:.85rem;color:rgba(244,248,255,.6);">
            Gradient Boosting Classifier
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Problem Statement ──────────────────────────────────────────────────────
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    section_header("Problem Statement", "WHY IT MATTERS")

    st.markdown("""
    <div class="cg-card anim-fade-up" style="border-left:3px solid var(--teal);">
      <p class="cg-body">
        Cardiovascular diseases are the
        <strong style="color:var(--red)">leading cause of death globally</strong>,
        accounting for over 18 million deaths per year (WHO, 2023). A large proportion
        of these are preventable with early detection and lifestyle modification.
        However, access to clinical diagnostics remains limited for many individuals.
      </p>
      <p class="cg-body" style="margin-top:.8rem;">
        CardioGuard AI provides an accessible, free, and instant risk screening tool
        — enabling preventive health awareness for everyone.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Dataset ────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    section_header("Dataset", "DATA FOUNDATION")

    col_a, col_b, col_c = st.columns(3, gap="medium")
    with col_a:
        st.markdown("""
        <div class="cg-metric anim-fade-up">
          <div style="font-size:1.4rem">📦</div>
          <div class="cg-metric-value">70,000</div>
          <div class="cg-metric-label">Patient Records</div>
        </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="cg-metric anim-fade-up anim-delay-1">
          <div style="font-size:1.4rem">🔢</div>
          <div class="cg-metric-value">11 + 2</div>
          <div class="cg-metric-label">Raw + Engineered Features</div>
        </div>""", unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div class="cg-metric anim-fade-up anim-delay-2">
          <div style="font-size:1.4rem">🎯</div>
          <div class="cg-metric-value">Binary</div>
          <div class="cg-metric-label">Classification Target</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    features_raw = [
        ("👤 Age",               "Patient age in days (converted to years)"),
        ("⚧ Gender",             "1 = Female, 2 = Male"),
        ("📏 Height (cm)",       "Patient height in centimetres"),
        ("⚖️ Weight (kg)",        "Patient weight in kilograms"),
        ("🩺 Systolic BP",       "Upper blood pressure reading (mmHg)"),
        ("🩺 Diastolic BP",      "Lower blood pressure reading (mmHg)"),
        ("🫀 Cholesterol",       "Level: 1=Normal, 2=Above Normal, 3=Well Above"),
        ("🍬 Glucose",           "Level: 1=Normal, 2=Above Normal, 3=Well Above"),
        ("🚬 Smoking",           "0 = Non-smoker, 1 = Smoker"),
        ("🍷 Alcohol Intake",    "0 = No, 1 = Yes"),
        ("🏃 Physical Activity", "0 = Inactive, 1 = Active"),
    ]

    cols = st.columns(2)
    for i, (feat, desc) in enumerate(features_raw):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="display:flex;gap:.8rem;padding:.6rem 0;
                        border-bottom:1px solid var(--border);">
              <div style="font-weight:600;color:var(--teal);min-width:155px;
                          font-size:.88rem;">{feat}</div>
              <div class="cg-body" style="font-size:.85rem;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    # ── ML Workflow ────────────────────────────────────────────────────────────
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    section_header("ML Workflow", "HOW IT WORKS")

    steps = [
        ("1", "🧹", "Data Cleaning",
         "Removed physiologically impossible values (e.g., BP &lt; 0), handled outliers "
         "using IQR filtering, and standardized age from days to years."),
        ("2", "⚙️", "Feature Engineering",
         "Created two derived features: <strong style='color:var(--teal)'>BMI</strong> "
         "(weight / height²) and <strong style='color:var(--teal)'>Pulse Pressure</strong> "
         "(systolic − diastolic BP), both strong cardiac risk indicators."),
        ("3", "🏋️", "Model Training",
         "Trained Gradient Boosting and Random Forest classifiers on an 80/20 "
         "train-test split with stratified sampling to preserve class balance."),
        ("4", "📊", "Model Evaluation",
         "Evaluated accuracy, precision, recall, F1-score, and AUC-ROC. "
         "Gradient Boosting achieved the best overall performance at "
         "<strong style='color:var(--teal)'>72.9%</strong> accuracy."),
    ]

    col_left, col_right = st.columns(2, gap="large")
    for i, (num, icon, title, desc) in enumerate(steps):
        col = col_left if i % 2 == 0 else col_right
        with col:
            st.markdown(f"""
            <div class="cg-card anim-fade-up" style="position:relative;padding:1.5rem;
                 margin-bottom:.6rem;">
              <div style="position:absolute;top:-12px;left:12px;width:28px;height:28px;
                   border-radius:50%;background:var(--teal);display:flex;
                   align-items:center;justify-content:center;
                   font-family:var(--font-head);font-weight:800;font-size:.82rem;
                   color:var(--navy);">{num}</div>
              <div style="font-size:1.8rem;margin-bottom:.4rem;">{icon}</div>
              <div style="font-family:var(--font-head);font-weight:700;
                          margin-bottom:.4rem;color:var(--white);">{title}</div>
              <div class="cg-body" style="font-size:.88rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    render_footer()

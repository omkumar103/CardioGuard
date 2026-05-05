"""
pages/features.py
App feature showcase with model benchmarks and data visualisations.
"""

import os
import streamlit as st
from utils.ui_components import render_footer, section_header


FEATURES = [
    {
        "icon": "⚡",
        "title": "Real-Time Prediction",
        "desc": "Submit your health vitals and receive an instant cardiovascular risk "
                "prediction powered by Gradient Boosting and Random Forest classifiers. "
                "Results render in under a second.",
        "color": "teal",
    },
    {
        "icon": "📊",
        "title": "Interactive Dashboard",
        "desc": "Visualise your health metrics through a clean, card-based dashboard. "
                "Track BMI, blood pressure category, pulse pressure, and confidence "
                "scores at a glance.",
        "color": "green",
    },
    {
        "icon": "🔬",
        "title": "Data Visualisation",
        "desc": "See probability confidence bars, risk factor breakdowns, and health "
                "metric summaries — all visualised in an intuitive, readable format.",
        "color": "teal",
    },
    {
        "icon": "🤖",
        "title": "Model Comparison",
        "desc": "Choose between Gradient Boosting (72.9% accuracy) and Random Forest "
                "(70.8% accuracy) models. Compare results and understand which model "
                "best suits your analysis.",
        "color": "orange",
    },
    {
        "icon": "🧠",
        "title": "Health Insights",
        "desc": "CardioGuard doesn't just predict — it explains. Get a curated list of "
                "detected risk factors with clinical context and actionable lifestyle "
                "guidance.",
        "color": "teal",
    },
    {
        "icon": "🔒",
        "title": "Privacy-First Design",
        "desc": "All computation happens locally in your browser session. No health data "
                "is stored, logged, or transmitted to any server. Your medical "
                "information stays yours.",
        "color": "green",
    },
    {
        "icon": "📱",
        "title": "Responsive Interface",
        "desc": "Designed to work seamlessly across desktop and mobile devices with a "
                "clean, accessible layout that adapts to your screen size.",
        "color": "teal",
    },
    {
        "icon": "🏥",
        "title": "Clinical Feature Coverage",
        "desc": "Analyses 13 health parameters including vitals, laboratory values, "
                "and lifestyle factors — covering the most critical cardiovascular risk "
                "indicators used in clinical practice.",
        "color": "orange",
    },
]

GRAPH_META = [
    ("heart_disease_distribution.png", "Heart Disease Distribution",
     "Overall split between positive and negative cases in the training dataset."),
    ("age_vs_disease.png",             "Age vs Heart Disease",
     "Distribution of CVD cases across age groups. Risk rises sharply after 50."),
    ("gender_vs_disease.png",          "Gender vs Heart Disease",
     "Comparative breakdown of CVD prevalence by gender."),
    ("systolic_bp.png",                "Systolic BP vs Heart Disease",
     "Higher systolic blood pressure is strongly linked to CVD."),
    ("diastolic_bp.png",               "Diastolic BP vs Heart Disease",
     "Elevated diastolic pressure also correlates with increased risk."),
    ("cholesterol.png",                "Cholesterol vs Heart Disease",
     "Well-above-normal cholesterol levels carry a significantly higher risk."),
    ("glucose.png",                    "Glucose vs Heart Disease",
     "Elevated glucose (diabetes risk) amplifies cardiovascular disease likelihood."),
    ("smoking.png",                    "Smoking vs Heart Disease",
     "Smokers show a higher prevalence of CVD across both genders."),
    ("alcohol.png",                    "Alcohol vs Heart Disease",
     "Alcohol intake influence on cardiovascular risk."),
    ("activity.png",                   "Physical Activity vs Heart Disease",
     "Physically active individuals show lower CVD rates."),
    ("correlation_heatmap.png",        "Feature Correlation Heatmap",
     "Pairwise correlations between all features. AP readings show the strongest signal."),
]


def render():
    st.markdown('<div class="cg-section">', unsafe_allow_html=True)

    # ── 1. Features Grid ──────────────────────────────────────────────────────
    section_header("App Features", "WHAT CARDIOGUARD OFFERS")

    for i in range(0, len(FEATURES), 2):
        col1, col2 = st.columns(2, gap="medium")
        for col, feat in zip([col1, col2], FEATURES[i:i+2]):
            with col:
                color = feat["color"]
                st.markdown(f"""
                <div class="cg-card cg-card-{color} anim-fade-up"
                     style="display:flex;flex-direction:column;gap:.8rem;
                            height:100%;min-height:130px;margin-bottom:.6rem;">
                  <div style="display:flex;align-items:center;gap:.9rem;">
                    <div class="cg-icon-circle" style="width:44px;height:44px;font-size:1.2rem;">
                      {feat['icon']}
                    </div>
                    <div style="font-family:var(--font-head);font-weight:700;font-size:1rem;
                                color:var(--white);">
                      {feat['title']}
                    </div>
                  </div>
                  <div class="cg-body" style="font-size:.88rem;">{feat['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── 2. Model Performance ──────────────────────────────────────────────────
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    section_header("Model Performance", "BENCHMARKS")

    st.markdown("""
    <div class="cg-card anim-fade-up">
      <table style="width:100%;border-collapse:collapse;font-size:.9rem;">
        <thead>
          <tr style="border-bottom:2px solid var(--border);">
            <th style="text-align:left;padding:.75rem;color:var(--teal);
                       font-family:var(--font-head);">Model</th>
            <th style="text-align:center;padding:.75rem;color:var(--teal);
                       font-family:var(--font-head);">Accuracy</th>
            <th style="text-align:center;padding:.75rem;color:var(--teal);
                       font-family:var(--font-head);">Precision</th>
            <th style="text-align:center;padding:.75rem;color:var(--teal);
                       font-family:var(--font-head);">Recall</th>
            <th style="text-align:center;padding:.75rem;color:var(--teal);
                       font-family:var(--font-head);">F1-Score</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom:1px solid var(--border);background:rgba(0,201,177,.05);">
            <td style="padding:.75rem;font-weight:600;color:var(--white);">
              🥇 Gradient Boosting</td>
            <td style="text-align:center;padding:.75rem;color:var(--green);font-weight:700;">
              72.9%</td>
            <td style="text-align:center;padding:.75rem;color:rgba(244,248,255,.75);">
              73.1%</td>
            <td style="text-align:center;padding:.75rem;color:rgba(244,248,255,.75);">
              71.8%</td>
            <td style="text-align:center;padding:.75rem;color:rgba(244,248,255,.75);">
              72.4%</td>
          </tr>
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:.75rem;font-weight:600;color:var(--white);">
              🥈 Random Forest</td>
            <td style="text-align:center;padding:.75rem;color:var(--orange);font-weight:700;">
              70.8%</td>
            <td style="text-align:center;padding:.75rem;color:rgba(244,248,255,.75);">
              71.2%</td>
            <td style="text-align:center;padding:.75rem;color:rgba(244,248,255,.75);">
              69.5%</td>
            <td style="text-align:center;padding:.75rem;color:rgba(244,248,255,.75);">
              70.3%</td>
          </tr>
        </tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

    # ── 3. Technology Stack ───────────────────────────────────────────────────
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    section_header("Technology Stack", "BUILT WITH")

    tech = [
        ("🐍", "Python 3.11",    "Core language"),
        ("🎈", "Streamlit",      "Web framework"),
        ("🤖", "scikit-learn",   "ML models"),
        ("🔢", "NumPy / Pandas", "Data processing"),
        ("🎨", "Custom CSS",     "UI & animations"),
    ]
    cols = st.columns(len(tech))
    for col, (icon, name, role) in zip(cols, tech):
        with col:
            st.markdown(f"""
            <div class="cg-card" style="text-align:center;padding:1.2rem .8rem;">
              <div style="font-size:2rem;margin-bottom:.4rem;">{icon}</div>
              <div style="font-family:var(--font-head);font-weight:700;
                          font-size:.95rem;color:var(--white);">{name}</div>
              <div class="cg-label" style="margin-top:.25rem;">{role}</div>
            </div>""", unsafe_allow_html=True)

    # ── 4. Data Visualisations ────────────────────────────────────────────────
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    section_header("Data Insights", "VISUAL ANALYSIS")

    graph_dir = os.path.join(os.path.dirname(__file__), "..", "graphs")
    graph_dir = os.path.normpath(graph_dir)

    any_found = False
    for i in range(0, len(GRAPH_META), 2):
        col_left, col_right = st.columns(2, gap="medium")
        for col, (filename, title, caption) in zip(
            [col_left, col_right], GRAPH_META[i:i+2]
        ):
            with col:
                full_path = os.path.join(graph_dir, filename)
                if os.path.exists(full_path):
                    any_found = True
                    st.markdown(f"""
                    <div class="cg-card" style="padding:1rem;margin-bottom:.6rem;">
                      <div style="font-family:var(--font-head);font-weight:700;
                                  font-size:.95rem;color:var(--white);margin-bottom:.6rem;">
                        {title}
                      </div>
                    """, unsafe_allow_html=True)
                    st.image(full_path, use_container_width=True)
                    st.markdown(
                        f'<div class="cg-body" style="font-size:.82rem;'
                        f'margin-top:.4rem;">{caption}</div></div>',
                        unsafe_allow_html=True
                    )
                # Silently skip missing graphs — no ugly warnings

    if not any_found:
        st.markdown("""
        <div class="cg-card cg-card-orange" style="text-align:center;padding:2rem;">
          <div style="font-size:2rem;margin-bottom:.6rem;">📁</div>
          <div style="font-family:var(--font-head);font-weight:700;color:var(--white);
                      margin-bottom:.4rem;">No Graphs Found</div>
          <div class="cg-body" style="font-size:.9rem;">
            Place your analysis images in the <code>graphs/</code> folder to see
            data visualisations here.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    render_footer()

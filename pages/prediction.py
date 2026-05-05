"""
pages/prediction.py
Core prediction functionality with sidebar inputs and rich output panel.
"""

import streamlit as st
import numpy as np

from utils.model_loader import load_models, predict
from utils.preprocessing import (
    build_feature_vector,
    compute_bmi,
    compute_pulse_pressure,
    bmi_category,
    bp_category,
    risk_factors,
)
from utils.ui_components import render_footer, section_header, progress_bar, info_box


def render():
    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:1rem 0 .5rem;">
          <div style="font-size:2.5rem;" class="anim-heart">❤️</div>
          <div style="font-family:var(--font-head);font-weight:800;font-size:1.1rem;
               color:var(--white);margin-top:.3rem;">Health Profile</div>
          <div style="font-size:.78rem;color:rgba(244,248,255,.5);margin-top:.2rem;">
            Enter your vitals below
          </div>
        </div>
        <div class="cg-divider"></div>
        """, unsafe_allow_html=True)

        # ── Personal Info ─────────────────────────────────────────────────────
        st.markdown('<div class="sidebar-section-title">👤 Personal Info</div>',
                    unsafe_allow_html=True)

        age    = st.slider("Age (years)", 18, 85, 45, help="Your current age")
        gender = st.selectbox("Gender", options=[1, 2],
                              format_func=lambda x: "Female" if x == 1 else "Male")

        # ── Vitals ────────────────────────────────────────────────────────────
        st.markdown('<div class="sidebar-section-title">🩺 Vitals</div>',
                    unsafe_allow_html=True)

        height = st.number_input("Height (cm)", min_value=100, max_value=220,
                                 value=170, step=1)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0,
                                 value=70.0, step=0.5)
        ap_hi  = st.number_input("Systolic BP (mmHg)", min_value=60, max_value=250,
                                  value=120, step=1,
                                  help="Upper blood pressure reading")
        ap_lo  = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=180,
                                  value=80, step=1,
                                  help="Lower blood pressure reading")

        # ── Medical Indicators ────────────────────────────────────────────────
        st.markdown('<div class="sidebar-section-title">🔬 Medical Indicators</div>',
                    unsafe_allow_html=True)

        chol_map = {1: "Normal", 2: "Above Normal", 3: "Well Above Normal"}
        gluc_map = {1: "Normal", 2: "Above Normal", 3: "Well Above Normal"}
        chol = st.selectbox("Cholesterol", [1, 2, 3],
                            format_func=lambda x: chol_map[x])
        gluc = st.selectbox("Glucose",     [1, 2, 3],
                            format_func=lambda x: gluc_map[x])

        # ── Lifestyle ─────────────────────────────────────────────────────────
        st.markdown('<div class="sidebar-section-title">🏃 Lifestyle</div>',
                    unsafe_allow_html=True)

        smoke  = 1 if st.toggle("Smoker",            value=False) else 0
        alco   = 1 if st.toggle("Alcohol Intake",    value=False) else 0
        active = 1 if st.toggle("Physically Active", value=True)  else 0

        # ── Model selection ───────────────────────────────────────────────────
        st.markdown('<div class="sidebar-section-title">🤖 Model</div>',
                    unsafe_allow_html=True)
        model_choice = st.selectbox("Select ML Model",
                                    ["Gradient Boosting", "Random Forest"])

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        predict_btn = st.button("🔮  Predict Risk", use_container_width=True)

    # ── Main Panel ────────────────────────────────────────────────────────────
    st.markdown('<div class="cg-section" style="padding-top:2rem;">',
                unsafe_allow_html=True)
    section_header("Cardiovascular Risk Prediction", "AI ANALYSIS")

    if not predict_btn and "last_prediction" not in st.session_state:
        # Placeholder state
        st.markdown("""
        <div class="cg-card" style="text-align:center;padding:3rem 2rem;margin-top:1rem;">
          <div style="font-size:4rem;margin-bottom:1rem;" class="anim-heart">❤️</div>
          <div style="font-family:var(--font-head);font-weight:700;
                      font-size:1.3rem;margin-bottom:.8rem;color:var(--white);">
            Ready to Analyse
          </div>
          <div class="cg-body" style="max-width:440px;margin:0 auto;">
            Fill in your health profile in the left panel and click
            <strong style="color:var(--teal)">Predict Risk</strong> to receive your
            AI-powered cardiovascular risk assessment.
          </div>
        </div>
        """, unsafe_allow_html=True)

    if predict_btn or "last_prediction" in st.session_state:
        if predict_btn:
            with st.spinner("Analysing your health data…"):
                models  = load_models()
                bmi_val = compute_bmi(weight, height)
                pp_val  = compute_pulse_pressure(ap_hi, ap_lo)
                feats   = build_feature_vector(
                    age, gender, height, weight,
                    ap_hi, ap_lo, chol, gluc,
                    smoke, alco, active,
                )
                pred, proba = predict(models, feats, model_choice)
                model_acc   = models[model_choice]["accuracy"]

            st.session_state.last_prediction = {
                "pred":     pred,
                "proba":    proba,
                "bmi":      bmi_val,
                "pp":       pp_val,
                "ap_hi":    ap_hi,
                "ap_lo":    ap_lo,
                "model":    model_choice,
                "accuracy": model_acc,
                "age":      age,
                "chol":     chol,
                "gluc":     gluc,
                "smoke":    smoke,
                "alco":     alco,
                "active":   active,
            }

        # Restore cached state
        s      = st.session_state.last_prediction
        pred   = s["pred"]
        proba  = s["proba"]
        bmi_val = s["bmi"]
        pp_val  = s["pp"]

        # ── Result Card ────────────────────────────────────────────────────────
        result_class = "cg-result-high" if pred == 1 else "cg-result-low"
        result_label = "High Risk"       if pred == 1 else "Low Risk"
        result_icon  = "🔴"              if pred == 1 else "🟢"
        result_color = "red"             if pred == 1 else "green"
        result_msg   = (
            "⚠️ Elevated cardiovascular disease risk detected. "
            "Please consult a healthcare professional."
            if pred == 1 else
            "✅ No significant cardiovascular risk detected based on the provided parameters."
        )

        col_res, col_conf = st.columns([1, 1], gap="large")

        with col_res:
            st.markdown(f"""
            <div class="{result_class} anim-fade-up" style="margin-top:.5rem;">
              <div class="cg-result-icon anim-heart">{result_icon}</div>
              <div class="cg-result-label"
                   style="color:{'var(--red)' if pred==1 else 'var(--green)'}">
                {result_label}
              </div>
              <div class="cg-body" style="margin-top:.8rem;">{result_msg}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_conf:
            st.markdown(f"""
            <div class="cg-card anim-fade-up anim-delay-1" style="margin-top:.5rem;">
              <div class="cg-subheading">Prediction Confidence</div>
              <div style="margin:.8rem 0;">
            """, unsafe_allow_html=True)

            progress_bar(proba, result_color,
                         f"Risk Probability: {proba*100:.1f}%")
            progress_bar(s["accuracy"], "teal",
                         f"Model Accuracy ({s['model']}): {s['accuracy']*100:.1f}%")

            st.markdown(f"""
              </div>
              <div style="display:flex;gap:.8rem;margin-top:1rem;flex-wrap:wrap;">
                <div class="cg-badge">{s['model']}</div>
                <div class="cg-badge"
                     style="background:rgba(46,204,113,.12);
                            border-color:rgba(46,204,113,.35);color:var(--green);">
                  {s['accuracy']*100:.1f}% Accuracy
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Health Metrics ─────────────────────────────────────────────────────
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="cg-subheading anim-fade-up">📊 HEALTH METRICS</div>',
                    unsafe_allow_html=True)

        bmi_cat, bmi_clr = bmi_category(bmi_val)
        bp_cat,  bp_clr  = bp_category(s["ap_hi"], s["ap_lo"])

        color_map = {
            "green":  "var(--green)",
            "orange": "var(--orange)",
            "red":    "var(--red)",
            "teal":   "var(--teal)",
        }

        pp_clr = "teal" if pp_val < 60 else "orange"

        m1, m2, m3, m4 = st.columns(4)
        for col, val, label, icon, clr in [
            (m1, f"{bmi_val}",             f"BMI · {bmi_cat}",   "⚖️", bmi_clr),
            (m2, f"{s['ap_hi']}/{s['ap_lo']}", f"BP · {bp_cat}", "🩺", bp_clr),
            (m3, f"{pp_val} mmHg",         "Pulse Pressure",      "💓", pp_clr),
            (m4, f"{s['age']} yrs",        "Age",                 "📅", "teal"),
        ]:
            with col:
                clr_css = color_map.get(clr, "var(--teal)")
                st.markdown(f"""
                <div class="cg-metric anim-fade-up" style="align-items:center;text-align:center;">
                  <div style="font-size:1.6rem;">{icon}</div>
                  <div class="cg-metric-value" style="color:{clr_css};font-size:1.5rem;">{val}</div>
                  <div class="cg-metric-label">{label}</div>
                </div>""", unsafe_allow_html=True)

        # ── Risk Factors ───────────────────────────────────────────────────────
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="cg-subheading anim-fade-up">🧠 RISK FACTORS DETECTED</div>',
                    unsafe_allow_html=True)

        factors = risk_factors(
            bmi_val,
            s["ap_hi"], s["ap_lo"],
            s["chol"],  s["gluc"],
            s["smoke"], s["alco"],
            s["active"], s["age"],
        )

        severity_color = {"high": "red", "medium": "orange", "low": "teal"}

        if factors:
            for f in factors:
                col_icon, col_text = st.columns([1, 14])
                with col_icon:
                    st.markdown(
                        f"<div style='font-size:1.4rem;padding-top:.4rem;'>{f['icon']}</div>",
                        unsafe_allow_html=True
                    )
                with col_text:
                    sev   = f["severity"]
                    color = severity_color.get(sev, "teal")
                    info_box(
                        f"<strong>{f['title']}</strong> — {f['desc']}", color
                    )
        else:
            info_box(
                "✅ No significant risk factors detected. Maintain your healthy lifestyle!",
                "green"
            )

        # ── Medical Disclaimer ─────────────────────────────────────────────────
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(243,156,18,.08);border:1px solid rgba(243,156,18,.3);
             border-radius:10px;padding:.9rem 1.2rem;">
          <strong style="color:var(--orange);">⚠️ Medical Disclaimer</strong>
          <div class="cg-body" style="margin-top:.3rem;font-size:.85rem;">
            This tool is for informational and educational purposes only. It is
            <strong>not a substitute for professional medical advice</strong>. Always
            consult a qualified healthcare professional for diagnosis and treatment.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    render_footer()

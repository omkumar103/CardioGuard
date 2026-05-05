"""
utils/model_loader.py
Loads, trains, and caches the cardiovascular disease prediction model.
Falls back to a scikit-learn model trained on synthetic data if no saved
model is found, so the app always works without a CSV file.
"""

import pickle
import numpy as np
import streamlit as st
from pathlib import Path

from utils.preprocessing import build_feature_vector

MODEL_PATH = Path(__file__).parent.parent / "models" / "cardio_model.pkl"


# ── Synthetic model training (fallback) ──────────────────────────────────────
def _train_fallback_models() -> dict:
    """Train lightweight GB + RF models on synthetic data. Returns model dict."""
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    import warnings
    warnings.filterwarnings("ignore")

    rng = np.random.default_rng(42)
    n = 8_000

    age      = rng.integers(30, 80, n).astype(float)
    gender   = rng.integers(1, 3, n).astype(float)
    height   = rng.integers(150, 200, n).astype(float)
    weight   = rng.uniform(45, 130, n)
    ap_hi    = rng.integers(90, 200, n).astype(float)
    ap_lo    = rng.integers(60, 130, n).astype(float)
    chol     = rng.integers(1, 4, n).astype(float)
    gluc     = rng.integers(1, 4, n).astype(float)
    smoke    = rng.integers(0, 2, n).astype(float)
    alco     = rng.integers(0, 2, n).astype(float)
    active   = rng.integers(0, 2, n).astype(float)
    bmi      = weight / (height / 100) ** 2
    pulse_pr = ap_hi - ap_lo

    X = np.column_stack([
        age, gender, height, weight,
        ap_hi, ap_lo, chol, gluc,
        smoke, alco, active, bmi, pulse_pr,
    ])

    # Realistic composite risk signal
    risk = (
        (age > 55) * 2.0
        + (ap_hi > 140) * 2.5
        + (ap_lo > 90) * 1.5
        + (chol == 3) * 2.0
        + (chol == 2) * 1.0
        + (gluc == 3) * 1.5
        + (bmi > 30) * 1.5
        + (bmi > 35) * 1.0
        + (smoke == 1) * 1.2
        + (alco == 1) * 0.8
        + (active == 0) * 1.0
        + (pulse_pr > 60) * 1.2
        + rng.normal(0, 1, n)
    )
    y = (risk > 5.5).astype(int)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    gb = GradientBoostingClassifier(
        n_estimators=120, max_depth=4, learning_rate=0.08, random_state=42
    )
    gb.fit(X_scaled, y)

    rf = RandomForestClassifier(
        n_estimators=100, max_depth=6, random_state=42
    )
    rf.fit(X_scaled, y)

    # Compute approximate test accuracy (last 20%)
    split = int(0.8 * n)
    gb_acc = gb.score(X_scaled[split:], y[split:])
    rf_acc = rf.score(X_scaled[split:], y[split:])

    models = {
        "Gradient Boosting": {"model": gb, "accuracy": round(gb_acc, 3)},
        "Random Forest":     {"model": rf, "accuracy": round(rf_acc, 3)},
        "scaler":            scaler,
    }

    # Persist to disk
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(models, f)

    return models


def _load_from_csv() -> dict | None:
    """Try to train from the real CSV. Returns model dict or None."""
    from pathlib import Path
    csv_path = Path(__file__).parent.parent / "data" / "cardio_train.csv"
    if not csv_path.exists():
        return None

    try:
        from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        from utils.preprocessing import load_and_clean_data, feature_engineering
        import warnings
        warnings.filterwarnings("ignore")

        df = load_and_clean_data(str(csv_path))
        df = feature_engineering(df)

        X = df.drop("target", axis=1).values
        y = df["target"].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test  = scaler.transform(X_test)

        gb = GradientBoostingClassifier(
            n_estimators=120, max_depth=4, learning_rate=0.08, random_state=42
        )
        gb.fit(X_train, y_train)
        gb_acc = gb.score(X_test, y_test)

        rf = RandomForestClassifier(
            n_estimators=100, max_depth=10, random_state=42
        )
        rf.fit(X_train, y_train)
        rf_acc = rf.score(X_test, y_test)

        models = {
            "Gradient Boosting": {"model": gb, "accuracy": round(gb_acc, 3)},
            "Random Forest":     {"model": rf, "accuracy": round(rf_acc, 3)},
            "scaler":            scaler,
        }

        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(models, f)

        return models

    except Exception as e:
        print(f"[model_loader] CSV training failed: {e}")
        return None


@st.cache_resource(show_spinner=False)
def load_models() -> dict:
    """
    Returns:
        {
          "Gradient Boosting": {"model": ..., "accuracy": float},
          "Random Forest":     {"model": ..., "accuracy": float},
          "scaler":            StandardScaler,
        }
    """
    # 1. Try cached .pkl
    if MODEL_PATH.exists():
        try:
            with open(MODEL_PATH, "rb") as f:
                data = pickle.load(f)
            if "scaler" in data and "Gradient Boosting" in data:
                return data
        except Exception:
            pass

    # 2. Try training from real CSV
    result = _load_from_csv()
    if result:
        return result

    # 3. Fallback: synthetic model
    return _train_fallback_models()


def predict(models: dict, features: np.ndarray, model_name: str) -> tuple:
    """
    Returns (prediction: int, probability: float).
    prediction: 1 = High Risk, 0 = Low Risk
    """
    scaler = models["scaler"]
    m = models[model_name]["model"]
    features_scaled = scaler.transform(features)
    pred  = int(m.predict(features_scaled)[0])
    proba = float(m.predict_proba(features_scaled)[0][1])
    return pred, proba

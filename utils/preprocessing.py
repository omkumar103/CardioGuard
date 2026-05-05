"""
utils/preprocessing.py
Data loading, cleaning, feature engineering, and helper functions.
"""

import numpy as np
import pandas as pd


# ── Data loading & cleaning ───────────────────────────────────────────────────
def load_and_clean_data(path: str = "data/cardio_train.csv") -> pd.DataFrame:
    df = pd.read_csv(path, sep=";")

    if "id" in df.columns:
        df.drop("id", axis=1, inplace=True)

    # Convert age from days to years
    df["age"] = (df["age"] / 365).astype(int)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Remove physiologically impossible BP values
    df = df[(df["ap_hi"] > 50) & (df["ap_hi"] < 250)]
    df = df[(df["ap_lo"] > 30) & (df["ap_lo"] < 200)]

    # Rename target column
    df.rename(columns={"cardio": "target"}, inplace=True)

    return df.reset_index(drop=True)


# ── Feature engineering ───────────────────────────────────────────────────────
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)
    df["pulse_pressure"] = df["ap_hi"] - df["ap_lo"]
    return df


# ── Build feature vector from single-row user input ─────────────────────────
def build_feature_vector(
    age: int,
    gender: int,
    height: int,
    weight: float,
    ap_hi: int,
    ap_lo: int,
    cholesterol: int,
    glucose: int,
    smoke: int,
    alco: int,
    active: int,
) -> np.ndarray:
    bmi = round(weight / (height / 100) ** 2, 1) if height > 0 else 0.0
    pp  = max(0, ap_hi - ap_lo)
    return np.array([[
        age, gender, height, weight,
        ap_hi, ap_lo, cholesterol, glucose,
        smoke, alco, active, bmi, pp,
    ]], dtype=float)


# ── Derived metric helpers ────────────────────────────────────────────────────
def compute_bmi(weight_kg: float, height_cm: float) -> float:
    if height_cm <= 0:
        return 0.0
    return round(weight_kg / (height_cm / 100) ** 2, 1)


def compute_pulse_pressure(ap_hi: int, ap_lo: int) -> int:
    return max(0, ap_hi - ap_lo)


def bmi_category(bmi: float) -> tuple:
    """Returns (category_label, color_class)."""
    if bmi < 18.5:
        return "Underweight", "orange"
    elif bmi < 25.0:
        return "Normal", "green"
    elif bmi < 30.0:
        return "Overweight", "orange"
    else:
        return "Obese", "red"


def bp_category(ap_hi: int, ap_lo: int) -> tuple:
    """Returns (category_label, color_class)."""
    if ap_hi < 120 and ap_lo < 80:
        return "Normal", "green"
    elif ap_hi < 130 and ap_lo < 80:
        return "Elevated", "orange"
    elif ap_hi < 140 or ap_lo < 90:
        return "High Stage 1", "orange"
    elif ap_hi >= 180 or ap_lo >= 120:
        return "Crisis", "red"
    else:
        return "High Stage 2", "red"


# ── Risk factor explanations ──────────────────────────────────────────────────
def risk_factors(
    bmi: float,
    ap_hi: int,
    ap_lo: int,
    cholesterol: int,
    glucose: int,
    smoke: int,
    alco: int,
    active: int,
    age: int,
) -> list:
    """Return a list of detected risk factors with severity."""
    factors = []

    if ap_hi >= 140 or ap_lo >= 90:
        factors.append({
            "icon": "🩺",
            "title": "High Blood Pressure",
            "desc": f"Your BP ({ap_hi}/{ap_lo} mmHg) is above the healthy range. "
                    "Hypertension directly strains the heart and arteries.",
            "severity": "high",
        })
    elif ap_hi >= 130:
        factors.append({
            "icon": "⚠️",
            "title": "Elevated Blood Pressure",
            "desc": f"BP ({ap_hi}/{ap_lo} mmHg) is elevated. Monitor closely and reduce sodium intake.",
            "severity": "medium",
        })

    if bmi >= 30:
        factors.append({
            "icon": "⚖️",
            "title": "Obesity",
            "desc": f"BMI of {bmi} indicates obesity, a major cardiovascular risk factor.",
            "severity": "high",
        })
    elif bmi >= 25:
        factors.append({
            "icon": "⚖️",
            "title": "Overweight",
            "desc": f"BMI of {bmi} is above the healthy range (18.5–24.9).",
            "severity": "medium",
        })

    if cholesterol == 3:
        factors.append({
            "icon": "🫀",
            "title": "Very High Cholesterol",
            "desc": "High cholesterol causes plaque build-up in arteries, increasing heart attack risk.",
            "severity": "high",
        })
    elif cholesterol == 2:
        factors.append({
            "icon": "🫀",
            "title": "Above-Normal Cholesterol",
            "desc": "Cholesterol is above normal. Dietary changes and exercise can help.",
            "severity": "medium",
        })

    if glucose == 3:
        factors.append({
            "icon": "🍬",
            "title": "Very High Glucose",
            "desc": "High blood glucose is linked to diabetes, which significantly raises cardiac risk.",
            "severity": "high",
        })
    elif glucose == 2:
        factors.append({
            "icon": "🍬",
            "title": "Above-Normal Glucose",
            "desc": "Blood glucose is above normal. Monitor for pre-diabetes.",
            "severity": "medium",
        })

    if smoke:
        factors.append({
            "icon": "🚬",
            "title": "Smoking",
            "desc": "Smoking damages blood vessel walls and dramatically increases cardiovascular risk.",
            "severity": "high",
        })

    if alco:
        factors.append({
            "icon": "🍷",
            "title": "Alcohol Use",
            "desc": "Frequent alcohol consumption can raise blood pressure and weaken heart muscle.",
            "severity": "medium",
        })

    if not active:
        factors.append({
            "icon": "🏃",
            "title": "Physical Inactivity",
            "desc": "A sedentary lifestyle increases risk of obesity, hypertension, and heart disease.",
            "severity": "medium",
        })

    if age >= 60:
        factors.append({
            "icon": "📅",
            "title": "Age Risk Factor",
            "desc": f"Age {age} is a significant non-modifiable risk factor for cardiovascular disease.",
            "severity": "medium",
        })

    return factors

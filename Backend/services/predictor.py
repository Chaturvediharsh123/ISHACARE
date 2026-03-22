import pickle
import numpy as np
import os

# Load ML model
MODEL_PATH = os.path.join("Models", "model.pkl")

with open(MODEL_PATH, "rb") as f:
    ml_model = pickle.load(f)


# ---------------- RULE-BASED ---------------- #
def rule_based_prediction(data):

    risk = {}
    explanation = {}

    # Diabetes
    if data.get("glucose", 0) > 140 or data.get("hba1c", 0) > 6.5:
        risk["diabetes"] = "High"
        explanation["diabetes"] = "High glucose or HbA1c"
    else:
        risk["diabetes"] = "Low"
        explanation["diabetes"] = "Normal"

    # Heart
    if data.get("ldl", 0) > 130 or data.get("triglycerides", 0) > 150:
        risk["heart"] = "High"
        explanation["heart"] = "High LDL or triglycerides"
    else:
        risk["heart"] = "Low"
        explanation["heart"] = "Normal"

    # Liver
    if data.get("alt", 0) > 55 or data.get("ast", 0) > 48:
        risk["liver"] = "High"
        explanation["liver"] = "High liver enzymes"
    else:
        risk["liver"] = "Low"
        explanation["liver"] = "Normal"

    # Kidney
    if data.get("creatinine", 0) > 1.3:
        risk["kidney"] = "High"
        explanation["kidney"] = "High creatinine"
    else:
        risk["kidney"] = "Low"
        explanation["kidney"] = "Normal"

    # Anemia
    if data.get("hemoglobin", 0) < 12:
        risk["anemia"] = "High"
        explanation["anemia"] = "Low hemoglobin"
    else:
        risk["anemia"] = "Low"
        explanation["anemia"] = "Normal"

    return risk, explanation


# ---------------- ML PREDICTION ---------------- #
def ml_prediction(data):
    input_data = np.array([[
        data.get("hemoglobin", 0),
        data.get("cholesterol", 0),
        data.get("glucose", 0)
    ]])

    pred = ml_model.predict(input_data)[0]

    return "High Risk ⚠️" if pred == 1 else "Low Risk ✅"


# ---------------- SCORE ---------------- #
def calculate_score(risk_dict):
    score = sum(1 for v in risk_dict.values() if v == "High")
    return round((score / len(risk_dict)) * 100, 2)


# ---------------- FINAL HYBRID ---------------- #
def predict_full_health(data):

    rule_risk, explanation = rule_based_prediction(data)
    ml_risk = ml_prediction(data)
    score = calculate_score(rule_risk)

    return {
        "rule_based": rule_risk,
        "ml_prediction": ml_risk,
        "risk_score": score,
        "explanation": explanation
    }

def predict_health_risk(data):
    risk = {}

    risk["diabetes"] = "High" if data.get("glucose", 0) > 140 or data.get("hba1c", 0) > 6.5 else "Low"
    risk["heart"] = "High" if data.get("ldl", 0) > 130 or data.get("triglycerides", 0) > 150 else "Low"
    risk["liver"] = "High" if data.get("alt", 0) > 55 or data.get("ast", 0) > 48 else "Low"
    risk["kidney"] = "High" if data.get("creatinine", 0) > 1.3 else "Low"
    risk["anemia"] = "High" if data.get("hemoglobin", 0) < 12 else "Low"

    return risk
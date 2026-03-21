def predict_health_risk(data):

    risk = {}

    risk["diabetes"] = "High" if data.get("glucose", 0) > 140 or data.get("hba1c", 0) > 6.5 else "Low"

    risk["heart"] = "High" if data.get("ldl", 0) > 130 or data.get("triglycerides", 0) > 150 else "Low"

    risk["liver"] = "High" if data.get("alt", 0) > 55 or data.get("ast", 0) > 48 else "Low"

    risk["kidney"] = "High" if data.get("creatinine", 0) > 1.3 else "Low"

    risk["anemia"] = "High" if data.get("hemoglobin", 15) < 12 else "Low"

    return risk
def generate_alerts(data):

    alerts = []

    if data.get("glucose", 0) > 180:
        alerts.append("🚨 Critical Diabetes Risk")

    if data.get("ldl", 0) > 160:
        alerts.append("🚨 High Bad Cholesterol")

    if data.get("creatinine", 0) > 1.5:
        alerts.append("🚨 Kidney Risk")

    if data.get("alt", 0) > 70:
        alerts.append("🚨 Liver Damage Risk")

    return alerts
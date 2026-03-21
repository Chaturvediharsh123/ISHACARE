from services.extractor import extract_text, extract_values
from services.cleaner import clean_data
from services.predictor import predict_health_risk
from services.scorer import calculate_score
from services.automation import run_automation

def run_pipeline(file_path):

    text = extract_text(file_path)

    raw_data = extract_values(text)

    clean = clean_data(raw_data)

    risk = predict_health_risk(clean)

    score = calculate_score(clean)

    alerts = run_automation(clean)

    return {
        "structured_data": clean,
        "risk_analysis": risk,
        "health_score": score,
        "alerts": alerts
    }
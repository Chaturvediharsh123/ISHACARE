import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import time
import pickle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime
import matplotlib.pyplot as plt
import os
import numpy as np

# ---------- CONFIG ----------
st.set_page_config(page_title="ISHACARE", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>
.stApp { background: #0f172a; }

.title {
    font-size: 34px;
    font-weight: 600;
    color: #f1f5f9;
}

.card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #334155;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    border: 1px solid #38bdf8;
}

.fade { animation: fadeIn 0.5s ease-in; }

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

label, .stMarkdown, .stSubheader {
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title fade">ISHACARE Dashboard</div>', unsafe_allow_html=True)

# ---------- HERO SECTION ----------
file = st.file_uploader("Upload Medical Report", type=["pdf", "png", "jpg"])

if not file:
    st.markdown("### 🧠 AI-Powered Health Intelligence System")

    st.markdown("""
    Welcome to **ISHACARE** 🚀  
    Your smart assistant for analyzing medical reports using **AI + Machine Learning**.

    🔍 Upload your report and get:
    - 📊 Health Score
    - 🧠 AI Risk Prediction
    - ⚠ Disease Detection
    - 💡 Personalized Recommendations
    - 📄 Downloadable AI Report
    """)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📊 Smart Analysis")
        st.info("Automatically extracts and analyzes medical parameters")

    with col2:
        st.markdown("### 🧠 AI Prediction")
        st.info("Uses ML models to predict health risks")

    with col3:
        st.markdown("### 📄 Report Generation")
        st.info("Generates detailed downloadable health reports")

    st.divider()

    st.markdown("### ⚙️ How It Works")

    st.markdown("""
    1️⃣ Upload your medical report (PDF/Image)  
    2️⃣ AI extracts important health parameters  
    3️⃣ ML model analyzes risk  
    4️⃣ Get insights + downloadable report  
    """)

    st.divider()

    if st.button("✨ Try Demo Without Upload"):
        st.session_state["demo"] = {
            "health_score": 65,
            "risk_analysis": {
                "diabetes": "High",
                "heart": "Low",
                "liver": "Low",
                "kidney": "Low",
                "anemia": "High"
            },
            "alerts": ["High glucose detected", "Low hemoglobin"],
            "structured_data": {
                "glucose": {"value": 160},
                "hemoglobin": {"value": 10},
                "cholesterol": {"value": 220}
            }
        }

# ---------- LOAD ML MODEL ----------
MODEL_PATH = os.path.join("Backend", "Models", "model.pkl")

try:
    model = pickle.load(open(MODEL_PATH, "rb"))
except:
    model = None


def predict_ml(data):
    if not model:
        return "Model not loaded", 0

    features = np.array([[
        data.get("hemoglobin", 0),
        data.get("cholesterol", 0),
        data.get("glucose", 0)
    ]])

    pred = model.predict(features)[0]
    prob = model.predict_proba(features)[0][pred]

    label = "High Risk ⚠️" if pred == 1 else "Low Risk ✅"
    return label, round(prob * 100, 2)


def calculate_confidence(data):
    total = len(data)
    valid = sum(1 for v in data.values() if (v["value"] if isinstance(v, dict) else v) > 0)
    return round((valid / total) * 100, 2)


def generate_recommendations(risks):
    recs = []

    if risks.get("diabetes") == "High":
        recs.append("Reduce sugar intake and monitor glucose regularly")

    if risks.get("heart") == "High":
        recs.append("Avoid oily food and maintain regular exercise")

    if risks.get("liver") == "High":
        recs.append("Avoid alcohol and take liver-friendly diet")

    if risks.get("kidney") == "High":
        recs.append("Stay hydrated and monitor creatinine levels")

    if risks.get("anemia") == "High":
        recs.append("Increase iron intake (spinach, dates, etc.)")

    return recs if recs else ["Maintain a healthy lifestyle ✅"]


def generate_pdf(data, ml_result, confidence, recommendations):

    doc = SimpleDocTemplate("health_report.pdf")
    styles = getSampleStyleSheet()
    elements = []

    now = datetime.now().strftime("%d-%m-%Y %H:%M")

    elements.append(Paragraph("AI HEALTH REPORT", styles['Title']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Generated on: {now}", styles['Normal']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Summary", styles['Heading2']))
    elements.append(Paragraph(f"ML Prediction: {ml_result}", styles['Normal']))
    elements.append(Paragraph(f"Confidence Score: {confidence}%", styles['Normal']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Risk Analysis", styles['Heading2']))

    risk_data = [["Condition", "Status"]]
    for k, v in data["risk_analysis"].items():
        risk_data.append([k, v])

    table = Table(risk_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("AI Recommendations", styles['Heading2']))
    for r in recommendations:
        elements.append(Paragraph(f"- {r}", styles['Normal']))

    elements.append(Spacer(1, 10))

    labels = list(data["structured_data"].keys())
    values = [v["value"] if isinstance(v, dict) else v for v in data["structured_data"].values()]

    plt.bar(labels, values)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("graph.png")
    plt.close()

    elements.append(Image("graph.png", width=5*inch, height=3*inch))

    doc.build(elements)


# ---------- MAIN ----------
if file or "demo" in st.session_state:

    with st.spinner("Analyzing..."):
        time.sleep(1)

        if "demo" in st.session_state:
            data = st.session_state["demo"]
        else:
            res = requests.post(
                "http://127.0.0.1:8000/analyze/",
                files={"file": file}
            )
            data = res.json()

    score = data["health_score"]
    risks = data["risk_analysis"]
    alerts = data["alerts"]
    structured_data = data["structured_data"]

    flat_data = {k: (v["value"] if isinstance(v, dict) else v) for k, v in structured_data.items()}
    ml_result, ml_conf = predict_ml(flat_data)
    confidence_score = calculate_confidence(structured_data)
    recommendations = generate_recommendations(risks)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Health Score", score)
    c1.progress(score/100)

    c2.metric("Risks", sum(1 for v in risks.values() if v == "High"))
    c3.metric("ML Prediction", ml_result)
    c4.metric("Confidence", f"{ml_conf}%")

    st.divider()

    st.subheader("Overall Status")

    if score > 80:
        st.success("🟢 Healthy")
    elif score > 50:
        st.warning("🟡 Moderate")
    else:
        st.error("🔴 Critical")

    st.subheader("Health Parameters")

    labels = []
    values = []

    for k, v in structured_data.items():
        labels.append(k)
        values.append(v["value"] if isinstance(v, dict) else v)

    df = pd.DataFrame({"Parameter": labels, "Value": values})

    fig = px.bar(df, x="Parameter", y="Value", text="Value")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Risk Analysis")

    risk_df = pd.DataFrame({
        "Condition": list(risks.keys()),
        "Status": list(risks.values())
    })

    st.dataframe(risk_df, use_container_width=True)

    st.subheader("Extracted Parameters")

    param_df = pd.DataFrame({
        "Parameter": labels,
        "Value": values
    })

    st.dataframe(param_df, use_container_width=True)

    st.subheader("Alerts")

    if score < 50:
        st.error("🚨 Critical condition")

    if not alerts:
        st.success("✅ No major issues detected")

    for a in alerts:
        st.warning(a)

    st.subheader("AI Insights")

    if "High Risk" in ml_result:
        st.warning("⚠ High disease risk detected. Please consult a doctor.")
    else:
        st.success("✔ No major disease risk detected.")

    st.subheader("💡 Recommendations")

    for r in recommendations:
        st.info(r)

    st.subheader("Report")

    if st.button("📄 Generate & Download Report"):
        generate_pdf(data, ml_result, ml_conf, recommendations)

        with open("health_report.pdf", "rb") as f:
            st.download_button("⬇ Download Report", f, file_name="health_report.pdf")
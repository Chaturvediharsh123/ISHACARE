import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
st.set_page_config(page_title="Health AI", layout="wide")

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
st.markdown('<div class="title fade">Health Analysis Dashboard</div>', unsafe_allow_html=True)

# ---------- UPLOAD ----------
file = st.file_uploader("Upload Medical Report", type=["pdf", "png", "jpg"])

# ---------- PDF ----------
def generate_pdf(data):

    doc = SimpleDocTemplate("health_report.pdf")
    styles = getSampleStyleSheet()
    elements = []

    now = datetime.now().strftime("%d-%m-%Y %H:%M")

    elements.append(Paragraph("AI HEALTH REPORT", styles['Title']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Date: {now}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # Risk Table
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

    # Graph
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
if file:

    with st.spinner("Analyzing..."):
        time.sleep(1)
        res = requests.post(
            "http://127.0.0.1:8000/analyze/",
            files={"file": file}
        )
        data = res.json()

    score = data["health_score"]
    risks = data["risk_analysis"]
    alerts = data["alerts"]
    structured_data = data["structured_data"]

    # ---------- CARDS ----------
    c1, c2, c3 = st.columns(3)

    c1.metric("Health Score", score)
    c1.progress(score/100)

    c2.metric("Risks", sum(1 for v in risks.values() if v == "High"))
    c3.metric("Alerts", len(alerts))

    st.divider()

    # ---------- GRAPH ----------
    st.subheader("Health Parameters")

    labels = []
    values = []

    for k, v in structured_data.items():
        labels.append(k)
        values.append(v["value"] if isinstance(v, dict) else v)

    df = pd.DataFrame({"Parameter": labels, "Value": values})

    fig = px.bar(df, x="Parameter", y="Value", text="Value")
    st.plotly_chart(fig, use_container_width=True)

    # ---------- RISK TABLE ----------
    st.subheader("Risk Analysis")

    risk_df = pd.DataFrame({
        "Condition": list(risks.keys()),
        "Status": list(risks.values())
    })

    st.dataframe(risk_df, use_container_width=True)

    # ---------- PARAM TABLE ----------
    st.subheader("Extracted Parameters")

    param_df = pd.DataFrame({
        "Parameter": labels,
        "Value": values
    })

    st.dataframe(param_df, use_container_width=True)

    # ---------- ALERTS ----------
    st.subheader("Alerts")

    if score < 50:
        st.error("🚨 Critical condition")

    for a in alerts:
        st.warning(a)

    # ---------- DOWNLOAD ----------
    if st.button("📄 Generate Report"):
        generate_pdf(data)

        with open("health_report.pdf", "rb") as f:
            st.download_button("Download Report", f, file_name="report.pdf")
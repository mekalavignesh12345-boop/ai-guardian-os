import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

from database.database import get_connection

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(

    page_title="Compliance Report",

    page_icon="📑",

    layout="wide"

)

st.title("📑 Responsible AI Compliance Report")

st.caption(

    "Generate enterprise Responsible AI compliance reports."

)

st.divider()
# -----------------------------------------------------
# Load Analysis Results
# -----------------------------------------------------

if "dataset" not in st.session_state:
    st.error("❌ Please upload a dataset first.")
    st.stop()

df = st.session_state["dataset"]

fairness = st.session_state.get("fairness_score", 0)
privacy = st.session_state.get("privacy_score", 0)
explainability = st.session_state.get("explainability_score", 0)
accuracy = st.session_state.get("model_accuracy", 0)

dataset = {
    "rows": len(df),
    "columns": len(df.columns),
    "filename": "Uploaded Dataset"
}

project_id = "Current Session"

st.success("✅ Analysis results loaded successfully.")

st.divider()
# -----------------------------------------------------
# Compliance Dashboard
# -----------------------------------------------------

st.header("Compliance Dashboard")

c1,c2,c3,c4 = st.columns(4)

fairness = model["fairness"] or 0
privacy = model["privacy"] or 0
explainability = model["explainability"] or 0
accuracy = model["accuracy"] or 0

overall = round(

    (

        fairness +

        privacy +

        explainability +

        accuracy

    ) / 4,

    2

)
# -----------------------------------------------------
# Save Compliance Results
# -----------------------------------------------------

st.session_state["compliance_score"] = overall
# Save Compliance Results
st.session_state["compliance_score"] = overall
st.session_state["risk_level"] = risk_level if "risk_level" in locals() else "LOW"

c1.metric(

    "Fairness",

    f"{fairness}%"

)

c2.metric(

    "Privacy",

    f"{privacy}%"

)

c3.metric(

    "Explainability",

    f"{explainability}%"

)

c4.metric(

    "Overall",

    f"{overall}%"

)

st.progress(

    overall / 100

)

st.divider()
# -----------------------------------------------------
# Executive Summary
# -----------------------------------------------------

st.header("Executive Summary")

risk_level = "LOW"

if overall < 60:

    risk_level = "HIGH"

elif overall < 80:

    risk_level = "MEDIUM"

summary = f"""
The Responsible AI assessment for the selected project has been completed.

Overall Compliance Score: {overall:.2f}%

Risk Level: {risk_level}

The evaluation includes fairness, privacy,
model explainability and overall governance
readiness.

This report summarizes the current
Responsible AI posture of the project and
highlights areas requiring improvement.
"""

st.info(summary)
st.success("✅ Compliance analysis completed.")

st.divider()
st.session_state["risk_level"] = risk_level
# -----------------------------------------------------
# Dataset Information
# -----------------------------------------------------

st.header("Dataset Information")

if dataset is not None:

    d1, d2, d3 = st.columns(3)

    d1.metric(

        "Rows",

        dataset["rows"]

    )

    d2.metric(

        "Columns",

        dataset["columns"]

    )

    d3.metric(

        "Filename",

        dataset["filename"]

    )

else:

    st.warning(

        "Dataset metadata unavailable."

    )

st.divider()

# -----------------------------------------------------
# Compliance Score Table
# -----------------------------------------------------

st.header("Compliance Scorecard")

score_df = pd.DataFrame({

    "Category":[

        "Fairness",

        "Privacy",

        "Explainability",

        "Accuracy",

        "Overall"

    ],

    "Score":[

        fairness,

        privacy,

        explainability,

        accuracy,

        overall

    ]

})

st.dataframe(

    score_df,

    use_container_width=True,

    hide_index=True

)

st.bar_chart(

    score_df.set_index(

        "Category"

    )

)

st.divider()

# -----------------------------------------------------
# Compliance Checklist
# -----------------------------------------------------

st.header("Compliance Checklist")

checks = {

    "Dataset Uploaded": dataset is not None,

    "Model Registered": model is not None,

    "Fairness Analysis": fairness > 0,

    "Privacy Analysis": privacy > 0,

    "Explainability Analysis": explainability > 0,

    "Accuracy Recorded": accuracy > 0

}

for item, passed in checks.items():
    passed = sum(checks.values())
failed = len(checks) - passed

st.session_state["policy_passed"] = passed
st.session_state["policy_failed"] = failed

    if passed:

        st.success(f"✅ {item}")

    else:

        st.error(f"❌ {item}")

st.divider()

# -----------------------------------------------------
# Detailed Assessment
# -----------------------------------------------------

st.header("Assessment")

assessment = pd.DataFrame({

    "Area":[

        "Fairness",

        "Privacy",

        "Explainability",

        "Accuracy"

    ],

    "Status":[

        "PASS" if fairness >= 80 else "REVIEW",

        "PASS" if privacy >= 80 else "REVIEW",

        "PASS" if explainability >= 80 else "REVIEW",

        "PASS" if accuracy >= 80 else "REVIEW"

    ],

    "Score":[

        fairness,

        privacy,

        explainability,

        accuracy

    ]

})

st.dataframe(

    assessment,

    use_container_width=True,

    hide_index=True

)

st.divider()

# -----------------------------------------------------
# Recommendations
# -----------------------------------------------------

st.header("Recommendations")

recommendations = []

if fairness < 80:

    recommendations.append(

        "Improve demographic fairness by reviewing training data and model thresholds."

    )

if privacy < 80:

    recommendations.append(

        "Reduce privacy risk by masking or anonymizing sensitive information."

    )

if explainability < 80:

    recommendations.append(

        "Increase model transparency with additional explainability analysis."

    )

if accuracy < 80:

    recommendations.append(

        "Retrain or optimize the model to improve predictive performance."

    )

if not recommendations:

    st.success(

        "All Responsible AI checks meet the recommended threshold."

    )
    st.session_state["recommendation_count"] = len(recommendations)

else:

    for recommendation in recommendations:

        st.warning(recommendation)

st.divider()

# -----------------------------------------------------
# Readiness Status
# -----------------------------------------------------

st.header("Deployment Readiness")
if overall >= 90:

    deployment = "Approved"

    st.success("🟢 Ready for production deployment.")

elif overall >= 75:

    deployment = "Conditional"

    st.warning("🟡 Ready with recommended improvements.")

else:

    deployment = "Rejected"

    st.error("🔴 Not recommended for production.")

st.session_state["deployment_status"] = deployment
if overall >= 90:

    st.success(

        "🟢 Ready for production deployment."

    )

elif overall >= 75:

    st.warning(

        "🟡 Ready with recommended improvements."

    )

else:

    st.error(

        "🔴 Not recommended for production until issues are resolved."

    )

st.divider()
st.session_state["deployment_status"] = (
    "Approved"
    if overall >= 90
    else "Conditional"
    if overall >= 75
    else "Rejected"
)
# -----------------------------------------------------
# Generate PDF Report
# -----------------------------------------------------

st.header("Generate Compliance Report")

organization = st.text_input(

    "Organization",

    value="AI Guardian OS"

)

analyst = st.text_input(

    "Prepared By",

    value="Developer"

)

report_name = st.text_input(

    "Report Name",

    value=f"Compliance_Report_Project_{project_id}"

)

generate = st.button(

    "📄 Generate PDF Report",

    type="primary"

)

if generate:

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    pdf_path = report_dir / f"{report_name}.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(str(pdf_path))

    elements = []

    elements.append(

        Paragraph(

            "<b>AI Guardian OS</b>",

            styles["Title"]

        )

    )

    elements.append(

        Paragraph(

            "Responsible AI Compliance Report",

            styles["Heading1"]

        )

    )

    elements.append(Spacer(1, 0.25 * inch))

    elements.append(

        Paragraph(

            f"<b>Organization:</b> {organization}",

            styles["Normal"]

        )

    )

    elements.append(

        Paragraph(

            f"<b>Prepared By:</b> {analyst}",

            styles["Normal"]

        )

    )

    elements.append(

        Paragraph(

            f"<b>Project ID:</b> {project_id}",

            styles["Normal"]

        )

    )

    elements.append(

        Paragraph(

            f"<b>Overall Compliance:</b> {overall}%",

            styles["Normal"]

        )

    )

    elements.append(

        Paragraph(

            f"<b>Risk Level:</b> {risk_level}",

            styles["Normal"]

        )

    )

    elements.append(Spacer(1, 0.3 * inch))

    table_data = [

        [

            "Category",

            "Score"

        ],

        [

            "Fairness",

            fairness

        ],

        [

            "Privacy",

            privacy

        ],

        [

            "Explainability",

            explainability

        ],

        [

            "Accuracy",

            accuracy

        ],

        [

            "Overall",

            overall

        ]

    ]

    table = Table(table_data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("BOTTOMPADDING",(0,0),(-1,0),10)

        ])

    )

    elements.append(table)

    elements.append(Spacer(1,0.3*inch))

    elements.append(

        Paragraph(

            "<b>Recommendations</b>",

            styles["Heading2"]

        )

    )

    if recommendations:

        for rec in recommendations:

            elements.append(

                Paragraph(

                    f"• {rec}",

                    styles["Normal"]

                )

            )

    else:

        elements.append(

            Paragraph(

                "No major issues identified.",

                styles["Normal"]

            )

        )

    certificate_id = str(uuid.uuid4())[:8].upper()

    elements.append(Spacer(1,0.3*inch))

    elements.append(

        Paragraph(

            f"<b>Certificate ID:</b> {certificate_id}",

            styles["Normal"]

        )

    )

    doc.build(elements)

    

    log(

        analyst,

        f"Generated compliance report for Project {project_id}",

        "INFO"

    )

    st.success(

        "Compliance report generated successfully."

    )

    with open(pdf_path, "rb") as pdf_file:

        st.download_button(

            "⬇ Download PDF Report",

            pdf_file,

            pdf_path.name,

            "application/pdf"

        )

# -----------------------------------------------------
# Export Excel Summary
# -----------------------------------------------------

st.header("Export Summary")

excel_buffer = io.BytesIO()

with pd.ExcelWriter(

    excel_buffer,

    engine="openpyxl"

) as writer:

    score_df.to_excel(

        writer,

        sheet_name="Compliance Scores",

        index=False

    )

    assessment.to_excel(

        writer,

        sheet_name="Assessment",

        index=False

    )

st.download_button(

    "⬇ Download Excel Summary",

    excel_buffer.getvalue(),

    "compliance_summary.xlsx",

    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)

# -----------------------------------------------------
# Completion Status
# -----------------------------------------------------

st.divider()

st.success(

    f"""

Compliance report generation completed successfully.

Project ID: {project_id}

Overall Compliance Score: {overall:.2f}%

Risk Level: {risk_level}

The generated PDF and Excel reports are now available for governance, auditing, and regulatory documentation.

"""

)
st.divider()

st.subheader("Responsible AI Compliance Status")

c1, c2 = st.columns(2)

c1.metric(
    "Compliance Score",
    f"{overall}%"
)

c2.metric(
    "Risk Level",
    risk_level
)

if overall >= 90:
    st.success("🟢 AI System Approved")

elif overall >= 75:
    st.warning("🟡 AI System Requires Minor Improvements")

else:
    st.error("🔴 AI System Not Approved")

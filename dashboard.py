import streamlit as st
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from reportlab.lib.units import inch

from modules.pdf_report import generate_pdf_report

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# =====================================================
# PDF REPORT GENERATOR
# =====================================================

def generate_research_pdf():

    pdf_path = "Airborne_Survey_Research_Report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()
    styles["BodyText"].leading = 20
    styles["BodyText"].alignment = 4

    styles["Heading1"].textColor = colors.HexColor(
        "#0F4C81"
    )

    styles["Heading1"].spaceAfter = 12

    styles["Heading2"].textColor = colors.HexColor(
        "#2563EB"
    )

    elements = []

    # =====================================
    # COVER PAGE
    # =====================================

    title = Paragraph(
        "Airborne Survey Quality Assessment Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1,20)
    )

    elements.append(
        Paragraph(
            """
            Machine Learning Based Airborne Survey
            Quality Assessment using Isolation Forest,
            Root Cause Analytics, Temporal Evolution Analysis
            and Survey Quality Index.
            """,
            styles["BodyText"]
        )
    )

    elements.append(
        PageBreak()
    )

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    elements.append(
        Paragraph(
            "Executive Summary",
            styles["Heading1"]
        )
    )

    total_lines = len(
        quality_df
    )

    avg_sqi = round(
        quality_df["SQI"].mean(),
        2
    )

    total_anomalies = len(
        analysis_df
    )

    summary = f"""
    Total Survey Lines: {total_lines}<br/>
    Detected Anomalies: {total_anomalies}<br/>
    Average SQI: {avg_sqi}<br/>
    """

    elements.append(
        Paragraph(
            summary,
            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1,20)
    )

    # =====================================
    # LINE HEALTH TABLE
    # =====================================

    elements.append(
        Paragraph(
            "Survey Quality Overview",
            styles["Heading1"]
        )
    )

    top_lines = quality_df.sort_values(
        "SQI",
        ascending=False
    )

    text = ""

    for _, row in top_lines.iterrows():

        text += (
            f"Line {row['LINE']} : "
            f"SQI={row['SQI']} "
            f"({row['Quality_Class']})<br/>"
        )

    elements.append(
        Paragraph(
            text,
            styles["BodyText"]
        )
    )

    # =====================================
    # EMBED VISUALIZATIONS
    # =====================================

    chart_list = [

        (
            "Trajectory Overview",
            f"{VIS_DIR}/trajectory_overview.png"
        ),

        (
            "Flightline Anomaly Map",
            f"{VIS_DIR}/flightline_anomaly_map.png"
        ),

        (
            "Severity Risk Map",
            f"{VIS_DIR}/severity_risk_map.png"
        ),

        (
            "Feature Correlation",
            f"{VIS_DIR}/feature_correlation_heatmap.png"
        ),

        (
            "Spatial Hotspots",
            f"{VIS_DIR}/spatial_anomaly_hotspots.png"
        ),

        (
            "Anomaly Density",
            f"{VIS_DIR}/anomaly_density_by_line.png"
        )
    ]

    for title, img_path in chart_list:

        if os.path.exists(img_path):

            elements.append(
                Paragraph(
                    title,
                    styles["Heading1"]
                )
            )

            elements.append(
                Spacer(1,10)
            )

            elements.append(
                Image(
                    img_path,
                    width=5.8*inch,
                    height=3.6*inch
                )
            )

            elements.append(
                Spacer(1,10)
            )   

    # =====================================
    # ROOT CAUSE SUMMARY
    # =====================================


    elements.append(
        Paragraph(
            "Root Cause Analysis",
            styles["Heading1"]
        )
    )

    cause_counts = (
        root_df["Root_Cause"]
        .value_counts()
    )

    cause_text = ""

    for cause, count in cause_counts.items():

        cause_text += (
            f"{cause}: "
            f"{count} anomalies<br/>"
        )

    elements.append(
        Paragraph(
            cause_text,
            styles["BodyText"]
        )
    )

    # =====================================
    # RESEARCH CONCLUSION
    # =====================================

    elements.append(
        Paragraph(
            "Research Conclusions",
            styles["Heading1"]
        )
    )

    conclusion = """
    The proposed framework successfully integrates
    Isolation Forest anomaly detection,
    root cause attribution,
    temporal anomaly evolution analysis
    and survey quality scoring.

    Results demonstrate the capability
    of identifying operational disturbances,
    ranking survey line quality,
    and providing interpretable decision support
    for airborne gravity survey missions.
    """

    elements.append(
        Paragraph(
            conclusion,
            styles["BodyText"]
        )
    )

    doc.build(elements)

    return pdf_path
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Airborne Survey Quality Assessment",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

.flashcard {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );

    border-radius:20px;
    padding:25px;

    margin-bottom:15px;

    border:1px solid #334155;

    box-shadow:
        0px 6px 20px rgba(0,0,0,0.25);

    transition:0.3s;
}

.flashcard:hover {
    transform:translateY(-5px);
}

.card-title {
    font-size:22px;
    font-weight:bold;
    color:#38bdf8;
}

.card-subtitle {
    color:#94a3b8;
    margin-top:10px;
    font-size:15px;
}

.search-box {
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.flashcard-front {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );

    color:white;

    border-radius:20px;

    padding:25px;

    height:220px;

    display:flex;
    justify-content:center;
    align-items:center;

    text-align:center;

    font-size:24px;
    font-weight:bold;

    border:1px solid #334155;

    box-shadow:0px 6px 18px rgba(0,0,0,0.25);
}

.flashcard-back {
    background: linear-gradient(
        135deg,
        #082f49,
        #0f172a
    );

    color:white;

    border-radius:20px;

    padding:20px;

    height:220px;

    overflow-y:auto;

    border:1px solid #38bdf8;

    box-shadow:0px 6px 18px rgba(0,0,0,0.25);
}

.flashcard-title {
    color:#38bdf8;
    font-size:22px;
    font-weight:bold;
    margin-bottom:10px;
}

.section-header {
    color:#38bdf8;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="metric-container"] {
    background-color: #1e293b;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 15px;
}

h1, h2, h3 {
    color: white;
}

div[data-testid="stMetricValue"] {
    color: #38bdf8;
}

div[data-testid="stMetricLabel"] {
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* =========================================
   FLASHCARD SYSTEM
========================================= */

.flip-card {
    background: transparent;
    width: 100%;
    height: 260px;
    perspective: 1000px;
    margin-bottom: 20px;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.8s;
    transform-style: preserve-3d;
}

.flip-toggle {
    display:none;
}

.flip-toggle:checked + .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {

    position:absolute;

    width:100%;
    height:100%;

    backface-visibility:hidden;

    border-radius:24px;

    overflow:hidden;

    border:1px solid rgba(56,189,248,0.25);

    box-shadow:
        0 8px 30px rgba(0,0,0,0.35);

}

/* FRONT */

.flip-card-front {

    background:
    linear-gradient(
        135deg,
        rgba(15,23,42,0.95),
        rgba(30,41,59,0.95)
    );

    display:flex;
    justify-content:center;
    align-items:center;

    color:white;

    font-size:24px;
    font-weight:700;

    cursor:pointer;
}

/* BACK */

.flip-card-back {

    background:
    linear-gradient(
        135deg,
        rgba(8,47,73,0.95),
        rgba(15,23,42,0.95)
    );

    color:white;

    transform:rotateY(180deg);

    padding:20px;

    overflow-y:auto;

    text-align:left;
}

.card-title {

    color:#38bdf8;

    font-size:20px;

    font-weight:bold;

    margin-bottom:12px;
}

.card-content {

    color:#e2e8f0;

    line-height:1.7;

    font-size:14px;
}

/* Glow effect */

.flip-card-front:hover {

    box-shadow:
        0 0 25px rgba(56,189,248,0.35),
        0 0 60px rgba(56,189,248,0.15);
}

/* Category title */

.flash-section {

    color:#38bdf8;

    font-size:28px;

    font-weight:700;

    margin-top:30px;

    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)
# =====================================================
# FILE PATHS
# =====================================================

RESULTS_DIR = "data/results"
VIS_DIR = "data/results/visualizations"

# =====================================================
# DATA LOADER
# =====================================================

@st.cache_data
def load_data():

    data = {}

    try:
        data["iso"] = pd.read_csv(
            f"{RESULTS_DIR}/isolation_forest_results.csv"
        )
    except:
        data["iso"] = pd.DataFrame()

    try:
        data["analysis"] = pd.read_csv(
            f"{RESULTS_DIR}/anomaly_analysis_results.csv"
        )
    except:
        data["analysis"] = pd.DataFrame()

    try:
        data["root_cause"] = pd.read_csv(
            f"{RESULTS_DIR}/root_cause_results.csv"
        )
    except:
        data["root_cause"] = pd.DataFrame()

    try:
        data["quality"] = pd.read_csv(
            f"{RESULTS_DIR}/survey_quality_results.csv"
        )
    except:
        data["quality"] = pd.DataFrame()

    try:
        data["ranking"] = pd.read_csv(
            f"{RESULTS_DIR}/line_health_ranking.csv"
        )
    except:
        data["ranking"] = pd.DataFrame()

    try:
        data["timeline"] = pd.read_csv(
            f"{RESULTS_DIR}/anomaly_timeline.csv"
        )
    except:
        data["timeline"] = pd.DataFrame()

    return data

# =====================================================
# LOAD DATA
# =====================================================

data = load_data()

analysis_df = pd.read_csv(
    "data/results/anomaly_analysis_results.csv"
)

root_df = pd.read_csv(
    "data/results/root_cause_results.csv"
)

quality_df = pd.read_csv(
    "data/results/survey_quality_results.csv"
)

timeline_df = pd.read_csv(
    "data/results/anomaly_timeline.csv"
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("✈️ Airborne Survey")

page = st.sidebar.radio(
    "Navigation",
    [
        "Flight Overview",
        "Flight Analytics",
        "Anomaly Explorer",
        "Root Cause Analytics",
        "Temporal Evolution",
        "Survey Health Dashboard",
        "Flashcards",
        "Research Summary"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    Airborne Survey Quality Assessment Platform

    Isolation Forest
    + Root Cause Analysis
    + SQI Assessment
    + Temporal Evolution Analysis
    """
)

# =====================================================
# PAGE 1
# FLIGHT OVERVIEW
# =====================================================

if page == "Flight Overview":

    st.title(
        "✈️ Airborne Survey Quality Assessment Dashboard"
    )

    st.markdown(
        "Research-grade anomaly detection and survey quality assessment platform."
    )

    quality_df = data["quality"]
    analysis_df = data["analysis"]

    total_lines = (
        len(quality_df)
        if not quality_df.empty
        else 0
    )

    total_anomalies = (
        len(analysis_df)
        if not analysis_df.empty
        else 0
    )

    avg_sqi = (
        round(quality_df["SQI"].mean(), 2)
        if not quality_df.empty
        else 0
    )

    best_line = (
        quality_df.iloc[
            quality_df["SQI"].idxmax()
        ]["LINE"]
        if not quality_df.empty
        else "-"
    )

    worst_line = (
        quality_df.iloc[
            quality_df["SQI"].idxmin()
        ]["LINE"]
        if not quality_df.empty
        else "-"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Survey Lines",
        total_lines
    )

    col2.metric(
        "Detected Anomalies",
        total_anomalies
    )

    col3.metric(
        "Average SQI",
        avg_sqi
    )

    col4.metric(
        "Best Line",
        best_line
    )

    col5.metric(
        "Worst Line",
        worst_line
    )

    st.markdown("---")

    colA, colB = st.columns(2)

    trajectory_img = (
        f"{VIS_DIR}/trajectory_overview.png"
    )

    anomaly_map_img = (
        f"{VIS_DIR}/flightline_anomaly_map.png"
    )

    with colA:

        st.subheader(
            "Survey Flight Trajectory"
        )

        if os.path.exists(trajectory_img):
            st.image(
                trajectory_img,
                use_container_width=True
            )
        else:
            st.warning(
                "trajectory_overview.png not found."
            )

    with colB:

        st.subheader(
            "Flightline Anomaly Map"
        )

        if os.path.exists(anomaly_map_img):
            st.image(
                anomaly_map_img,
                use_container_width=True
            )
        else:
            st.warning(
                "flightline_anomaly_map.png not found."
            )

# =====================================================
# PLACEHOLDERS
# =====================================================

elif page == "Flight Analytics":

    st.title("📊 Flight Analytics")

    st.markdown(
        """
        Comprehensive visualization suite for
        airborne survey anomaly detection and
        flight quality assessment.
        """
    )

    # ==========================================
    # FLIGHT BEHAVIOUR
    # ==========================================

    st.header("✈️ Flight Behaviour")

    col1, col2 = st.columns(2)

    with col1:

        img = f"{VIS_DIR}/trajectory_overview.png"

        if os.path.exists(img):
            st.image(
                img,
                caption="Survey Flight Trajectory",
                use_container_width=True
            )

    with col2:

        img = f"{VIS_DIR}/speed_profile.png"

        if os.path.exists(img):
            st.image(
                img,
                caption="Aircraft Speed Profile",
                use_container_width=True
            )

    st.divider()

    # ==========================================
    # ANOMALY DETECTION
    # ==========================================

    st.header("🚨 Anomaly Detection")

    col1, col2 = st.columns(2)

    with col1:

        img = f"{VIS_DIR}/anomaly_distribution.png"

        if os.path.exists(img):
            st.image(
                img,
                caption="Isolation Forest Classification",
                use_container_width=True
            )

    with col2:

        img = f"{VIS_DIR}/anomaly_scores.png"

        if os.path.exists(img):
            st.image(
                img,
                caption="Anomaly Score Distribution",
                use_container_width=True
            )

    st.divider()

    # ==========================================
    # SEVERITY ANALYSIS
    # ==========================================

    st.header("⚠ Severity Analysis")

    col1, col2 = st.columns(2)

    with col1:

        img = f"{VIS_DIR}/severity_distribution.png"

        if os.path.exists(img):
            st.image(
                img,
                caption="Severity Categories",
                use_container_width=True
            )

    with col2:

        img = f"{VIS_DIR}/severity_risk_map.png"

        if os.path.exists(img):
            st.image(
                img,
                caption="Severity Risk Map",
                use_container_width=True
            )

    st.divider()

    # ==========================================
    # SPATIAL ANALYSIS
    # ==========================================

    st.header("🛰 Spatial Analysis")

    col1, col2 = st.columns(2)

    with col1:

        img = f"{VIS_DIR}/flightline_anomaly_map.png"

        if os.path.exists(img):
            st.image(
                img,
                caption="Flightline Anomaly Map",
                use_container_width=True
            )

    with col2:

        img = f"{VIS_DIR}/spatial_anomaly_hotspots.png"

        if os.path.exists(img):
            st.image(
                img,
                caption="Spatial Hotspots",
                use_container_width=True
            )

    st.divider()

    # ==========================================
    # FEATURE ANALYSIS
    # ==========================================

    st.header("📈 Feature Analytics")

    col1, col2 = st.columns(2)

    with col1:

        img = f"{VIS_DIR}/feature_correlation_heatmap.png"

        if os.path.exists(img):
            st.image(
                img,
                caption="Feature Correlation Matrix",
                use_container_width=True
            )

    with col2:

        img = f"{VIS_DIR}/anomaly_feature_importance.png"

        if os.path.exists(img):
            st.image(
                img,
                caption="Feature Importance",
                use_container_width=True
            )

    st.divider()

    # ==========================================
    # ANOMALY DENSITY
    # ==========================================

    st.header("📍 Survey Line Statistics")

    img = f"{VIS_DIR}/anomaly_density_by_line.png"

    if os.path.exists(img):
        st.image(
            img,
            caption="Anomaly Density by Survey Line",
            use_container_width=True
        )

elif page == "Anomaly Explorer":

    st.title("🔍 Anomaly Explorer")

    st.markdown(
        """
        Investigate detected anomalies,
        severity patterns and root causes
        across individual survey lines.
        """
    )

    # ==========================================
    # LINE SELECTION
    # ==========================================

    available_lines = sorted(
        analysis_df["LINE"].unique()
    )

    selected_line = st.selectbox(
        "Select Survey Line",
        available_lines
    )

    line_anomalies = analysis_df[
        analysis_df["LINE"] == selected_line
    ]

    line_root = root_df[
        root_df["LINE"] == selected_line
    ]

    # ==========================================
    # NO ANOMALIES CASE
    # ==========================================

    if len(line_anomalies) == 0:

        st.success(
            f"Line {selected_line} contains no detected anomalies."
        )

    else:

        # ======================================
        # SUMMARY CARDS
        # ======================================

        total_anomalies = len(line_anomalies)

        avg_severity = round(
            line_anomalies["Severity_Score"].mean(),
            2
        )

        max_severity = round(
            line_anomalies["Severity_Score"].max(),
            2
        )

        dominant_cause = (
            line_root["Root_Cause"]
            .value_counts()
            .idxmax()
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Anomalies",
                total_anomalies
            )

        with c2:
            st.metric(
                "Avg Severity",
                avg_severity
            )

        with c3:
            st.metric(
                "Max Severity",
                max_severity
            )

        with c4:
            st.metric(
                "Top Cause",
                dominant_cause
            )

        st.divider()

        # ======================================
        # TABLE
        # ======================================

        st.subheader(
            "📋 Anomaly Details"
        )

        display_cols = [
            "Window_ID",
            "Severity_Score",
            "Severity_Category",
            "Start_Distance_m",
            "End_Distance_m"
        ]

        merged = pd.merge(
            line_anomalies,
            line_root[
                [
                    "Window_ID",
                    "Root_Cause"
                ]
            ],
            on="Window_ID",
            how="left"
        )

        st.dataframe(
            merged[
                display_cols +
                ["Root_Cause"]
            ],
            use_container_width=True,
            height=300
        )

        st.divider()

        # ======================================
        # CHARTS
        # ======================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "📈 Severity Distribution"
            )

            fig = px.histogram(
                line_anomalies,
                x="Severity_Score",
                nbins=10,
                title=""
            )

            fig.update_layout(
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            st.subheader(
                "🥧 Root Cause Breakdown"
            )

            cause_counts = (
                line_root["Root_Cause"]
                .value_counts()
                .reset_index()
            )

            cause_counts.columns = [
                "Cause",
                "Count"
            ]

            pie = px.pie(
                cause_counts,
                names="Cause",
                values="Count"
            )

            pie.update_layout(
                height=400
            )

            st.plotly_chart(
                pie,
                use_container_width=True
            )

        st.divider()

        # ======================================
        # TIMELINE
        # ======================================

        st.subheader(
            "📍 Anomaly Timeline"
        )

        line_anomalies = (
            line_anomalies
            .sort_values(
                "Start_Distance_m"
            )
        )

        timeline = px.scatter(
            line_anomalies,
            x="Start_Distance_m",
            y="Severity_Score",
            color="Severity_Category",
            size="Severity_Score",
            hover_data=[
                "Window_ID"
            ]
        )

        timeline.update_layout(
            xaxis_title=
                "Distance Along Line (m)",

            yaxis_title=
                "Severity Score",

            height=500
        )

        st.plotly_chart(
            timeline,
            use_container_width=True
        )

elif page == "Root Cause Analytics":

    st.title("🧠 Root Cause Analytics")

    st.markdown(
        """
        Comprehensive analysis of anomaly
        mechanisms affecting airborne survey quality.
        """
    )

    # ==================================================
    # KPI SECTION
    # ==================================================

    total_anomalies = len(root_df)

    total_causes = (
        root_df["Root_Cause"]
        .nunique()
    )

    most_common = (
        root_df["Root_Cause"]
        .value_counts()
        .idxmax()
    )

    severity_merge = root_df.copy()

    most_critical = (
        severity_merge
        .groupby("Root_Cause")["Severity_Score"]
        .mean()
        .idxmax()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Anomalies",
        total_anomalies
    )

    c2.metric(
        "Root Causes",
        total_causes
    )

    c3.metric(
        "Most Common",
        most_common
    )

    c4.metric(
        "Most Critical",
        most_critical
    )

    st.divider()

    # ==================================================
    # DONUT CHART
    # ==================================================

    col1, col2 = st.columns(2)

    cause_counts = (
        root_df["Root_Cause"]
        .value_counts()
        .reset_index()
    )

    cause_counts.columns = [
        "Root_Cause",
        "Count"
    ]

    with col1:

        st.subheader(
            "🥧 Root Cause Distribution"
        )

        pie = px.pie(
            cause_counts,
            names="Root_Cause",
            values="Count",
            hole=0.6
        )

        pie.update_layout(
            height=500
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    with col2:

        st.subheader(
            "📊 Cause Frequency Ranking"
        )

        bar = px.bar(
            cause_counts,
            x="Count",
            y="Root_Cause",
            orientation="h",
            text="Count"
        )

        bar.update_layout(
            height=500
        )

        st.plotly_chart(
            bar,
            use_container_width=True
        )

    st.divider()

    # ==================================================
    # ROOT CAUSE VS LINE
    # ==================================================

    st.subheader(
        "🔥 Root Cause vs Survey Line"
    )

    heatmap_df = pd.crosstab(
        root_df["LINE"],
        root_df["Root_Cause"]
    )

    fig, ax = plt.subplots(
        figsize=(12,6)
    )

    sns.heatmap(
        heatmap_df,
        annot=True,
        fmt="d",
        cmap="YlOrRd",
        ax=ax
    )

    ax.set_xlabel(
        "Root Cause"
    )

    ax.set_ylabel(
        "Survey Line"
    )

    st.pyplot(fig)

    st.divider()

    # ==================================================
    # SEVERITY COMPARISON
    # ==================================================

    st.subheader(
        "⚠️ Severity Distribution by Root Cause"
    )

    severity_plot = px.box(
        severity_merge,
        x="Root_Cause",
        y="Severity_Score",
        points="all"
    )

    severity_plot.update_layout(
        height=600
    )

    st.plotly_chart(
        severity_plot,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # CONTRIBUTION ANALYSIS
    # ==================================================

    st.subheader(
        "🎯 Mean Contribution by Root Cause"
    )

    contribution_df = (
        root_df
        .groupby("Root_Cause")
        ["Contribution_Value"]
        .mean()
        .reset_index()
    )

    contribution_df = (
        contribution_df
        .sort_values(
            "Contribution_Value",
            ascending=False
        )
    )

    contribution_plot = px.bar(
        contribution_df,
        x="Root_Cause",
        y="Contribution_Value",
        text_auto=".2f"
    )

    contribution_plot.update_layout(
        height=500
    )

    st.plotly_chart(
        contribution_plot,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # RESEARCH INSIGHT
    # ==================================================

    dominant = (
        root_df["Root_Cause"]
        .value_counts()
        .idxmax()
    )

    percentage = round(
        (
            root_df["Root_Cause"]
            .value_counts()
            .max()
            /
            len(root_df)
        ) * 100,
        2
    )

    st.success(
        f"""
        🔬 Research Insight

        {dominant} is the dominant anomaly mechanism,
        contributing approximately {percentage}% of
        all detected airborne survey anomalies.

        This indicates that flight disturbances are
        primarily driven by this operational factor.
        """
    )

elif page == "Temporal Evolution":

    st.title(
        "📈 Temporal Evolution Analysis"
    )

    st.markdown(
        """
        Analyze how anomaly behaviour
        evolves throughout the survey.

        Determine whether anomalies are:

        • Isolated Events

        • Clustered Disturbances

        • Sustained Flight Instabilities
        """
    )

    # ====================================
    # KPI SECTION
    # ====================================

    total_points = len(
        timeline_df
    )

    anomaly_points = len(
        timeline_df[
            timeline_df["Anomaly_Status"]
            == "Anomaly"
        ]
    )

    anomaly_ratio = round(
        (
            anomaly_points
            /
            total_points
        ) * 100,
        2
    )

    max_score = round(
        timeline_df[
            "Anomaly_Score"
        ].max(),
        3
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Timeline Points",
        total_points
    )

    c2.metric(
        "Anomalies",
        anomaly_points
    )

    c3.metric(
        "Anomaly %",
        f"{anomaly_ratio}%"
    )

    c4.metric(
        "Peak Score",
        max_score
    )

    st.divider()

    # ====================================
    # MAIN TIMELINE
    # ====================================

    st.subheader(
        "🚀 Distance vs Anomaly Score"
    )

    fig = px.line(
        timeline_df,
        x="Mid_Distance_m",
        y="Anomaly_Score"
    )

    anomaly_df = timeline_df[
        timeline_df["Anomaly_Status"]
        == "Anomaly"
    ]

    fig.add_scatter(
        x=anomaly_df[
            "Mid_Distance_m"
        ],
        y=anomaly_df[
            "Anomaly_Score"
        ],
        mode="markers",
        marker=dict(
            size=10
        ),
        name="Detected Anomaly"
    )

    fig.update_layout(
        height=700,
        xaxis_title=
        "Survey Distance (m)",

        yaxis_title=
        "Anomaly Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ====================================
    # LINE SELECTOR
    # ====================================

    st.subheader(
        "🎯 Survey Line Analysis"
    )

    selected_line = st.selectbox(
        "Choose Survey Line",
        sorted(
            timeline_df[
                "LINE"
            ].unique()
        )
    )

    line_df = timeline_df[
        timeline_df["LINE"]
        == selected_line
    ]

    line_chart = px.line(
        line_df,
        x="Mid_Distance_m",
        y="Anomaly_Score"
    )

    line_anomaly = line_df[
        line_df["Anomaly_Status"]
        == "Anomaly"
    ]

    line_chart.add_scatter(
        x=line_anomaly[
            "Mid_Distance_m"
        ],
        y=line_anomaly[
            "Anomaly_Score"
        ],
        mode="markers",
        marker=dict(
            size=12
        ),
        name="Anomaly"
    )

    line_chart.update_layout(
        height=600
    )

    st.plotly_chart(
        line_chart,
        use_container_width=True
    )

    st.divider()

    # ====================================
    # CLUSTER ANALYSIS
    # ====================================

    st.subheader(
        "🔥 Disturbance Cluster Analysis"
    )

    anomaly_locations = (
        anomaly_df[
            "Mid_Distance_m"
        ]
        .sort_values()
        .values
    )

    clusters = 0

    if len(
        anomaly_locations
    ) > 1:

        gaps = np.diff(
            anomaly_locations
        )

        cluster_threshold = 1000

        clusters = (
            gaps < cluster_threshold
        ).sum()

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Potential Clusters",
            clusters
        )

    with c2:

        st.metric(
            "Anomaly Events",
            anomaly_points
        )

    st.divider()

    # ====================================
    # DENSITY PLOT
    # ====================================

    st.subheader(
        "🌋 Anomaly Density Distribution"
    )

    density = px.histogram(
        anomaly_df,
        x="Mid_Distance_m",
        nbins=25
    )

    density.update_layout(
        height=500
    )

    st.plotly_chart(
        density,
        use_container_width=True
    )

    st.divider()

    # ====================================
    # RESEARCH INSIGHT
    # ====================================

    st.subheader(
        "🔬 Research Insight"
    )

    if clusters > anomaly_points * 0.4:

        message = """
        Detected anomaly events
        exhibit strong clustering behaviour.

        This suggests sustained flight
        disturbances rather than isolated
        operational noise.
        """

    else:

        message = """
        Most anomaly events appear
        isolated in nature.

        This suggests localized
        disturbances rather than
        prolonged flight instability.
        """

    st.success(
        message
    )

elif page == "Survey Health Dashboard":

    st.title("🏥 Survey Health Dashboard")

    st.markdown(
        """
        Comprehensive quality assessment of
        airborne gravity survey flight lines.
        """
    )

    # ==========================================
    # BASIC METRICS
    # ==========================================

    best_line = (
        quality_df
        .sort_values(
            "SQI",
            ascending=False
        )
        .iloc[0]
    )

    worst_line = (
        quality_df
        .sort_values(
            "SQI"
        )
        .iloc[0]
    )

    average_sqi = round(
        quality_df["SQI"].mean(),
        2
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Average SQI",
        average_sqi
    )

    c2.metric(
        "Best Line",
        int(best_line["LINE"])
    )

    c3.metric(
        "Best SQI",
        best_line["SQI"]
    )

    c4.metric(
        "Worst Line",
        int(worst_line["LINE"])
    )

    st.divider()

    # ==========================================
    # SQI BAR CHART
    # ==========================================

    st.subheader(
        "📊 Survey Quality Index by Flight Line"
    )

    sqi_chart = px.bar(
        quality_df,
        x="LINE",
        y="SQI",
        color="Quality_Class",
        text="SQI"
    )

    sqi_chart.update_layout(
        height=600
    )

    sqi_chart.add_hline(
        y=90,
        line_dash="dash"
    )

    sqi_chart.add_hline(
        y=75,
        line_dash="dash"
    )

    sqi_chart.add_hline(
        y=60,
        line_dash="dash"
    )

    st.plotly_chart(
        sqi_chart,
        use_container_width=True
    )

    st.divider()

    # ==========================================
    # QUALITY DISTRIBUTION
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "🥧 Quality Distribution"
        )

        pie = px.pie(
            quality_df,
            names="Quality_Class"
        )

        pie.update_layout(
            height=450
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    with col2:

        st.subheader(
            "🏆 Health Ranking"
        )

        ranking_df = (
            quality_df
            .sort_values(
                "SQI",
                ascending=False
            )
            .reset_index(drop=True)
        )

        ranking_df["Rank"] = (
            ranking_df.index + 1
        )

        st.dataframe(
            ranking_df[
                [
                    "Rank",
                    "LINE",
                    "SQI",
                    "Quality_Class"
                ]
            ],
            use_container_width=True
        )

    st.divider()

    # ==========================================
    # ANOMALY VS QUALITY
    # ==========================================

    st.subheader(
        "⚠️ Quality vs Anomaly Burden"
    )

    scatter = px.scatter(
        quality_df,
        x="Anomaly_Count",
        y="SQI",
        size="Mean_Severity",
        color="Quality_Class",
        hover_data=["LINE"]
    )

    scatter.update_layout(
        height=600
    )

    st.plotly_chart(
        scatter,
        use_container_width=True
    )

    st.divider()

    # ==========================================
    # TOP / BOTTOM LINES
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "🥇 Highest Quality Lines"
        )

        st.dataframe(
            quality_df
            .sort_values(
                "SQI",
                ascending=False
            )
            .head(5),
            use_container_width=True
        )

    with col2:

        st.subheader(
            "🚨 Lowest Quality Lines"
        )

        st.dataframe(
            quality_df
            .sort_values(
                "SQI"
            )
            .head(5),
            use_container_width=True
        )

    st.divider()

    # ==========================================
    # HEALTH STATUS CARD
    # ==========================================

    st.subheader(
        "🔬 Survey Assessment"
    )

    excellent = len(
        quality_df[
            quality_df["Quality_Class"]
            == "Excellent"
        ]
    )

    good = len(
        quality_df[
            quality_df["Quality_Class"]
            == "Good"
        ]
    )

    moderate = len(
        quality_df[
            quality_df["Quality_Class"]
            == "Moderate"
        ]
    )

    poor = len(
        quality_df[
            quality_df["Quality_Class"]
            == "Poor"
        ]
    )

    st.success(
        f"""
        Survey Quality Summary

        • Excellent Lines : {excellent}

        • Good Lines : {good}

        • Moderate Lines : {moderate}

        • Poor Lines : {poor}

        Best Performing Line :
        {int(best_line["LINE"])}

        Worst Performing Line :
        {int(worst_line["LINE"])}
        """
    )

elif page == "Flashcards":

    st.title(
        "🧠 Airborne Survey Learning Center"
    )

    st.markdown("""
    Learn how the project works,
    understand every feature,
    interpret visualizations,
    and explore the machine learning concepts
    used in airborne survey quality assessment.
    """)

    search = st.text_input(
        "🔍 Search Any Concept"
    )

    flashcards = {

        "✈ Flight Features": {

            "Mean Speed":
            """
Average aircraft speed inside a survey segment.

Why it matters:

• Stable speed produces better survey quality.

• Large speed changes may indicate turbulence,
pilot corrections or unstable flight.

Look for:
Higher variation = higher instability.
            """,

            "Mean Turn Rate":
            """
Measures how quickly the aircraft changes direction.

Why it matters:

Survey aircraft should normally fly straight.

High values indicate:

• Sharp turns

• Aggressive manoeuvres

• Navigation issues
            """,

            "Mean Curvature":
            """
Measures how much the flight path bends.

Low Curvature:

Straight survey line.

High Curvature:

Aircraft path is curving.

Important because:

Curved flight paths may reduce survey accuracy.
            """,

            "Mean Altitude Rate":
            """
Measures climbing and descending behaviour.

Low Values:

Stable altitude.

High Values:

Vertical instability.

Important because survey sensors
work best at consistent heights.
            """,

            "Mean Deviation":
            """
Most important navigation feature.

Measures how far aircraft moved away
from the planned survey line.

High deviation means:

• Navigation drift

• Tracking errors

• Lower survey quality
            """
        },

        "📊 Visualizations": {

            "Trajectory Overview":
            """
Shows complete aircraft path.

Used to understand:

• Survey coverage

• Flight geometry

• Overall mission pattern

This is the first visualization
operators usually inspect.
            """,

            "Flightline Anomaly Map":
            """
Displays anomaly locations directly
on survey flight lines.

Red points indicate:

Potential problem regions.

Helps locate exactly
where investigation is required.
            """,

            "Severity Risk Map":
            """
Shows anomaly severity.

Large points:

More severe anomalies.

Small points:

Less severe anomalies.

Used to prioritize operational review.
            """,

            "Temporal Evolution":
            """
Shows anomaly score over distance.

Answers:

Are anomalies isolated?

Are anomalies clustered?

Is there sustained instability?

Very important for research studies.
            """
        },

        "🤖 Machine Learning": {

            "Isolation Forest":
            """
Main anomaly detection model.

It learns what normal flight behaviour
looks like.

Anything significantly different
is marked as anomalous.

No labelled training data required.
            """,

            "Sliding Window":
            """
Flight trajectory is divided into
small segments called windows.

Each window becomes one sample
for machine learning.

This allows behaviour analysis
throughout the survey.
            """,

            "Anomaly Score":
            """
Numerical measure of abnormality.

More extreme score:

Higher anomaly likelihood.

Used for:

• Ranking anomalies

• Severity analysis

• Risk assessment
            """
        },

        "🔬 Research Outputs": {

            "Survey Quality Index":
            """
Overall quality score for each survey line.

100 = Perfect

0 = Extremely Poor

Categories:

Excellent

Good

Moderate

Poor

Provides a quick quality assessment.
            """,

            "Root Cause Analysis":
            """
Answers:

WHY did anomaly occur?

Possible causes:

• Sharp Turn

• Navigation Deviation

• Altitude Instability

• Speed Instability

• Multi-Parameter Disturbance
            """,

            "Line Health Ranking":
            """
Ranks survey lines from best to worst.

Used to identify:

✓ Best line

✓ Worst line

✓ Reflight candidates

Very useful for decision making.
            """
        }
    }

    if "flipped_cards" not in st.session_state:
        st.session_state.flipped_cards = {}

    for category, cards in flashcards.items():

        st.markdown(
            f"## {category}"
        )

        cols = st.columns(3)

        for idx, (title, desc) in enumerate(cards.items()):

            if (
                search
                and
                search.lower()
                not in title.lower()
                and
                search.lower()
                not in desc.lower()
            ):
                continue

            key = f"{category}_{title}"

            if key not in st.session_state.flipped_cards:
                st.session_state.flipped_cards[key] = False

            with cols[idx % 3]:

                if not st.session_state.flipped_cards[key]:

                    st.markdown(
                        f"""
                        <div class='flashcard-front'>
                        {title}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "🔄 Flip Card",
                        key=f"flip_{key}"
                    ):
                        st.session_state.flipped_cards[key] = True
                        st.rerun()

                else:

                     formatted_desc = desc.strip().replace(
    "\n",
    "<br>"
)
                     st.markdown(
                        f"""
                        <div class='flashcard-back'>
                           <div class='flashcard-title'>
                                 {title}
                           </div>
                           <div>
                                 {formatted_desc}
                           </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                     )

                     if st.button(
                        "↩ Back",
                        key=f"back_{key}"
                    ):
                        st.session_state.flipped_cards[key] = False
                        st.rerun()

        st.divider()

elif page == "Research Summary":

    st.title(
        "📑 Research Summary"
    )

    st.markdown(
        """
        Final consolidated interpretation of the
        airborne survey quality assessment.

        This page combines anomaly detection,
        root cause analysis, temporal evolution,
        survey quality assessment and line ranking
        into one operational overview.
        """
    )

    st.divider()

    # ==========================================
    # EXECUTIVE METRICS
    # ==========================================

    total_lines = len(
        quality_df
    )

    total_anomalies = len(
        analysis_df
    )

    average_sqi = round(
        quality_df["SQI"].mean(),
        2
    )

    best_line = (
        quality_df
        .sort_values(
            "SQI",
            ascending=False
        )
        .iloc[0]
    )

    worst_line = (
        quality_df
        .sort_values(
            "SQI"
        )
        .iloc[0]
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Survey Lines",
        total_lines
    )

    c2.metric(
        "Anomalies",
        total_anomalies
    )

    c3.metric(
        "Average SQI",
        average_sqi
    )

    c4.metric(
        "Best Line",
        int(best_line["LINE"])
    )

    c5.metric(
        "Worst Line",
        int(worst_line["LINE"])
    )

    st.divider()

    # ==========================================
    # OVERALL HEALTH
    # ==========================================

    st.subheader(
        "🏥 Survey Health Overview"
    )

    excellent = len(
        quality_df[
            quality_df["Quality_Class"]
            == "Excellent"
        ]
    )

    good = len(
        quality_df[
            quality_df["Quality_Class"]
            == "Good"
        ]
    )

    moderate = len(
        quality_df[
            quality_df["Quality_Class"]
            == "Moderate"
        ]
    )

    poor = len(
        quality_df[
            quality_df["Quality_Class"]
            == "Poor"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        health_chart = px.pie(
            quality_df,
            names="Quality_Class",
            hole=0.55
        )

        health_chart.update_layout(
            height=450
        )

        st.plotly_chart(
            health_chart,
            use_container_width=True
        )

    with col2:

        st.success(
            f"""
Survey Health Classification

Excellent Lines : {excellent}

Good Lines : {good}

Moderate Lines : {moderate}

Poor Lines : {poor}

Average Survey Quality Index : {average_sqi}
            """
        )

    st.divider()

    # ==========================================
    # ROOT CAUSE SUMMARY
    # ==========================================

    st.subheader(
        "🧠 Root Cause Summary"
    )

    dominant_cause = (
        root_df["Root_Cause"]
        .value_counts()
        .idxmax()
    )

    dominant_pct = round(
        (
            root_df["Root_Cause"]
            .value_counts()
            .max()
            /
            len(root_df)
        ) * 100,
        2
    )

    cause_counts = (
        root_df["Root_Cause"]
        .value_counts()
        .reset_index()
    )

    cause_counts.columns = [
        "Root_Cause",
        "Count"
    ]

    chart = px.bar(
        cause_counts,
        x="Root_Cause",
        y="Count",
        text="Count"
    )

    chart.update_layout(
        height=500
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    st.info(
        f"""
Dominant Root Cause:

{dominant_cause}

Contribution:

{dominant_pct}% of all detected anomalies.
        """
    )

    st.divider()

    # ==========================================
    # TEMPORAL SUMMARY
    # ==========================================

    st.subheader(
        "📈 Temporal Evolution Summary"
    )

    anomaly_points = timeline_df[
        timeline_df["Anomaly_Status"]
        == "Anomaly"
    ]

    timeline_chart = px.line(
        timeline_df,
        x="Mid_Distance_m",
        y="Anomaly_Score"
    )

    timeline_chart.add_scatter(
        x=anomaly_points["Mid_Distance_m"],
        y=anomaly_points["Anomaly_Score"],
        mode="markers",
        name="Anomaly"
    )

    timeline_chart.update_layout(
        height=500
    )

    st.plotly_chart(
        timeline_chart,
        use_container_width=True
    )

    st.divider()

    # ==========================================
    # TOP / BOTTOM LINES
    # ==========================================

    st.subheader(
        "🏆 Line Health Ranking"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### 🥇 Best Performing Lines"
        )

        st.dataframe(
            quality_df
            .sort_values(
                "SQI",
                ascending=False
            )
            .head(5),
            use_container_width=True
        )

    with col2:

        st.markdown(
            "### 🚨 Lowest Performing Lines"
        )

        st.dataframe(
            quality_df
            .sort_values(
                "SQI"
            )
            .head(5),
            use_container_width=True
        )

    st.divider()

    # ==========================================
    # RESEARCH FINDINGS
    # ==========================================

    st.subheader(
        "🔬 Key Research Findings"
    )

    st.markdown(
        f"""
### Finding 1

Isolation Forest successfully identified
{total_anomalies} anomalous flight windows
across {total_lines} survey lines.

---

### Finding 2

The dominant anomaly mechanism was
**{dominant_cause}**,
contributing approximately
**{dominant_pct}%**
of all detected anomalies.

---

### Finding 3

Survey Line
**{int(best_line["LINE"])}**
achieved the highest survey quality
with an SQI of
**{best_line["SQI"]}**.

---

### Finding 4

Survey Line
**{int(worst_line["LINE"])}**
showed the lowest survey quality,
indicating increased operational disturbance.

---

### Finding 5

Temporal evolution analysis revealed
how anomaly behaviour changes
throughout survey progression,
allowing identification of localized
and clustered disturbances.
        """
    )

    st.divider()

    # ==========================================
    # FINAL RESEARCH STATEMENT
    # ==========================================

    st.subheader(
        "📜 Final Statement"
    )

    st.success(
        f"""
This framework integrates trajectory analysis,
feature engineering, Isolation Forest anomaly detection,
root cause analysis, temporal evolution monitoring
and survey quality assessment into a unified system.

A total of {total_anomalies} anomalous flight windows
were detected across {total_lines} survey lines.

The average Survey Quality Index (SQI) was
{average_sqi}, with Line {int(best_line["LINE"])}
showing the strongest operational performance.

The developed methodology provides a scalable,
data-driven approach for evaluating airborne survey
quality and identifying operational disturbances
that may affect geophysical data acquisition.
        """
    )
    st.divider()

    st.subheader(
        "📄 Publication Report"
    )

    if st.button(
        "Generate Publication PDF"
    ):

        pdf_path = generate_research_pdf()

        st.success(
            "Publication report generated successfully."
        )

        with open(
            pdf_path,
            "rb"
        ) as file:

            st.download_button(
                label="⬇ Download Publication PDF",
                data=file,
                file_name=
                "Airborne_Survey_Research_Report.pdf",
                mime="application/pdf"
            )
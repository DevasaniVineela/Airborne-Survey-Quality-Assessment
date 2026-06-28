# Machine Learning-Based Airborne Survey Quality Assessment using Isolation Forest

An end-to-end machine learning framework developed during my internship at **CSIR–National Geophysical Research Institute (CSIR–NGRI)** for automated airborne gravity survey quality assessment.

The framework combines trajectory analytics, feature engineering, unsupervised anomaly detection, severity analysis, root cause identification, temporal evolution analysis, Survey Quality Index (SQI) computation, interactive visualization, and automated PDF report generation within a unified Streamlit dashboard.

---

# Project Overview

Airborne gravity surveys are widely used for geophysical exploration, geological mapping, mineral exploration, groundwater investigation, and national-scale geophysical studies. The quality of collected survey data directly affects the reliability of gravity measurements and subsequent interpretations.

Traditional survey quality assessment methods primarily rely on manual inspection and threshold-based analysis, making them time-consuming and difficult to scale for large airborne datasets.

This project introduces a machine learning-based framework that automatically detects anomalous flight behaviour, identifies possible operational causes, evaluates survey quality, and presents the results through an interactive dashboard.

---

# Key Features

- Automated airborne survey quality assessment
- Data preprocessing pipeline
- Feature engineering for flight behaviour analysis
- Sliding window generation
- Isolation Forest based anomaly detection
- Severity analysis of detected anomalies
- Root cause identification
- Temporal evolution analysis
- Survey Quality Index (SQI) computation
- Survey line quality ranking
- Interactive Streamlit dashboard
- Publication-style PDF report generation

---

# System Workflow

```text
Airborne Gravity Survey Dataset
            │
            ▼
Data Preprocessing
            │
            ▼
Feature Engineering
            │
            ▼
Sliding Window Generation
            │
            ▼
Isolation Forest
            │
            ▼
Anomaly Detection
            │
            ├──────────────┐
            ▼              ▼
Severity Analysis   Root Cause Analysis
            │              │
            └──────┬───────┘
                   ▼
        Temporal Evolution Analysis
                   │
                   ▼
     Survey Quality Index (SQI)
                   │
                   ▼
 Visualization & Dashboard
                   │
                   ▼
     Publication PDF Report
```

---

# Technologies Used

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Dashboard | Streamlit |
| Machine Learning | Scikit-learn (Isolation Forest) |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib |
| PDF Generation | ReportLab |
| File Handling | OpenPyXL |

---

# Machine Learning Pipeline

The complete analytical workflow consists of:

- Data Loading
- Data Preprocessing
- Feature Engineering
- Sliding Window Generation
- Isolation Forest Model
- Severity Analysis
- Root Cause Analysis
- Temporal Evolution Analysis
- Survey Quality Index (SQI)
- Visualization Generation
- Interactive Dashboard
- PDF Report Generation

---

# Dashboard Modules

The Streamlit dashboard contains multiple analytical modules including:

- Dashboard Overview
- Dataset Exploration
- Trajectory Analysis
- Isolation Forest Results
- Feature Analysis
- Root Cause Analysis
- Temporal Evolution
- Survey Quality Assessment
- Research Summary
- Publication Report Generation

---

# Generated Outputs

The framework automatically generates:

- Isolation Forest Results
- Anomaly Analysis Results
- Root Cause Results
- Survey Quality Results
- Line Health Ranking
- Temporal Evolution Results
- Visualization Images
- Publication-style PDF Report

---

# Project Outputs

The dashboard provides:

- Interactive visualizations
- Flight trajectory analysis
- Anomaly distribution maps
- Root cause visualization
- Severity analysis
- Temporal anomaly evolution
- Survey Quality Index
- Survey line rankings
- Publication-ready PDF reports

---

# Future Scope

Possible future enhancements include:

- Real-time anomaly detection
- Live aircraft telemetry integration
- Deep learning based anomaly detection
- Multi-sensor fusion
- Cloud deployment
- Automatic alert systems
- LiDAR survey support
- Magnetic survey support
- Drone-based airborne survey adaptation

---

# Research Background

This work was carried out as part of an internship project at:

**CSIR – National Geophysical Research Institute (CSIR–NGRI)**

The project focuses on improving airborne gravity survey quality assessment using machine learning and data-driven analytical techniques.

---

# Acknowledgements

I sincerely thank **CSIR–National Geophysical Research Institute (CSIR–NGRI)** for providing the opportunity to work on this project and for offering valuable guidance throughout the internship.

Special thanks to my project mentor for their continuous support and technical guidance during the development of this framework.

---

# Author

**Devasani Vineela**

B.Tech – Information Technology

Machine Learning | Data Analytics | Python | Streamlit | Geospatial Analytics

---

⭐ If you found this project useful, consider giving it a star.

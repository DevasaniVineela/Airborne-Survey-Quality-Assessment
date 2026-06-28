import pandas as pd
import numpy as np


def calculate_survey_quality(
        analysis_file,
        windows_file,
        output_file):

    print("\nLoading survey quality inputs...")

    analysis_df = pd.read_csv(analysis_file)
    windows_df = pd.read_csv(windows_file)

    # -------------------------------------
    # ALL SURVEY LINES
    # -------------------------------------

    all_lines = sorted(
        windows_df["LINE"].unique()
    )

    # -------------------------------------
    # NO ANOMALIES CASE
    # -------------------------------------

    if len(analysis_df) == 0:

        results = []

        for line in all_lines:

            results.append({
                "LINE": line,
                "Anomaly_Count": 0,
                "Mean_Severity": 0,
                "SQI": 100,
                "Quality_Class": "Excellent"
            })

        quality_df = pd.DataFrame(results)

        quality_df.to_csv(
            output_file,
            index=False
        )

        return quality_df

    # -------------------------------------
    # NORMALIZATION VALUES
    # -------------------------------------

    max_anomaly_count = (
        analysis_df
        .groupby("LINE")
        .size()
        .max()
    )

    max_mean_severity = (
        analysis_df
        .groupby("LINE")["Severity_Score"]
        .mean()
        .max()
    )

    results = []

    # -------------------------------------
    # PROCESS EVERY LINE
    # -------------------------------------

    for line in all_lines:

        line_df = analysis_df[
            analysis_df["LINE"] == line
        ]

        # -------------------------
        # NO ANOMALIES
        # -------------------------

        if len(line_df) == 0:

            results.append({

                "LINE": line,

                "Anomaly_Count": 0,

                "Mean_Severity": 0,

                "SQI": 100,

                "Quality_Class":
                    "Excellent"
            })

            continue

        anomaly_count = len(line_df)

        mean_severity = (
            line_df["Severity_Score"]
            .mean()
        )

        # -------------------------
        # NORMALIZED PENALTIES
        # -------------------------

        anomaly_penalty = (

            anomaly_count
            /
            max_anomaly_count

        ) * 40

        severity_penalty = (

            mean_severity
            /
            max_mean_severity

        ) * 40

        sqi = (

            100
            - anomaly_penalty
            - severity_penalty

        )

        sqi = round(
            max(0, sqi),
            2
        )

        # -------------------------
        # CLASSIFICATION
        # -------------------------

        if sqi >= 90:
            quality = "Excellent"

        elif sqi >= 75:
            quality = "Good"

        elif sqi >= 60:
            quality = "Moderate"

        else:
            quality = "Poor"

        results.append({

            "LINE": line,

            "Anomaly_Count":
                anomaly_count,

            "Mean_Severity":
                round(
                    mean_severity,
                    2
                ),

            "SQI":
                sqi,

            "Quality_Class":
                quality
        })

    quality_df = pd.DataFrame(
        results
    )

    quality_df = quality_df.sort_values(
        by="LINE"
    )

    quality_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nSurvey Quality saved:"
        f" {output_file}"
    )

    return quality_df
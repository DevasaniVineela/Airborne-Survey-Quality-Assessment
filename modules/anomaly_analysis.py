import pandas as pd
import numpy as np


FEATURES = [

    "Mean_Speed",
    "Std_Speed",

    "Mean_Absolute_Acceleration",
    "Max_Absolute_Acceleration",

    "Mean_Turn_Rate",
    "Max_Turn_Rate",

    "Mean_Curvature",
    "Max_Curvature",
    "High_Curvature_Count",

    "Mean_Absolute_Altitude_Rate",
    "Max_Absolute_Altitude_Rate",

    "Mean_Deviation",
    "Max_Deviation",
    "High_Deviation_Count"
]


def analyze_anomalies(
        input_file,
        output_file):

    print("\nLoading Isolation Forest results...")

    df = pd.read_csv(input_file)

    print(f"Rows: {len(df)}")

    anomalies = df[
        df["Anomaly_Label"] == -1
    ].copy()

    print(
        f"\nAnomalous Windows Found: "
        f"{len(anomalies)}"
    )

    if len(anomalies) == 0:

        print(
            "\nNo anomalies detected."
        )

        pd.DataFrame().to_csv(
            output_file,
            index=False
        )

        return pd.DataFrame()

    # -----------------------------------------
    # Baselines
    # -----------------------------------------

    print(
        "\nCalculating line baselines..."
    )

    normal_df = df[
        df["Anomaly_Label"] == 1
    ]

    line_baselines = (
        normal_df
        .groupby("LINE")[FEATURES]
        .mean()
    )

    analysis_rows = []

    print(
        "\nAnalyzing anomalies..."
    )

    for _, row in anomalies.iterrows():

        line = row["LINE"]

        if line not in line_baselines.index:
            continue

        baseline = (
            line_baselines.loc[line]
        )

        result = {

            "Window_ID":
                row["Window_ID"],

            "LINE":
                line,

            "Start_Distance_m":
                row["Start_Distance_m"],

            "End_Distance_m":
                row["End_Distance_m"],

            "Anomaly_Score":
                row["Anomaly_Score"]
        }

        severity_total = 0

        for feature in FEATURES:

            anomaly_value = row[feature]

            baseline_value = (
                baseline[feature]
            )

            if abs(baseline_value) < 1e-6:

                percent_change = (
                    anomaly_value * 100
                )

            else:

                percent_change = (

                    (
                        anomaly_value
                        -
                        baseline_value
                    )

                    /

                    abs(
                        baseline_value
                    )

                ) * 100

            result[
                f"{feature}_Baseline"
            ] = baseline_value

            result[
                f"{feature}_Percent_Change"
            ] = percent_change

            severity_total += abs(
                percent_change
            )

        result[
            "Severity_Score"
        ] = severity_total

        analysis_rows.append(
            result
        )

    analysis_df = pd.DataFrame(
        analysis_rows
    )

    if len(analysis_df) == 0:

        print(
            "\nNo analyzable anomalies."
        )

        analysis_df.to_csv(
            output_file,
            index=False
        )

        return analysis_df

    # -----------------------------------------
    # Ranking
    # -----------------------------------------

    analysis_df[
        "Severity_Rank"
    ] = (

        analysis_df[
            "Severity_Score"
        ]

        .rank(
            ascending=False,
            method="dense"
        )

        .astype(int)

    )

    analysis_df = (
        analysis_df
        .sort_values(
            by="Severity_Score",
            ascending=False
        )
    )

    # -----------------------------------------
    # Severity Class
    # -----------------------------------------

    severity_75 = (
        analysis_df[
            "Severity_Score"
        ].quantile(0.75)
    )

    severity_50 = (
        analysis_df[
            "Severity_Score"
        ].quantile(0.50)
    )

    def classify(score):

        if score >= severity_75:
            return "High"

        elif score >= severity_50:
            return "Moderate"

        else:
            return "Low"

    analysis_df[
        "Severity_Category"
    ] = (

        analysis_df[
            "Severity_Score"
        ]

        .apply(classify)

    )

    # -----------------------------------------
    # Save
    # -----------------------------------------

    analysis_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nAnalysis saved: "
        f"{output_file}"
    )

    print(
        f"Anomalies analyzed: "
        f"{len(analysis_df)}"
    )

    return analysis_df
import pandas as pd


def generate_anomaly_timeline(
        isolation_file,
        output_file):

    print("\nGenerating anomaly timeline...")

    df = pd.read_csv(isolation_file)

    timeline_df = df[[
        "Window_ID",
        "LINE",
        "Start_Distance_m",
        "End_Distance_m",
        "Anomaly_Score",
        "Anomaly_Status"
    ]].copy()

    timeline_df["Mid_Distance_m"] = (
        timeline_df["Start_Distance_m"]
        +
        timeline_df["End_Distance_m"]
    ) / 2

    timeline_df = timeline_df.sort_values(
        by="Mid_Distance_m"
    )

    timeline_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Timeline saved to: {output_file}"
    )

    return timeline_df
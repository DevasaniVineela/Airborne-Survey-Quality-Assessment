import pandas as pd


def rank_survey_lines(
        survey_quality_file,
        output_file):

    print("\nLoading Survey Quality Results...")

    df = pd.read_csv(
        survey_quality_file
    )

    if len(df) == 0:

        print("No survey quality data found.")

        pd.DataFrame().to_csv(
            output_file,
            index=False
        )

        return pd.DataFrame()

    # ---------------------------------
    # SORT BY SQI
    # ---------------------------------
    
    ranking_df = (
        df
        .sort_values(
            by="SQI",
            ascending=False
        )
        .reset_index(drop=True)
    )

    ranking_df["Rank"] = (
        ranking_df.index + 1
    )

    ranking_df = ranking_df[[
        "Rank",
        "LINE",
        "SQI",
        "Quality_Class",
        "Anomaly_Count",
        "Mean_Severity"
    ]]

    ranking_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nLine Health Ranking saved:"
        f" {output_file}"
    )
    ranking_df["Health_Status"] = ranking_df["Quality_Class"]
    print("\nTop 3 Best Lines")

    print(
        ranking_df.head(3)[
            ["LINE", "SQI"]
        ]
    )

    print("\nTop 3 Worst Lines")

    print(
        ranking_df.tail(3)[
            ["LINE", "SQI"]
        ]
    )

    return ranking_df
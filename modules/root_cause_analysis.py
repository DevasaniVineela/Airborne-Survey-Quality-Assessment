import pandas as pd


def classify_root_causes(
        input_file,
        output_file):

    print("\nLoading anomaly analysis results...")

    df = pd.read_csv(input_file)

    print(f"Anomalies: {len(df)}")

    if len(df) == 0:

        print("No anomalies found.")

        pd.DataFrame().to_csv(
            output_file,
            index=False
        )

        return pd.DataFrame()

    results = []

    for _, row in df.iterrows():

        contributions = {

            "Navigation Deviation":
                abs(
                    row[
                        "Mean_Deviation_Percent_Change"
                    ]
                ),

            "Sharp Aircraft Turn":
                max(
                    abs(
                        row[
                            "Mean_Turn_Rate_Percent_Change"
                        ]
                    ),
                    abs(
                        row[
                            "Mean_Curvature_Percent_Change"
                        ]
                    )
                ),

            "Altitude Instability":
                abs(
                    row[
                        "Mean_Absolute_Altitude_Rate_Percent_Change"
                    ]
                ),

            "Speed Instability":
                abs(
                    row[
                        "Mean_Speed_Percent_Change"
                    ]
                ),

            "Acceleration Disturbance":
                abs(
                    row[
                        "Mean_Absolute_Acceleration_Percent_Change"
                    ]
                )
        }

        dominant_cause = max(
            contributions,
            key=contributions.get
        )

        results.append({

            "Window_ID":
                row["Window_ID"],

            "LINE":
                row["LINE"],

            "Start_Distance_m":
                row["Start_Distance_m"],

            "End_Distance_m":
                row["End_Distance_m"],

            "Severity_Score":
                row["Severity_Score"],

            "Root_Cause":
                dominant_cause,

            "Contribution_Value":
                contributions[
                    dominant_cause
                ]
        })

    root_cause_df = pd.DataFrame(
        results
    )

    root_cause_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nRoot cause results saved:"
        f" {output_file}"
    )

    return root_cause_df
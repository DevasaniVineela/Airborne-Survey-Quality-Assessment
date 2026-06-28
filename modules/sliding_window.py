import pandas as pd
import numpy as np


def create_sliding_windows(
        input_file,
        output_file,
        window_size=2000.0,
        stride=50.0):

    print("\nLoading dataset...")

    df = pd.read_csv(input_file)

    print(f"Rows: {len(df)}")

    required_columns = [
        "LINE",
        "Distance_m",
        "Raw_Acceleration_mps2",
        "Altitude_Rate",
        "Curvature",
        "Heading_Change",
        "Turn_Rate_deg_per_sec",
        "Smoothed_Speed_mps"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    if "Survey_Line_Deviation_m" not in df.columns:
        print(
            "Survey_Line_Deviation_m not found."
            " Creating zero deviation column."
        )

        df["Survey_Line_Deviation_m"] = 0

    # --------------------------------------------------
    # Feature Engineering
    # --------------------------------------------------

    df["Absolute_Acceleration"] = (
        df["Raw_Acceleration_mps2"].abs()
    )

    df["Absolute_Altitude_Rate"] = (
        df["Altitude_Rate"].abs()
    )

    curvature_threshold = (
        df["Curvature"].quantile(0.95)
    )

    deviation_threshold = (
        df["Survey_Line_Deviation_m"].quantile(0.95)
    )

    df["High_Curvature_Flag"] = (
        df["Curvature"] > curvature_threshold
    ).astype(int)

    df["High_Deviation_Flag"] = (
        df["Survey_Line_Deviation_m"]
        > deviation_threshold
    ).astype(int)

    survey_lines = sorted(
        [x for x in df["LINE"].unique() if x != 1]
    )

    print("\nSurvey Lines:")
    print(survey_lines)

    all_windows = []
    window_id = 0

    for line in survey_lines:

        print(f"\nProcessing Line {line}")

        line_df = (
            df[df["LINE"] == line]
            .copy()
            .reset_index(drop=True)
        )

        line_df["Cumulative_Distance"] = (
            line_df["Distance_m"].cumsum()
        )

        line_length = (
            line_df["Cumulative_Distance"].max()
        )

        print(f"Length = {line_length:.2f} m")

        start_distance = 0
        windows_generated = 0

        while start_distance + window_size <= line_length:

            end_distance = (
                start_distance + window_size
            )

            window = line_df[
                (
                    line_df["Cumulative_Distance"]
                    >= start_distance
                )
                &
                (
                    line_df["Cumulative_Distance"]
                    < end_distance
                )
            ]

            if len(window) >= 30:

                record = {

                    "Window_ID":
                        window_id,

                    "LINE":
                        line,

                    "Start_Distance_m":
                        start_distance,

                    "End_Distance_m":
                        end_distance,

                    "Point_Count":
                        len(window),

                    "Mean_Speed":
                        window["Smoothed_Speed_mps"].mean(),

                    "Std_Speed":
                        window["Smoothed_Speed_mps"].std(ddof=0),

                    "Mean_Acceleration":
                        window["Raw_Acceleration_mps2"].mean(),

                    "Std_Acceleration":
                        window["Raw_Acceleration_mps2"].std(ddof=0),

                    "Mean_Absolute_Acceleration":
                        window["Absolute_Acceleration"].mean(),

                    "Max_Absolute_Acceleration":
                        window["Absolute_Acceleration"].max(),

                    "Mean_Heading_Change":
                        window["Heading_Change"].mean(),

                    "Max_Heading_Change":
                        window["Heading_Change"].max(),

                    "Mean_Turn_Rate":
                        window["Turn_Rate_deg_per_sec"].mean(),

                    "Max_Turn_Rate":
                        window["Turn_Rate_deg_per_sec"].max(),

                    "Mean_Curvature":
                        window["Curvature"].mean(),

                    "Max_Curvature":
                        window["Curvature"].max(),

                    "High_Curvature_Count":
                        window["High_Curvature_Flag"].sum(),

                    "Mean_Altitude_Rate":
                        window["Altitude_Rate"].mean(),

                    "Max_Altitude_Rate":
                        window["Altitude_Rate"].max(),

                    "Mean_Absolute_Altitude_Rate":
                        window[
                            "Absolute_Altitude_Rate"
                        ].mean(),

                    "Max_Absolute_Altitude_Rate":
                        window[
                            "Absolute_Altitude_Rate"
                        ].max(),

                    "Mean_Deviation":
                        window[
                            "Survey_Line_Deviation_m"
                        ].mean(),

                    "Max_Deviation":
                        window[
                            "Survey_Line_Deviation_m"
                        ].max(),

                    "High_Deviation_Count":
                        window[
                            "High_Deviation_Flag"
                        ].sum()
                }

                all_windows.append(record)

                window_id += 1
                windows_generated += 1

            start_distance += stride

        print(
            f"Windows Generated: {windows_generated}"
        )

    window_df = pd.DataFrame(all_windows)

    if len(window_df) == 0:
        raise ValueError(
            "No windows generated."
        )

    window_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nSliding windows saved: "
        f"{output_file}"
    )

    return window_df
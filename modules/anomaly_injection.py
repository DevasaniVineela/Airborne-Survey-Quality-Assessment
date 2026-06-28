import pandas as pd
import numpy as np


def inject_synthetic_anomalies(
        input_file,
        output_file=None
):

    print(
        "\nInjecting synthetic anomalies..."
    )

    df = pd.read_csv(input_file)

    df["Synthetic_Anomaly"] = 0

    anomaly_count = 0

    # -----------------------------------
    # Speed anomaly
    # -----------------------------------

    speed_rows = (
        df[df["LINE"] == 3000]
        .index
    )

    if len(speed_rows) > 400:

        idx = speed_rows[100:300]

        df.loc[
            idx,
            "Smoothed_Speed_mps"
        ] *= 1.8

        df.loc[
            idx,
            "Raw_Speed_mps"
        ] *= 1.8

        df.loc[
            idx,
            "Synthetic_Anomaly"
        ] = 1

    # -----------------------------------
    # Curvature anomaly
    # -----------------------------------

    curve_rows = (
        df[df["LINE"] == 3020]
        .index
    )

    if len(curve_rows) > 500:

        idx = curve_rows[150:350]

        df.loc[
            idx,
            "Curvature"
        ] *= 8

        df.loc[
            idx,
            "Heading_Change"
        ] *= 3

        df.loc[
            idx,
            "Synthetic_Anomaly"
        ] = 1

    # -----------------------------------
    # Turn rate anomaly
    # -----------------------------------

    turn_rows = (
        df[df["LINE"] == 3040]
        .index
    )

    if len(turn_rows) > 500:

        idx = turn_rows[200:400]

        df.loc[
            idx,
            "Turn_Rate_deg_per_sec"
        ] *= 6

        df.loc[
            idx,
            "Heading_Change"
        ] *= 4

        df.loc[
            idx,
            "Synthetic_Anomaly"
        ] = 1

    # -----------------------------------
    # Altitude anomaly
    # -----------------------------------

    alt_rows = (
        df[df["LINE"] == 3070]
        .index
    )

    if len(alt_rows) > 600:

        idx = alt_rows[250:500]

        oscillation = (
            np.sin(
                np.linspace(
                    0,
                    12*np.pi,
                    len(idx)
                )
            ) * 8
        )

        df.loc[
            idx,
            "Altitude_Rate"
        ] += oscillation

        df.loc[
            idx,
            "Synthetic_Anomaly"
        ] = 1

    # -----------------------------------
    # Survey deviation
    # -----------------------------------

    if (
        "Survey_Line_Deviation_m"
        in df.columns
    ):

        dev_rows = (
            df[df["LINE"] == 3090]
            .index
        )

        if len(dev_rows) > 500:

            idx = dev_rows[100:350]

            df.loc[
                idx,
                "Survey_Line_Deviation_m"
            ] += 50

            df.loc[
                idx,
                "Synthetic_Anomaly"
            ] = 1

    anomaly_count = (
        df["Synthetic_Anomaly"]
        .sum()
    )

    print(
        f"Injected anomalies: {anomaly_count}"
    )

    if output_file:

        df.to_csv(
            output_file,
            index=False
        )

        print(
            f"Saved: {output_file}"
        )

    return df
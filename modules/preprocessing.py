import pandas as pd
import numpy as np
from pyproj import Transformer
import matplotlib.pyplot as plt


def ddmm_to_dd(values):

    values = pd.to_numeric(
        values,
        errors="coerce"
    )

    degrees = np.floor(values / 100)

    minutes = values % 100

    return degrees + minutes / 60


def preprocess_gps_data(
        input_file,
        output_file=None,
        generate_plot=False,
        utm_epsg="EPSG:32644",
        min_movement_threshold=0.5,
        speed_window=5,
        acc_window=7
):

    print("\nLoading GPS dataset...")

    df = pd.read_csv(input_file)

    print(f"Rows: {len(df)}")

    # ----------------------------------
    # Cleaning
    # ----------------------------------

    df = df.drop_duplicates()

    df = df[
        (df["Glat"] != 0)
        &
        (df["Glong"] != 0)
    ].copy()

    df.reset_index(drop=True, inplace=True)

    # ----------------------------------
    # Coordinate conversion
    # ----------------------------------

    df["Lat_DD"] = ddmm_to_dd(df["Glat"])
    df["Long_DD"] = ddmm_to_dd(df["Glong"])

    transformer = Transformer.from_crs(
        "EPSG:4326",
        utm_epsg,
        always_xy=True
    )

    easting, northing = transformer.transform(
        df["Long_DD"],
        df["Lat_DD"]
    )

    df["Easting_X"] = easting
    df["Northing_Y"] = northing

    # ----------------------------------
    # Distance
    # ----------------------------------

    dx = np.diff(
        df["Easting_X"],
        prepend=df["Easting_X"].iloc[0]
    )

    dy = np.diff(
        df["Northing_Y"],
        prepend=df["Northing_Y"].iloc[0]
    )

    distance = np.sqrt(dx**2 + dy**2)

    distance[
        distance < min_movement_threshold
    ] = 0

    df["Distance_m"] = distance

    # ----------------------------------
    # Time
    # ----------------------------------

    delta_time = np.diff(
        df["GTime"],
        prepend=df["GTime"].iloc[0]
    )

    delta_time[
        delta_time <= 0
    ] = np.nan

    df["Delta_Time"] = delta_time

    # ----------------------------------
    # Speed
    # ----------------------------------

    raw_speed = np.divide(
        distance,
        delta_time,
        out=np.zeros_like(distance),
        where=~np.isnan(delta_time)
    )

    df["Raw_Speed_mps"] = raw_speed

    smooth_speed = (
        pd.Series(raw_speed)
        .rolling(
            window=speed_window,
            center=True,
            min_periods=1
        )
        .mean()
    )

    df["Smoothed_Speed_mps"] = smooth_speed

    df["Smoothed_Speed_kmph"] = (
        smooth_speed * 3.6
    )

    # ----------------------------------
    # Acceleration
    # ----------------------------------

    delta_speed = np.diff(
        raw_speed,
        prepend=raw_speed[0]
    )

    acceleration = np.divide(
        delta_speed,
        delta_time,
        out=np.zeros_like(delta_speed),
        where=(
            (~np.isnan(delta_time))
            &
            (delta_time >= 0.2)
        )
    )

    acceleration[
        np.abs(acceleration) > 15
    ] = np.nan

    acceleration = (
        pd.Series(acceleration)
        .interpolate(
            limit_direction="both"
        )
        .values
    )

    df["Raw_Acceleration_mps2"] = acceleration

    df["Smoothed_Acceleration_mps2"] = (
        pd.Series(acceleration)
        .rolling(
            window=acc_window,
            center=True,
            min_periods=1
        )
        .median()
    )

    # ----------------------------------
    # Heading
    # ----------------------------------

    heading = np.zeros(len(df))

    for i in range(1, len(df)):

        if distance[i] > 0:

            heading[i] = np.degrees(
                np.arctan2(
                    dy[i],
                    dx[i]
                )
            )

        else:

            heading[i] = heading[i-1]

    heading = (heading + 360) % 360

    df["Heading"] = heading

    heading_change = np.abs(
        np.diff(
            heading,
            prepend=heading[0]
        )
    )

    heading_change = np.where(
        heading_change > 180,
        360 - heading_change,
        heading_change
    )

    df["Heading_Change"] = heading_change

    df["Turn_Rate_deg_per_sec"] = np.divide(
        heading_change,
        delta_time,
        out=np.zeros_like(
            heading_change
        ),
        where=~np.isnan(delta_time)
    )

    df["Curvature"] = np.divide(
        np.radians(heading_change),
        distance + 1e-6
    )

    # ----------------------------------
    # Altitude
    # ----------------------------------

    altitude_change = np.diff(
        df["Galt"],
        prepend=df["Galt"].iloc[0]
    )

    df["Altitude_Change"] = altitude_change

    df["Altitude_Rate"] = np.divide(
        altitude_change,
        delta_time,
        out=np.zeros_like(
            altitude_change
        ),
        where=~np.isnan(delta_time)
    )

    # ----------------------------------
    # Save
    # ----------------------------------

    if output_file:

        df.to_csv(
            output_file,
            index=False
        )

        print(
            f"Saved: {output_file}"
        )

    # ----------------------------------
    # Plot
    # ----------------------------------

    if generate_plot:

        plt.figure(figsize=(10,8))

        plt.plot(
            df["Easting_X"],
            df["Northing_Y"]
        )

        plt.title(
            "Aircraft Trajectory"
        )

        plt.axis("equal")

        plt.show()

    return df
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA


def calculate_survey_line_deviation(
        input_file,
        output_file):

    print("\nLoading processed dataset...")

    df = pd.read_csv(input_file)

    print(f"Rows: {len(df)}")

    df["Survey_Line_Deviation_m"] = np.nan

    survey_lines = sorted(
        [line for line in df["LINE"].unique()
         if line != 1]
    )

    print("\nSurvey Lines Found:")
    print(survey_lines)

    for line_id in survey_lines:

        print(f"\nProcessing LINE {line_id}")

        line_mask = df["LINE"] == line_id

        line_df = df.loc[line_mask]

        if len(line_df) < 10:

            print("Skipped (too few points)")
            continue

        coords = line_df[
            ["Easting_X", "Northing_Y"]
        ].values

        pca = PCA(n_components=2)

        pca.fit(coords)

        center = pca.mean_

        direction = pca.components_[0]

        diff = coords - center

        projection_length = diff @ direction

        projected_points = (
            center
            +
            np.outer(
                projection_length,
                direction
            )
        )

        deviation = np.linalg.norm(
            coords - projected_points,
            axis=1
        )

        df.loc[
            line_mask,
            "Survey_Line_Deviation_m"
        ] = deviation

        print(
            f"Points: {len(line_df)} | "
            f"Mean Dev: {deviation.mean():.2f} m | "
            f"Max Dev: {deviation.max():.2f} m"
        )

    df["Survey_Line_Deviation_m"] = (
        df["Survey_Line_Deviation_m"]
        .fillna(0)
    )

    print("\n==========================")
    print("DEVIATION SUMMARY")
    print("==========================")

    print(
        df["Survey_Line_Deviation_m"]
        .describe()
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(f"\nSaved: {output_file}")

    return df


if __name__ == "__main__":

    calculate_survey_line_deviation(
        input_file="data/processed/gps_processed.csv",
        output_file="data/processed/gps_processed_with_deviation.csv"
    )
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
import joblib
import os


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


def train_isolation_forest(
        input_file,
        output_file,
        model_path,
        scaler_path):

    print("\nLoading window dataset...")

    df = pd.read_csv(input_file)

    X = df[FEATURES].copy()
    X = X.replace(
       [np.inf, -np.inf],
       np.nan
    )
    X = X.fillna(
        X.median(numeric_only=True)
    )

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=300,
        contamination=0.02,
        random_state=42
    )

    model.fit(X_scaled)

    df["Anomaly_Label"] = (
        model.predict(X_scaled)
    )

    df["Anomaly_Score"] = (
        model.decision_function(X_scaled)
    )

    df["Anomaly_Status"] = np.where(
        df["Anomaly_Label"] == -1,
        "Anomaly",
        "Normal"
    )

    df["Anomaly_Rank"] = (
        df["Anomaly_Score"]
        .rank(
            method="dense",
            ascending=True
        )
        .astype(int)
    )

    os.makedirs(
        os.path.dirname(model_path),
        exist_ok=True
    )

    joblib.dump(model, model_path)

    joblib.dump(
        scaler,
        scaler_path
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nModel saved: {model_path}"
    )

    print(
        f"Scaler saved: {scaler_path}"
    )

    return df
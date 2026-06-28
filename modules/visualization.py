import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_visualizations(
    gps_file,
    windows_file,
    iso_file,
    analysis_file,
    root_cause_file,
    survey_quality_file,
    timeline_file,
    output_folder="data/results/visualizations"
):

   plt.style.use('default')
   sns.set_theme(style="whitegrid")

   # ----------------------------------------------------------
   # LOAD DATA
   # ----------------------------------------------------------

   print("Loading datasets...")

   os.makedirs(output_folder, exist_ok=True)

   gps_df = pd.read_csv(gps_file)
   windows_df = pd.read_csv(windows_file)
   iso_df = pd.read_csv(iso_file)
   analysis_df = pd.read_csv(analysis_file)
   root_cause_df = pd.read_csv(root_cause_file)
   quality_df = pd.read_csv(survey_quality_file)
   timeline_df = pd.read_csv(timeline_file)
   
   print("GPS rows:", len(gps_df))
   print("Windows:", len(iso_df))
   print("Anomalies:", len(analysis_df))

   # ----------------------------------------------------------
   # FIGURE 1
   # TRAJECTORY OVERVIEW
   # ----------------------------------------------------------

   print("Creating Figure 1...")

   plt.figure(figsize=(12, 8))

   plt.plot(
      gps_df["Easting_X"],
      gps_df["Northing_Y"],
      color="steelblue",
      linewidth=0.6,
      alpha=0.8
   )

   plt.title(
      "Airborne Survey Flight Trajectory",
      fontsize=16,
      weight='bold'
   )

   plt.xlabel("Easting (m)")
   plt.ylabel("Northing (m)")
   plt.tight_layout()

   plt.savefig(
      f"{output_folder}/trajectory_overview.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()

   # ----------------------------------------------------------
   # FIGURE 2
   # SPEED PROFILE
   # ----------------------------------------------------------

   print("Creating Figure 2...")

   plt.figure(figsize=(14,6))

   plt.plot(
      gps_df["Distance_m"]/1000,
      gps_df["Smoothed_Speed_mps"],
      linewidth=1
   )

   plt.title(
      "Aircraft Speed Profile Along Survey Distance",
      fontsize=16,
      weight='bold'
   )

   plt.xlabel("Distance Along Survey (km)")
   plt.ylabel("Speed (m/s)")

   plt.tight_layout()

   plt.savefig(
      f"{output_folder}/speed_profile.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()

   # ----------------------------------------------------------
   # FIGURE 3
   # ANOMALY DISTRIBUTION
   # ----------------------------------------------------------

   print("Creating Figure 3...")

   plt.figure(figsize=(8,6))

   sns.countplot(
      data=iso_df,
      x="Anomaly_Status"
   )

   plt.title(
      "Isolation Forest Classification Distribution",
      fontsize=16,
      weight='bold'
   )

   plt.xlabel("Classification")
   plt.ylabel("Number of Windows")

   plt.tight_layout()

   plt.savefig(
      f"{output_folder}/anomaly_distribution.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()

   # ----------------------------------------------------------
   # FIGURE 4
   # ANOMALY SCORES
   # ----------------------------------------------------------

   print("Creating Figure 4...")

   plt.figure(figsize=(10,6))

   sns.histplot(
      iso_df["Anomaly_Score"],
      bins=30,
      kde=True
   )

   plt.axvline(
      0,
      linestyle='--',
      linewidth=2
   )

   plt.title(
      "Isolation Forest Anomaly Score Distribution",
      fontsize=16,
      weight='bold'
   )

   plt.xlabel("Anomaly Score")
   plt.ylabel("Count")

   plt.tight_layout()

   plt.savefig(
      f"{output_folder}/anomaly_scores.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()

   # ----------------------------------------------------------
   # FIGURE 5
   # SEVERITY DISTRIBUTION
   # ----------------------------------------------------------

   print("Creating Figure 5...")

   plt.figure(figsize=(8,6))

   severity_order = [
      "Low",
      "Moderate",
      "High"
   ]

   sns.countplot(
      data=analysis_df,
      x="Severity_Category",
      order=severity_order
   )

   plt.title(
      "Severity Category Distribution",
      fontsize=16,
      weight='bold'
   )

   plt.xlabel("Severity Category")
   plt.ylabel("Number of Anomalies")

   plt.tight_layout()

   plt.savefig(
      f"{output_folder}/severity_distribution.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()

   # ----------------------------------------------------------
   # FIGURE 6 — flightline_anomaly_map.png
   # ----------------------------------------------------------

   print("Generating Figure 7: Flightline Anomaly Map...")

   plt.figure(figsize=(14,8))

   for line in gps_df["LINE"].unique():
      line_data = gps_df[gps_df["LINE"] == line]

      plt.plot(
         line_data["Easting_X"],
         line_data["Northing_Y"],
         alpha=0.4,
         linewidth=1
      )

   for _, row in analysis_df.iterrows():

      line_points = gps_df[gps_df["LINE"] == row["LINE"]]

      midpoint = (
         row["Start_Distance_m"] +
         row["End_Distance_m"]
      ) / 2

      line_points = line_points.copy()

      line_points["Cumulative_Distance"] = (
         line_points["Distance_m"].cumsum()
      )

      idx = (
         line_points["Cumulative_Distance"]
         - midpoint
      ).abs().idxmin()

      plt.scatter(
         line_points.loc[idx, "Easting_X"],
         line_points.loc[idx, "Northing_Y"],
         s=max(row["Severity_Score"]/25, 20),
         c="red",
         edgecolors="black"
      )

   plt.title("Flight Line Anomaly Map")
   plt.xlabel("Easting (m)")
   plt.ylabel("Northing (m)")
   plt.grid(True)

   plt.tight_layout()
   plt.savefig(
      f"{output_folder}/flightline_anomaly_map.png",
      dpi=300,
      bbox_inches="tight"
   )
   plt.close()

   # ----------------------------------------------------------
   # FIGURE 7 — feature_correlation_heatmap.png
   # ----------------------------------------------------------

   print("Generating Figure 8: Feature Correlation Heatmap...")

   feature_cols = [
      "Mean_Speed",
      "Std_Speed",
      "Mean_Absolute_Acceleration",
      "Max_Absolute_Acceleration",
      "Mean_Turn_Rate",
      "Max_Turn_Rate",
      "Mean_Curvature",
      "Max_Curvature",
      "Mean_Absolute_Altitude_Rate",
      "Max_Absolute_Altitude_Rate",
      "Mean_Deviation",
      "Max_Deviation"
   ]

   corr_matrix = windows_df[feature_cols].corr()

   plt.figure(figsize=(12,10))

   sns.heatmap(
      corr_matrix,
      cmap="coolwarm",
      center=0,
      annot=True,
      fmt=".2f"
   )

   plt.title("Feature Correlation Matrix")

   plt.tight_layout()
   plt.savefig(
      f"{output_folder}/feature_correlation_heatmap.png",
      dpi=300,
      bbox_inches="tight"
   )
   plt.close()


   #-----------------------------------------------------------
   # FIGURE 10 — severity_risk_map.png
   #-----------------------------------------------------------

   print("Generating Figure 11: Severity Risk Map...")

   plt.figure(figsize=(12,7))

   sns.scatterplot(
      data=analysis_df,
      x="Anomaly_Score",
      y="Severity_Score",
      hue="Severity_Category",
      size="Severity_Score",
      sizes=(80,800)
   )

   plt.title("Severity Risk Map")
   plt.xlabel("Isolation Forest Score")
   plt.ylabel("Severity Score")

   plt.tight_layout()
   plt.savefig(
      f"{output_folder}/severity_risk_map.png",
      dpi=300,
      bbox_inches="tight"
   )
   plt.close()

   # ----------------------------------------------------------
   # FIGURE 11 — anomaly_density_by_line.png
   # ----------------------------------------------------------

   print("Generating Figure 12: Anomaly Density by Line...")

   line_counts = (
      analysis_df.groupby("LINE")
      .size()
      .reset_index(name="Anomaly_Count")
   )

   plt.figure(figsize=(10,6))

   sns.barplot(
      data=line_counts,
      x="LINE",
      y="Anomaly_Count"
   )

   plt.title("Anomaly Density by Survey Line")
   plt.xlabel("Survey Line")
   plt.ylabel("Number of Anomalies")

   for i, row in line_counts.iterrows():
      plt.text(
         i,
         row["Anomaly_Count"] + 0.05,
         str(row["Anomaly_Count"]),
         ha="center"
      )

   plt.tight_layout()
   plt.savefig(
      f"{output_folder}/anomaly_density_by_line.png",
      dpi=300,
      bbox_inches="tight"
   )
   plt.close()


   # ----------------------------------------------------------
   # FIGURE 13 — SPATIAL ANOMALY HOTSPOTS
   # ----------------------------------------------------------

   print("Generating Figure 14: Spatial Anomaly Hotspots...")

   hotspot_df = []

   for _, row in analysis_df.iterrows():

      line_points = gps_df[
         gps_df["LINE"] == row["LINE"]
      ]

      midpoint = (
         row["Start_Distance_m"] +
         row["End_Distance_m"]
      ) / 2

      idx = (
         line_points["Distance_m"] -
         midpoint
      ).abs().idxmin()

      hotspot_df.append([
         gps_df.loc[idx,"Easting_X"],
         gps_df.loc[idx,"Northing_Y"]
      ])

   hotspot_df = pd.DataFrame(
      hotspot_df,
      columns=["X","Y"]
   )

   plt.figure(figsize=(12,8))
   if len(hotspot_df) > 1:
      sns.kdeplot(
         data=hotspot_df,
         x="X",
         y="Y",
         fill=True,
         levels=20,
         cmap="Reds"
      )

   plt.scatter(
      hotspot_df["X"],
      hotspot_df["Y"],
      color="black",
      s=40
   )

   plt.title("Spatial Distribution of Anomaly Hotspots")

   plt.savefig(
      f"{output_folder}/spatial_anomaly_hotspots.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()

   # ----------------------------------------------------------
   # FIGURE 15 — FEATURE IMPORTANCE
   # ----------------------------------------------------------

   print("Generating Figure 16: Feature Importance...")

   importance_scores = {}

   for col in analysis_df.columns:

      if "Percent_Change" in col:

         importance_scores[col] = (
               abs(analysis_df[col]).mean()
         )

   importance_df = pd.DataFrame({
      "Feature": importance_scores.keys(),
      "Importance": importance_scores.values()
   })

   importance_df = (
      importance_df
      .sort_values(
         "Importance",
         ascending=False
      )
      .head(10)
   )

   plt.figure(figsize=(12,6))

   sns.barplot(
      data=importance_df,
      x="Importance",
      y="Feature"
   )

   plt.title(
      "Top Flight Parameters Driving Anomalies"
   )

   plt.savefig(
      f"{output_folder}/anomaly_feature_importance.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()

   # ----------------------------------------------------------
   # FIGURE 16 — SURVEY LINE HEALTH DASHBOARD
   # ----------------------------------------------------------

   print("Generating Figure 17: Survey Line Health Dashboard...")

   health_df = (
      analysis_df
      .groupby("LINE")
      .agg({
         "Severity_Score":"mean",
         "Window_ID":"count"
      })
      .reset_index()
   )

   health_df.columns = [
      "LINE",
      "Mean_Severity",
      "Anomaly_Count"
   ]

   plt.figure(figsize=(10,6))

   scatter = plt.scatter(
      health_df["Anomaly_Count"],
      health_df["Mean_Severity"],
      s=health_df["Mean_Severity"]/2,
      alpha=0.7
   )

   for _, row in health_df.iterrows():

      plt.text(
         row["Anomaly_Count"],
         row["Mean_Severity"],
         str(int(row["LINE"]))
      )

   plt.title(
      "Survey Line Health Dashboard"
   )

   plt.xlabel("Number of Anomalies")
   plt.ylabel("Average Severity Score")

   plt.grid(True)

   plt.savefig(
      f"{output_folder}/survey_line_health_dashboard.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()


   # ----------------------------------------------------------
   # FIGURE 17 — ROOT CAUSE DISTRIBUTION
   # ----------------------------------------------------------

   print("Generating Root Cause Distribution...")

   plt.figure(figsize=(10,6))

   sns.countplot(
      data=root_cause_df,
      x="Root_Cause"
   )

   plt.xticks(rotation=20)

   plt.title(
      "Root Cause Distribution"
   )

   plt.xlabel("Root Cause")
   plt.ylabel("Number of Anomalies")

   plt.tight_layout()

   plt.savefig(
      f"{output_folder}/root_cause_distribution.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()


   # ----------------------------------------------------------
   # Survey Quality 
   # ----------------------------------------------------------
   quality_df = pd.read_csv(
      survey_quality_file
   )

   plt.figure(figsize=(10,6))

   quality_df_sorted = (
      quality_df
      .sort_values("LINE")
   )

   sns.barplot(
      data=quality_df_sorted,
      x="LINE",
      y="SQI"
   )

   for i, row in quality_df_sorted.iterrows():

      plt.text(
         i,
         row["SQI"] + 1,
         f"{row['SQI']:.0f}",
         ha="center"
      )

   plt.axhline(
      90,
      color="green",
      linestyle="--",
      label="Excellent"
   )

   plt.axhline(
      75,
      color="orange",
      linestyle="--",
      label="Good"
   )

   plt.axhline(
      60,
      color="red",
      linestyle="--",
      label="Moderate"
   )

   plt.title(
      "Survey Quality Index by Flight Line"
   )

   plt.ylabel("SQI")

   plt.legend()

   plt.tight_layout()

   plt.savefig(
      f"{output_folder}/survey_quality_index.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()


   # ----------------------------------------------------------
   # TEMPORAL EVOLUTION ANALYSIS
   # ----------------------------------------------------------

   print(
      "Generating Temporal Evolution Analysis..."
   )

   plt.figure(figsize=(14,6))

   normal_df = timeline_df[
      timeline_df["Anomaly_Status"] == "Normal"
   ]

   anomaly_df = timeline_df[
      timeline_df["Anomaly_Status"] == "Anomaly"
   ]

   plt.plot(
      normal_df["Mid_Distance_m"] / 1000,
      normal_df["Anomaly_Score"],
      '.',
      alpha=0.3,
      label="Normal"
   )

   plt.scatter(
      anomaly_df["Mid_Distance_m"] / 1000,
      anomaly_df["Anomaly_Score"],
      color="red",
      s=30,
      label="Anomaly"
   )

   plt.axhline(
      0,
      linestyle="--",
      linewidth=1
   )

   plt.title(
      "Temporal Evolution of Anomalies"
   )

   plt.xlabel(
      "Distance Along Survey (km)"
   )

   plt.ylabel(
      "Isolation Forest Score"
   )

   plt.legend()

   plt.tight_layout()

   plt.savefig(
      f"{output_folder}/temporal_evolution_analysis.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()
# =========================================================
# Line Health Ranking
# =========================================================

   ranking_df = pd.read_csv(
      "data/results/line_health_ranking.csv"
   )

   plt.figure(figsize=(12,6))

   sns.barplot(
      data=ranking_df,
      x="LINE",
      y="SQI"
   )

   plt.title(
      "Survey Line Health Ranking"
   )

   plt.ylabel("SQI")

   plt.tight_layout()

   plt.savefig(
      f"{output_folder}/line_health_ranking.png",
      dpi=300,
      bbox_inches="tight"
   )

   plt.close()

   # ----------------------------------------------------------
   # SUMMARY
   # ----------------------------------------------------------

   print("\n" + "="*60)
   print("ALL 16 FIGURES GENERATED SUCCESSFULLY")
   print("="*60)

   print(f"Saved to folder: {output_folder}")

   for i in range(1,18):
      print(f"Figure {i} generated")

   print("""
   1. trajectory_overview.png
   2. speed_profile.png
   3. anomaly_distribution.png
   4. anomaly_scores.png
   5. severity_distribution.png
   6. flightline_anomaly_map.png
   7. feature_correlation_heatmap.png


   10. severity_risk_map.png
   11. anomaly_density_by_line.png

   13. spatial_anomaly_hotspots.png

   15.anomaly_feature_importance.png
   16.survey_line_health_dashboard.png
   """)
   return output_folder
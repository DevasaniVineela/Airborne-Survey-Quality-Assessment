import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    Table,
    TableStyle
)

from reportlab.lib.styles import (
getSampleStyleSheet
)

from reportlab.lib import colors
from reportlab.lib.units import inch

import pandas as pd

def generate_pdf_report(
   quality_file,
   analysis_file,
   root_cause_file,
   output_pdf
   ):

   quality_df = pd.read_csv(quality_file)
   analysis_df = pd.read_csv(analysis_file)
   root_df = pd.read_csv(root_cause_file)

   VIS_DIR = "data/results/visualizations"

   doc = SimpleDocTemplate(output_pdf)

   styles = getSampleStyleSheet()

   story = []

   # ==================================================
   # TITLE
   # ==================================================

   story.append(
      Paragraph(
         "Airborne Survey Quality Assessment Report",
         styles["Title"]
      )
   )

   story.append(
      Paragraph(
         "Machine Learning Based Trajectory Quality Evaluation",
         styles["Heading2"]
      )
   )

   story.append(
      Spacer(1,20)
   )

   # ==================================================
   # EXECUTIVE SUMMARY
   # ==================================================

   total_lines = len(quality_df)

   total_anomalies = len(analysis_df)

   avg_sqi = round(
      quality_df["SQI"].mean(),
      2
   )

   best_line = (
      quality_df
      .sort_values(
         "SQI",
         ascending=False
      )
      .iloc[0]["LINE"]
   )

   worst_line = (
      quality_df
      .sort_values(
         "SQI"
      )
      .iloc[0]["LINE"]
   )

   story.append(
      Paragraph(
         "Executive Summary",
         styles["Heading1"]
      )
   )

   summary = f"""
   This report presents a comprehensive airborne survey
   quality assessment framework developed using machine
   learning, trajectory analytics and anomaly detection.

   Total Survey Lines Analysed: {total_lines}<br/>
   Total Detected Anomalies: {total_anomalies}<br/>
   Average Survey Quality Index: {avg_sqi}<br/>
   Best Performing Line: {best_line}<br/>
   Lowest Performing Line: {worst_line}
   """

   story.append(
      Paragraph(
         summary,
         styles["BodyText"]
      )
   )

   story.append(
      Spacer(1,20)
   )

   # ==================================================
   # FLIGHT OVERVIEW
   # ==================================================

   story.append(
      Paragraph(
         "1. Flight Overview",
         styles["Heading1"]
      )
   )

   story.append(
      Paragraph(
         """
         The trajectory overview provides a visual
         representation of the survey mission path.
         It helps evaluate coverage consistency,
         flight geometry and overall survey execution.
         """,
         styles["BodyText"]
      )
   )

   trajectory = f"{VIS_DIR}/trajectory_overview.png"

   if os.path.exists(trajectory):

      story.append(
         Spacer(1,10)
      )

      story.append(
         Image(
               trajectory,
               width=5.5*inch,
               height=3.5*inch
         )
      )

      story.append(
         Paragraph(
               "Figure 1. Survey Flight Trajectory",
               styles["Italic"]
         )
      )

   story.append(
      Spacer(1,20)
   )

   # ==================================================
   # ANOMALY ANALYSIS
   # ==================================================

   story.append(
      Paragraph(
         "2. Anomaly Detection Analysis",
         styles["Heading1"]
      )
   )

   story.append(
      Paragraph(
         """
         Isolation Forest was used to identify
         abnormal flight behaviour throughout
         the airborne survey mission.
         """,
         styles["BodyText"]
      )
   )

   anomaly_map = f"{VIS_DIR}/flightline_anomaly_map.png"

   if os.path.exists(anomaly_map):

      story.append(
         Spacer(1,10)
      )

      story.append(
         Image(
               anomaly_map,
               width=5.5*inch,
               height=3.5*inch
         )
      )

      story.append(
         Paragraph(
               "Figure 2. Flightline Anomaly Map",
               styles["Italic"]
         )
      )

   story.append(
      Spacer(1,20)
   )

   # ==================================================
   # SURVEY QUALITY
   # ==================================================

   story.append(
      Paragraph(
         "3. Survey Quality Assessment",
         styles["Heading1"]
      )
   )

   ranking = quality_df.sort_values(
      "SQI",
      ascending=False
   )

   table_data = [
      ["Line","SQI","Class"]
   ]

   for _, row in ranking.iterrows():

      table_data.append([
         str(row["LINE"]),
         str(round(row["SQI"],2)),
         row["Quality_Class"]
      ])

   table = Table(
      table_data,
      colWidths=[80,80,120]
   )

   table.setStyle(
      TableStyle([
         ('BACKGROUND',(0,0),(-1,0),colors.darkblue),
         ('TEXTCOLOR',(0,0),(-1,0),colors.white),
         ('GRID',(0,0),(-1,-1),1,colors.black),
         ('ALIGN',(0,0),(-1,-1),'CENTER')
      ])
   )

   story.append(table)

   story.append(
      Spacer(1,20)
   )

   # ==================================================
   # ROOT CAUSE
   # ==================================================

   story.append(
      Paragraph(
         "4. Root Cause Analysis",
         styles["Heading1"]
      )
   )

   dominant = (
      root_df["Root_Cause"]
      .value_counts()
      .idxmax()
   )

   story.append(
      Paragraph(
         f"""
         Root cause analysis identified
         <b>{dominant}</b>
         as the dominant operational factor
         influencing airborne survey anomalies.
         """,
         styles["BodyText"]
      )
   )

   root_chart = f"{VIS_DIR}/root_cause_distribution.png"

   if os.path.exists(root_chart):

      story.append(
         Spacer(1,10)
      )

      story.append(
         Image(
               root_chart,
               width=5.5*inch,
               height=3.5*inch
         )
      )

   story.append(
      Spacer(1,20)
   )

   # ==================================================
   # TEMPORAL EVOLUTION
   # ==================================================

   story.append(
      Paragraph(
         "5. Temporal Evolution Analysis",
         styles["Heading1"]
      )
   )

   story.append(
      Paragraph(
         """
         Temporal evolution analysis evaluates
         how anomaly behaviour changes throughout
         the survey trajectory, helping distinguish
         isolated anomalies from clustered
         disturbances.
         """,
         styles["BodyText"]
      )
   )

   timeline = f"{VIS_DIR}/anomaly_timeline.png"

   if os.path.exists(timeline):

      story.append(
         Spacer(1,10)
      )

      story.append(
         Image(
               timeline,
               width=5.5*inch,
               height=3.5*inch
         )
      )

   story.append(
      Spacer(1,20)
   )

   # ==================================================
   # RESEARCH SUMMARY
   # ==================================================

   story.append(
      Paragraph(
         "6. Research Summary",
         styles["Heading1"]
      )
   )

   story.append(
      Paragraph(
         """
         The developed framework successfully integrates
         trajectory analysis, Isolation Forest anomaly
         detection, root cause identification, temporal
         evolution assessment and survey quality evaluation
         into a unified airborne survey monitoring system.

         The methodology provides a scalable and
         interpretable solution for identifying
         operational disturbances and assessing
         survey quality in airborne geophysical surveys.
         """,
         styles["BodyText"]
      )
   )

   doc.build(story)

   print(
      f"PDF Report Saved: {output_pdf}"
   )


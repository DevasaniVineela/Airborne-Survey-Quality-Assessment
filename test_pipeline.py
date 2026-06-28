from modules.preprocessing import preprocess_gps_data
from modules.survey_line_deviation import calculate_survey_line_deviation
from modules.anomaly_injection import inject_synthetic_anomalies
from modules.sliding_window import create_sliding_windows
from modules.train_model import train_isolation_forest
from modules.anomaly_analysis import analyze_anomalies
from modules.visualization import generate_visualizations
from modules.root_cause_analysis import classify_root_causes
from modules.survey_quality import calculate_survey_quality
from modules.line_health_ranking import rank_survey_lines
from modules.temporal_evolution import generate_anomaly_timeline

"""
# =====================================================
# STEP 1
# =====================================================

preprocess_gps_data(
    input_file="data/raw/gps_data.csv",
    output_file="data/processed/gps_processed.csv"
)

# =====================================================
# STEP 2
# =====================================================

calculate_survey_line_deviation(
    input_file="data/processed/gps_processed.csv",
    output_file="data/processed/gps_with_deviation.csv"
)

# =====================================================
# STEP 3
# ONLY FOR TRAINING DATA
# =====================================================

inject_synthetic_anomalies(
    input_file="data/processed/gps_with_deviation.csv",
    output_file="data/processed/gps_anomaly.csv"
)

# =====================================================
# STEP 4
# =====================================================

create_sliding_windows(
    input_file="data/processed/gps_anomaly.csv",
    output_file="data/processed/sliding_windows.csv"
)

# =====================================================
# STEP 5
# =====================================================

train_isolation_forest(
    input_file="data/processed/sliding_windows.csv",
    output_file="data/results/isolation_forest_results.csv",
    model_path="models/isolation_forest.pkl",
    scaler_path="models/scaler.pkl"
)
"""
generate_anomaly_timeline(
    isolation_file=
        "data/results/isolation_forest_results.csv",

    output_file=
        "data/results/anomaly_timeline.csv"
)
"""
# =====================================================
# STEP 6
# =====================================================

analyze_anomalies(
    input_file="data/results/isolation_forest_results.csv",
    output_file="data/results/anomaly_analysis_results.csv"
)


classify_root_causes(
    input_file="data/results/anomaly_analysis_results.csv",
    output_file="data/results/root_cause_results.csv"
)


quality_df = calculate_survey_quality(
    analysis_file=
        "data/results/anomaly_analysis_results.csv",

    windows_file=
        "data/processed/sliding_windows.csv",

    output_file=
        "data/results/survey_quality_results.csv"
)

ranking_df = rank_survey_lines(

    survey_quality_file=
        "data/results/survey_quality_results.csv",

    output_file=
        "data/results/line_health_ranking.csv"
)
"""
# =====================================================
# STEP 7
# =====================================================

generate_visualizations(
    gps_file="data/processed/gps_processed.csv",
    windows_file="data/processed/sliding_windows.csv",
    iso_file="data/results/isolation_forest_results.csv",
    analysis_file="data/results/anomaly_analysis_results.csv",
    root_cause_file="data/results/root_cause_results.csv",
    survey_quality_file="data/results/survey_quality_results.csv",
    timeline_file="data/results/anomaly_timeline.csv",
    output_folder="data/results/visualizations"
)
print("\nPIPELINE COMPLETED SUCCESSFULLY")
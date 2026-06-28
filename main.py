"""
if ENABLE_SYNTHETIC_ANOMALIES:
    inject_synthetic_anomalies(
        input_file=processed_file,
        output_file=anomaly_file
    )

    pipeline_input = anomaly_file

else:
    pipeline_input = processed_file
    
"""
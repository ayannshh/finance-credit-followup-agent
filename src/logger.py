import os
from datetime import datetime
import pandas as pd


def log_email(
    invoice_no,
    client_name,
    days_overdue,
    stage,
    tone,
    status,
):
    """
    Save one processing record to logs/audit_log.csv
    """

    log_file = "logs/audit_log.csv"

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "invoice_no": invoice_no,
        "client_name": client_name,
        "days_overdue": days_overdue,
        "stage": stage,
        "tone": tone,
        "status": status,
    }

    new_df = pd.DataFrame([record])

    # If log file already exists and is not empty, append to it
    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        existing_df = pd.read_csv(log_file)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    combined_df.to_csv(log_file, index=False)
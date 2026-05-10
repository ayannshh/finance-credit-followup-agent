import os
import streamlit as st
import pandas as pd

from src.stage_selector import get_follow_up_stage
from src.prompt_builder import build_email_prompt
from src.llm_generator import generate_email
from src.logger import log_email
from src.email_sender import send_email

# Page configuration
st.set_page_config(
    page_title="Finance Credit Follow-Up Email Agent",
    layout="wide"
)

# Header
st.title("Finance Credit Follow-Up Email Agent")
st.write("Upload a CSV file and automatically generate follow-up emails.")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Invoice CSV File",
    type=["csv"]
)

# Optional email sending
send_emails = st.checkbox("Send emails to clients")

# Show sample CSV format
with st.expander("Expected CSV Format"):
    sample_df = pd.DataFrame({
        "invoice_no": ["INV001"],
        "client_name": ["Aayansh Tarafdar"],
        "amount": [45000],
        "due_date": ["2026-04-20"],
        "email": ["aayansh@example.com"],
        "follow_up_count": [0],
    })
    st.dataframe(sample_df, use_container_width=True)

# Main application
if uploaded_file is not None:
    # Read uploaded CSV
    df = pd.read_csv(uploaded_file)

    # Preview uploaded data
    st.subheader("Uploaded Data Preview")
    st.dataframe(df, use_container_width=True)

    # Process button
    if st.button("Process Invoices"):
        emails_generated = 0
        escalated = 0
        emails_sent = 0

        # Clear previous audit log
        os.makedirs("logs", exist_ok=True)
        open("logs/audit_log.csv", "w").close()

        # Process each invoice
        for _, row in df.iterrows():
            days_overdue, stage, tone = get_follow_up_stage(
                row["due_date"]
            )

            # Not due yet
            if stage == "Not Due":
                log_email(
                    row["invoice_no"],
                    row["client_name"],
                    days_overdue,
                    stage,
                    tone,
                    "NO_ACTION",
                )
                continue

            # Manual review / escalation
            if stage == "Escalation":
                escalated += 1

                log_email(
                    row["invoice_no"],
                    row["client_name"],
                    days_overdue,
                    stage,
                    tone,
                    "ESCALATED",
                )

                st.warning(
                    f"{row['invoice_no']} - "
                    f"{row['client_name']} flagged for manual review."
                )
                continue

            # Build prompt
            prompt = build_email_prompt(
                client_name=row["client_name"],
                invoice_no=row["invoice_no"],
                amount=row["amount"],
                due_date=row["due_date"],
                days_overdue=days_overdue,
                tone=tone,
            )

            # Generate email
            email_text = generate_email(prompt)
            emails_generated += 1

            # Optionally send the email
            if send_emails:
                try:
                    send_email(row["email"], email_text)
                    emails_sent += 1

                    st.success(
                        f"Email sent to "
                        f"{row['client_name']} ({row['email']})"
                    )
                except Exception as e:
                    st.error(
                        f"Failed to send email to "
                        f"{row['email']}: {e}"
                    )

            # Save to audit log
            log_email(
                row["invoice_no"],
                row["client_name"],
                days_overdue,
                stage,
                tone,
                "EMAIL_GENERATED",
            )

            # Display generated email
            with st.expander(
                f"{row['invoice_no']} - "
                f"{row['client_name']} ({stage})",
                expanded=False
            ):
                st.text(email_text)

        # Summary metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Emails Generated", emails_generated)
        col2.metric("Escalated", escalated)
        col3.metric("Emails Sent", emails_sent)

        st.success("Processing completed successfully.")

        # Load audit log
        log_df = pd.read_csv("logs/audit_log.csv")

        # Show audit log
        st.subheader("Audit Log")
        st.dataframe(log_df, use_container_width=True)

        # Download audit log
        with open("logs/audit_log.csv", "rb") as f:
            st.download_button(
                label="Download Audit Log",
                data=f,
                file_name="audit_log.csv",
                mime="text/csv",
            )

else:
    st.info("Please upload a CSV file to begin.")
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
else:
    model = None


def extract_value(prompt, field_name):
    for line in prompt.splitlines():
        if line.startswith(f"{field_name}:"):
            return line.split(":", 1)[1].strip()
    return ""


def build_fallback_email(prompt):
    """
    Generate professional stage-specific payment follow-up emails.
    """
    client_name = extract_value(prompt, "Client Name")
    invoice_no = extract_value(prompt, "Invoice Number")
    amount = extract_value(prompt, "Amount Due")
    due_date = extract_value(prompt, "Due Date")
    days_overdue = extract_value(prompt, "Days Overdue")

    # Extract tone from prompt
    tone = ""
    for line in prompt.splitlines():
        if line.startswith("- Use a "):
            tone = line.replace("- Use a ", "").replace(" tone.", "").strip()
            break

    # Stage 1 — Warm & Friendly
    if tone == "Warm & Friendly":
        return f"""
Subject: Quick Reminder – Invoice {invoice_no} | {amount} Due

Hi {client_name},

I hope you're doing well.

This is a friendly reminder that Invoice {invoice_no} for {amount} was due on {due_date} and is currently {days_overdue} days overdue.

If you have already processed the payment, please disregard this message. Otherwise, we would appreciate it if you could arrange payment at your earliest convenience.

Thank you for your continued partnership.

Best regards,
Accounts Receivable Team
"""

    # Stage 2 — Polite but Firm
    if tone == "Polite but Firm":
        return f"""
Subject: Payment Reminder – Invoice {invoice_no} ({days_overdue} Days Overdue)

Dear {client_name},

This is a reminder that Invoice {invoice_no} for {amount}, due on {due_date}, remains unpaid and is now {days_overdue} days overdue.

We kindly request that you process the payment as soon as possible. If payment has already been initiated, please share the expected settlement date for our records.

Thank you for your prompt attention to this matter.

Best regards,
Accounts Receivable Team
"""

    # Stage 3 — Formal & Serious
    if tone == "Formal & Serious":
        return f"""
Subject: IMPORTANT: Outstanding Payment – Invoice {invoice_no} ({days_overdue} Days Overdue)

Dear {client_name},

Despite our previous reminders, Invoice {invoice_no} for {amount}, due on {due_date}, remains unpaid and is now {days_overdue} days overdue.

We request your immediate attention to this matter. Continued non-payment may affect your credit terms and future business arrangements.

Please arrange payment promptly and respond within 48 hours with either confirmation of payment or the expected payment date.

If there are any discrepancies or concerns regarding this invoice, please inform us immediately.

Sincerely,
Accounts Receivable Team
Finance Department
"""

    # Stage 4 — Stern & Urgent
    return f"""
Subject: FINAL NOTICE – Invoice {invoice_no} – Immediate Action Required

Dear {client_name},

This is our final reminder regarding Invoice {invoice_no} for {amount}, originally due on {due_date}. The invoice is now {days_overdue} days overdue.

Failure to remit payment within 24 hours may result in escalation to our legal and recovery team and may impact your account standing.

Please arrange immediate payment and provide confirmation today.

Regards,
Accounts Receivable Team
Finance Department
"""


def generate_email(prompt):
    """
    Use Gemini if available. If Gemini fails or quota is exhausted,
    use the professional fallback templates.
    """
    if model is not None:
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            pass

    return build_fallback_email(prompt)
def build_email_prompt(
    client_name,
    invoice_no,
    amount,
    due_date,
    days_overdue,
    tone,
):
    """
    Build a prompt for the LLM to generate a payment follow-up email.
    """

    prompt = f"""
You are a finance collections assistant.

Generate a professional payment follow-up email.

Requirements:
- Use a {tone} tone.
- Include the client name.
- Include the invoice number.
- Include the amount due.
- Include the due date.
- Mention that the invoice is {days_overdue} days overdue.
- Include a clear call to action requesting payment.
- Return:
  1. Subject
  2. Email Body

Invoice Details:
Client Name: {client_name}
Invoice Number: {invoice_no}
Amount Due: ₹{amount}
Due Date: {due_date}
Days Overdue: {days_overdue}
"""

    return prompt
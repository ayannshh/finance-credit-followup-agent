from datetime import datetime


def get_follow_up_stage(due_date_str):
    """
    Calculate overdue days and determine follow-up stage.
    Returns:
        days_overdue (int)
        stage (str)
        tone (str)
    """

    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    today = datetime.today().date()

    days_overdue = (today - due_date).days

    # If invoice is not overdue yet
    if days_overdue <= 0:
        return days_overdue, "Not Due", "No Action"

    # Stage 1
    if 1 <= days_overdue <= 7:
        return days_overdue, "Stage 1", "Warm & Friendly"

    # Stage 2
    if 8 <= days_overdue <= 14:
        return days_overdue, "Stage 2", "Polite but Firm"

    # Stage 3
    if 15 <= days_overdue <= 21:
        return days_overdue, "Stage 3", "Formal & Serious"

    # Stage 4
    if 22 <= days_overdue <= 30:
        return days_overdue, "Stage 4", "Stern & Urgent"

    # Escalation
    return days_overdue, "Escalation", "Manual Review Required"
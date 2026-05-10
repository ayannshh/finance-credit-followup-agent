[Open the App](https://finance-credit-followup-agent-43hbvjg6xunwjxp9bxwjze.streamlit.app/)

# Finance Credit Follow-Up Email Agent

An AI-powered agent that helps finance teams automatically generate follow-up emails for overdue invoices. The system reads invoice data from a CSV file, determines the appropriate follow-up stage based on the number of overdue days, generates personalized emails using Gemini (with a fallback template when API quota is unavailable), and records all actions in an audit log.

---

## Features

- Reads pending invoice records from CSV.
- Calculates days overdue.
- Selects follow-up stage and tone automatically.
- Generates personalized payment reminder emails.
- Escalates invoices overdue by more than 30 days.
- Maintains a complete audit trail.
- Streamlit web dashboard.
- Downloadable audit log.

---

## Follow-Up Stages

| Days Overdue | Stage | Tone |
|------------:|------|------|
| 1–7 | Stage 1 | Warm & Friendly |
| 8–14 | Stage 2 | Polite but Firm |
| 15–21 | Stage 3 | Formal & Serious |
| 22–30 | Stage 4 | Stern & Urgent |
| 30+ | Escalation | Manual Review Required |

---

## Tech Stack & Decision Log

### LLM Chosen
- Model: Gemini 2.0 Flash
- Provider: Google
- Rationale:
  - Fast response times
  - Free API access for development
  - Good text-generation quality

### Agent Framework
- Custom Python orchestration
- LangChain installed for extensibility

### Prompt Design
- Structured prompts with:
  - Client name
  - Invoice number
  - Amount due
  - Due date
  - Days overdue
  - Tone instructions

### UI
- Streamlit

### Data Processing
- Pandas

### Logging
- CSV audit log

---

## Security Mitigations

### Prompt Injection
- Prompts use controlled internal data only.

### Data Privacy
- API keys stored in `.env`.
- `.env` excluded via `.gitignore`.

### API Key Exposure
- No hardcoded credentials.
- `.env.example` provided.

### Hallucination Risk
- Structured prompts.
- Deterministic fallback template.

### Unauthorized Access
- Runs locally during development.

---

## Project Structure

```text
Project/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   └── invoices.csv
├── logs/
│   └── audit_log.csv
└── src/
    ├── data_loader.py
    ├── stage_selector.py
    ├── prompt_builder.py
    ├── llm_generator.py
    └── logger.py

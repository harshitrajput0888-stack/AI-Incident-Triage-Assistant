# AI Incident Triage Assistant

An AI-powered incident management application built with Python to analyze IT incidents, assign severity and priority, generate AI-based analysis, and maintain incident records.

## Features

* Create and record IT incidents
* Rule-based incident categorization
* Automatic severity classification
* Priority assignment from P1 to P4
* AI-generated incident analysis using Hugging Face
* Incident history management
* Search incidents by title or affected service
* Update incident status
* Incident statistics
* Application logging
* Automated testing with pytest

## Technology Stack

* Python 3.12
* Hugging Face Hub
* Hugging Face Inference API
* python-dotenv
* pytest
* JSON for incident data storage

## Project Structure

```text
AI-Incident-Triage-Assistant/
│
├── app/
│   ├── main.py
│   ├── incident.py
│   ├── triage.py
│   ├── ai_engine.py
│   ├── history.py
│   ├── config.py
│   └── logging_config.py
│
├── data/
│   └── incidents.json
│
├── logs/
│   └── app.log
│
├── tests/
│   ├── conftest.py
│   ├── test_triage.py
│   └── test_history.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

1. The user creates a new incident.
2. Incident details such as title, description, affected service, users, and environment are collected.
3. The rule-based triage engine analyzes the incident.
4. The system assigns a category, severity, and priority.
5. The incident is sent to the Hugging Face inference service for AI analysis.
6. The AI-generated analysis is displayed to the user.
7. The incident is saved to the JSON-based incident history.
8. Users can search incidents, update their status, and view statistics.
9. Application activities are recorded in the log file.

## Priority Levels

| Priority | Severity | Example                       |
| -------- | -------- | ----------------------------- |
| P1       | Critical | Production database outage    |
| P2       | High     | Major payment service failure |
| P3       | Medium   | Limited service disruption    |
| P4       | Low      | Minor application issue       |

## Testing

The project uses pytest for automated testing.

Current test coverage includes:

* Critical incident triage
* High severity incident triage
* Medium severity incident triage
* Low severity incident triage
* Incident save and load functionality

Run the tests using:

```bash
pytest
```

Expected result:

```text
5 passed
```

## Configuration

Create a `.env` file in the project root and add your Hugging Face token:

```text
HF_TOKEN=your_hugging_face_token
```

Never commit the `.env` file or API tokens to GitHub.

## Running the Application

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m app.main
```

## Future Improvements

* Web-based dashboard
* Database integration using MySQL or PostgreSQL
* Email or notification alerts for critical incidents
* Role-based access control
* Advanced incident analytics
* More comprehensive automated test coverage
* Integration with real IT service management platforms

## Project Objective

The objective of this project is to reduce manual effort in IT incident triage by combining rule-based classification with AI-assisted analysis, while maintaining incident history and operational visibility.

from app.triage import triage_incident


def test_critical_production_incident():

    incident = {
        "title": "Production Database Down",
        "description": "Production database is unavailable",
        "affected_service": "Database",
        "affected_users": 1500,
        "environment": "Production"
    }

    result = triage_incident(incident)

    assert result["category"] == "Database"
    assert result["severity"] == "Critical"
    assert result["priority"] == "P1"


def test_high_severity_incident():

    incident = {
        "title": "Payment Service Issue",
        "description": "Payment service is failing",
        "affected_service": "Payment API",
        "affected_users": 500,
        "environment": "Production"
    }

    result = triage_incident(incident)

    assert result["category"] == "Payment"
    assert result["severity"] == "High"
    assert result["priority"] == "P2"


def test_medium_severity_incident():

    incident = {
        "title": "Network Connectivity Issue",
        "description": "Users are experiencing network connectivity problems",
        "affected_service": "Network",
        "affected_users": 150,
        "environment": "Production"
    }

    result = triage_incident(incident)

    assert result["category"] == "Network"
    assert result["severity"] == "Medium"
    assert result["priority"] == "P3"


def test_low_severity_incident():

    incident = {
        "title": "Application Login Issue",
        "description": "A small number of users cannot login",
        "affected_service": "Authentication",
        "affected_users": 20,
        "environment": "Development"
    }

    result = triage_incident(incident)

    assert result["category"] == "Authentication"
    assert result["severity"] == "Low"
    assert result["priority"] == "P4"
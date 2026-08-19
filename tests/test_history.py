from app.history import save_incident, load_incidents


def test_save_and_load_incident(tmp_path, monkeypatch):

    test_file = tmp_path / "test_incidents.json"

    monkeypatch.setattr(
        "app.history.FILE_PATH",
        str(test_file)
    )

    incident = {
        "title": "Test Incident",
        "description": "Testing incident storage",
        "affected_service": "Test Service",
        "affected_users": 10,
        "environment": "Development",
        "category": "Application",
        "severity": "Low",
        "priority": "P4",
        "status": "OPEN",
        "ai_analysis": "Test AI analysis"
    }

    save_incident(incident)

    incidents = load_incidents()

    assert len(incidents) == 1

    saved_incident = incidents[0]

    assert saved_incident["title"] == "Test Incident"
    assert saved_incident["affected_service"] == "Test Service"
    assert saved_incident["priority"] == "P4"
    assert saved_incident["status"] == "OPEN"
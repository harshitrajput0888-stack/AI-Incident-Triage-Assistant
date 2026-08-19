import json
import os


FILE_PATH = "data/incidents.json"


def load_incidents():
    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_incident(incident):
    incidents = load_incidents()

    incidents.append(incident)

    os.makedirs("data", exist_ok=True)

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(incidents, file, indent=4)

    print("\nIncident saved successfully.")


def show_history():
    incidents = load_incidents()

    if not incidents:
        print("\nNo incidents found.")
        return

    print("\n" + "=" * 60)
    print("INCIDENT HISTORY")
    print("=" * 60)

    for index, incident in enumerate(incidents, start=1):

        print(f"\nIncident #{index}")
        print("-" * 40)

        print(f"Title       : {incident.get('title', 'N/A')}")
        print(f"Service     : {incident.get('affected_service', 'N/A')}")
        print(f"Users       : {incident.get('affected_users', 'N/A')}")
        print(f"Environment : {incident.get('environment', 'N/A')}")
        print(f"Category    : {incident.get('category', 'N/A')}")
        print(f"Severity    : {incident.get('severity', 'N/A')}")
        print(f"Priority    : {incident.get('priority', 'N/A')}")
        print(f"Status      : {incident.get('status', 'OPEN')}")


def search_incident(keyword):
    incidents = load_incidents()

    if not incidents:
        print("\nNo incidents found.")
        return

    keyword = keyword.lower().strip()

    results = []

    for incident in incidents:

        title = str(
            incident.get("title", "")
        ).lower()

        service = str(
            incident.get("affected_service", "")
        ).lower()

        if keyword in title or keyword in service:
            results.append(incident)

    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)

    if not results:
        print("\nNo matching incidents found.")
        return

    for index, incident in enumerate(results, start=1):

        print(f"\nResult #{index}")
        print("-" * 40)

        print(f"Title    : {incident.get('title', 'N/A')}")
        print(f"Service  : {incident.get('affected_service', 'N/A')}")
        print(f"Severity : {incident.get('severity', 'N/A')}")
        print(f"Priority : {incident.get('priority', 'N/A')}")
        print(f"Status   : {incident.get('status', 'OPEN')}")


def update_incident_status(incident_number, new_status):

    incidents = load_incidents()

    if not incidents:
        print("\nNo incidents found.")
        return

    if incident_number < 1 or incident_number > len(incidents):
        print("\nInvalid incident number.")
        return

    allowed_statuses = [
        "OPEN",
        "INVESTIGATING",
        "RESOLVED",
        "CLOSED"
    ]

    new_status = new_status.upper().strip()

    if new_status not in allowed_statuses:

        print("\nInvalid status.")
        print(
            "Allowed statuses:",
            ", ".join(allowed_statuses)
        )
        return

    incidents[incident_number - 1]["status"] = new_status

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(incidents, file, indent=4)

    print("\nIncident status updated successfully.")


def show_statistics():

    incidents = load_incidents()

    if not incidents:
        print("\nNo incidents available.")
        return

    total = len(incidents)

    critical = 0
    high = 0
    medium = 0
    low = 0

    open_count = 0
    investigating = 0
    resolved = 0
    closed = 0

    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0

    for incident in incidents:

        severity = incident.get(
            "severity", ""
        ).upper()

        priority = incident.get(
            "priority", ""
        ).upper()

        status = incident.get(
            "status", "OPEN"
        ).upper()

        if severity == "CRITICAL":
            critical += 1
        elif severity == "HIGH":
            high += 1
        elif severity == "MEDIUM":
            medium += 1
        elif severity == "LOW":
            low += 1

        if priority == "P1":
            p1 += 1
        elif priority == "P2":
            p2 += 1
        elif priority == "P3":
            p3 += 1
        elif priority == "P4":
            p4 += 1

        if status == "OPEN":
            open_count += 1
        elif status == "INVESTIGATING":
            investigating += 1
        elif status == "RESOLVED":
            resolved += 1
        elif status == "CLOSED":
            closed += 1

    print("\n" + "=" * 50)
    print("INCIDENT STATISTICS")
    print("=" * 50)

    print(f"\nTotal Incidents : {total}")

    print("\nSeverity:")
    print(f"Critical : {critical}")
    print(f"High     : {high}")
    print(f"Medium   : {medium}")
    print(f"Low      : {low}")

    print("\nPriority:")
    print(f"P1 : {p1}")
    print(f"P2 : {p2}")
    print(f"P3 : {p3}")
    print(f"P4 : {p4}")

    print("\nStatus:")
    print(f"Open          : {open_count}")
    print(f"Investigating : {investigating}")
    print(f"Resolved      : {resolved}")
    print(f"Closed        : {closed}")
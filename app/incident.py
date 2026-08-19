from app.triage import triage_incident
from app.ai_engine import AIIncidentAnalyzer
from app.history import save_incident
from app.logging_config import setup_logger


logger = setup_logger()


def create_incident():

    print("\n" + "=" * 50)
    print("CREATE NEW INCIDENT")
    print("=" * 50)

    # Incident title
    while True:

        title = input("\nIncident Title: ").strip()

        if title:
            break

        print("Incident title cannot be empty.")

    # Incident description
    while True:

        description = input(
            "Incident Description: "
        ).strip()

        if description:
            break

        print("Incident description cannot be empty.")

    # Affected service
    while True:

        affected_service = input(
            "Affected Service: "
        ).strip()

        if affected_service:
            break

        print("Affected service cannot be empty.")

    # Affected users
    while True:

        try:

            affected_users = int(
                input("Affected Users: ")
            )

            if affected_users < 0:
                print(
                    "Affected users cannot be negative."
                )
                continue

            break

        except ValueError:

            print(
                "Please enter a valid number."
            )

    # Environment
    valid_environments = [
        "production",
        "staging",
        "development"
    ]

    while True:

        environment = input(
            "Environment "
            "(Production/Staging/Development): "
        ).strip().lower()

        if environment in valid_environments:

            environment = environment.capitalize()
            break

        print(
            "Invalid environment. "
            "Use Production, Staging or Development."
        )

    # Create incident object
    incident = {

        "title": title,

        "description": description,

        "affected_service": affected_service,

        "affected_users": affected_users,

        "environment": environment
    }

    # Python-based triage
    print("\nAnalyzing incident...")

    try:

        triage_result = triage_incident(
            incident
        )

        incident["category"] = (
            triage_result["category"]
        )

        incident["severity"] = (
            triage_result["severity"]
        )

        incident["priority"] = (
            triage_result["priority"]
        )

        logger.info(
            f"Triage completed: {title} | "
            f"Priority: {incident['priority']} | "
            f"Severity: {incident['severity']}"
        )

    except Exception as error:

        logger.error(
            f"Triage failed for incident '{title}': "
            f"{error}"
        )

        print(
            f"\nTriage failed: {error}"
        )

        return

    # Display triage result
    print("\n" + "=" * 50)
    print("TRIAGE RESULT")
    print("=" * 50)

    print(
        f"Category : {incident['category']}"
    )

    print(
        f"Severity : {incident['severity']}"
    )

    print(
        f"Priority : {incident['priority']}"
    )

    # AI analysis
    print("\nGenerating AI analysis...")

    try:

        analyzer = AIIncidentAnalyzer()

        ai_analysis = analyzer.analyze(
            incident,
            triage_result
        )

        incident["ai_analysis"] = (
            ai_analysis
        )

        logger.info(
            f"AI analysis completed: {title}"
        )

        print("\n" + "=" * 50)
        print("AI ANALYSIS")
        print("=" * 50)

        print(ai_analysis)

    except Exception as error:

        incident["ai_analysis"] = (
            f"AI analysis failed: {error}"
        )

        logger.error(
            f"AI analysis failed for incident "
            f"'{title}': {error}"
        )

        print(
            f"\nAI analysis failed: {error}"
        )

    # Initial status
    incident["status"] = "OPEN"

    # Save incident
    try:

        save_incident(incident)

        logger.info(
            f"Incident saved successfully: {title}"
        )

    except Exception as error:

        logger.error(
            f"Failed to save incident "
            f"'{title}': {error}"
        )

        print(
            f"\nFailed to save incident: {error}"
        )

        return
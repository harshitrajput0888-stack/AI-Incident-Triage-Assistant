def triage_incident(incident):

    title = incident["title"].lower()
    description = incident["description"].lower()
    service = incident["affected_service"].lower()

    text = f"{title} {description} {service}"

    # Incident category
    if any(word in text for word in [
        "database",
        "sql",
        "mysql",
        "postgresql",
        "oracle",
        "db"
    ]):
        category = "Database"

    elif any(word in text for word in [
        "payment",
        "transaction",
        "billing",
        "invoice"
    ]):
        category = "Payment"

    elif any(word in text for word in [
        "network",
        "internet",
        "connection",
        "dns",
        "router"
    ]):
        category = "Network"

    elif any(word in text for word in [
        "login",
        "authentication",
        "password",
        "access",
        "account"
    ]):
        category = "Authentication"

    elif any(word in text for word in [
        "server",
        "cpu",
        "memory",
        "disk",
        "storage"
    ]):
        category = "Infrastructure"

    else:
        category = "Application"

    # Severity and priority
    affected_users = incident["affected_users"]
    environment = incident["environment"].lower()

    if environment == "production" and affected_users >= 1000:

        severity = "Critical"
        priority = "P1"

    elif affected_users >= 500:

        severity = "High"
        priority = "P2"

    elif affected_users >= 100:

        severity = "Medium"
        priority = "P3"

    else:

        severity = "Low"
        priority = "P4"

    return {
        "category": category,
        "severity": severity,
        "priority": priority
    }
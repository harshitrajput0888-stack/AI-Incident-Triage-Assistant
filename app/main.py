from app.incident import create_incident
from app.history import (
    show_history,
    search_incident,
    update_incident_status,
    show_statistics
)


def main():

    while True:

        print("\n" + "=" * 50)
        print("      AI INCIDENT TRIAGE ASSISTANT")
        print("=" * 50)

        print("\n1. Create New Incident")
        print("2. View Incident History")
        print("3. Search Incident")
        print("4. Update Incident Status")
        print("5. Incident Statistics")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            create_incident()

        elif choice == "2":

            show_history()

        elif choice == "3":

            keyword = input(
                "\nEnter incident title or service to search: "
            )

            search_incident(keyword)

        elif choice == "4":

            try:

                incident_number = int(
                    input("\nEnter incident number: ")
                )

                new_status = input(
                    "\nEnter new status "
                    "(OPEN/INVESTIGATING/RESOLVED/CLOSED): "
                )

                update_incident_status(
                    incident_number,
                    new_status
                )

            except ValueError:

                print(
                    "\nPlease enter a valid incident number."
                )

        elif choice == "5":

            show_statistics()

        elif choice == "6":

            print("\nApplication closed.")
            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1, 2, 3, 4, 5 or 6."
            )


if __name__ == "__main__":
    main()
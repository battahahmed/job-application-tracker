from database import *

create_table()

while True:
    print("""
    ===== JOB APPLICATION TRACKER =====
1. Add an application
2. View all applications
3. Update application status
4. Delete an application
5. Exit
""")
    choice = input("Enter your choice (1-5): ")
    if choice == '2':
        applications = view_application()
        if not applications:
            print("No applications found.")
        else:
        
            for application in applications:
                id, company, position, app_date, status = application    
                print(f"""
                ID: {id}
                Company: {company}
                Position: {position}
                Application date: {app_date}
                Status: {status}
                ---------------------------------------------
    """)

    elif choice == '1':
        company = input("Company name: ").strip().upper()
        position = input("Job position: ").strip().upper()
        app_date = input("Application date: ")
        status = input("Application status: ").strip().upper()
        
        add_application(company, position, app_date, status)

    elif choice == '3':
        try:
            id = int(input("ID: "))
        except(ValueError):
            print('Enter a valid numeric ID')
            continue

        valid_statuses = ["Applied", "Interview", "Rejected", "Offer"]

        while True:   
            new_status = input("New status: ").title()
            if new_status not in valid_statuses:
                print("Invalid choice! Please Enter Applied, Interview, Rejected or Offer.")
                continue

            update_application(id, new_status)
            break

    elif choice == '4':
        try:
            app_id = int(input("ID: "))
        except(ValueError):
            print('Enter a valid numeric ID')
            continue

        delete_application(app_id)

    elif choice == '5':
        print('Goodbye! Thanks for using Job Application Tracker.')
        break
    else:
        print('Invalid choice. Please enter a number between 1 and 5.')




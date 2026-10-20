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
        for application in applications:
            print(application)

    elif choice == '1':
        company = input("Company name: ")
        position = input("Job position: ")
        app_date = input("Application date: ")
        status = input("Application status: ")
        
        add_application(company, position, app_date, status)

    elif choice == '3':
        try:
            id = int(input("ID: "))
        except(ValueError):
            print('Enter a valid numeric ID')
            continue
            
        new_status = input("New status: ")

        update_application(id, new_status)

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
    





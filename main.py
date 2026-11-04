from datetime import datetime
from database import *

create_table()
#check_application_dates()

while True:
    print("""
    ===== JOB APPLICATION TRACKER =====
1. Add an application
2. View all applications
3. Update application status
4. Delete an application
5. Search applications by company
6. Update application date
7. Exit
""")
    choice = input("Enter your choice (1-7): ")
    if choice == '1':
        while True:
            company = input("Company name: ").strip().upper()
            if not company:
                print("Company name can't be empty! Please enter a name.")
            else:
                break

        while True:
            position = input("Job position: ").strip().upper()
            if not position:
                print("Position job can't be empty! Please enter a position.")
            else:
                break

        while True:
            app_date = input("Application date (DD/MM/YYYY): ").strip()
            try:
                date_object = datetime.strptime(app_date, "%d/%m/%Y")
                app_date = date_object.strftime("%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date. Please enter a valid date and use DD/MM/YYYY format.")

        valid_statuses = ["APPLIED", "INTERVIEW", "REJECTED", "OFFER"]
        while True:
            status = input("Application status: ").strip().upper()
            if not status:
                print("Status can't be empty! Please enter a status.")
            elif status not in valid_statuses:
                print("Invalid status. Please enter Applied, Interview, Rejected or Offer.")
            else:
                break
        
        add_application(company, position, app_date, status)


    elif choice == '2':
        while True:
            print("""
                1- Application date — newest first
                2- Application date — oldest first
                3- ID — ascending
                4- ID — descending
            """)
            valid_choices = ["1", "2", "3", "4"]
            menu = input("Enter your sorting applications choice(1-4): ")
            if menu not in valid_choices: 
                print("Invalid choice. Please enter a number from 1 to 4.")
            else:
                break
        applications = view_application(menu)
        if not applications:
            print("No applications found.")
        else:
        
            for application in applications:
                id, company, position, app_date, status = application
                display_date = datetime.strptime(app_date, "%Y-%m-%d").strftime("%d/%m/%Y")    
                print(f"""
                ID: {id}
                Company: {company}
                Position: {position}
                Application date: {display_date}
                Status: {status}
                ---------------------------------------------
    """)

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
        company = input("Enter company name to search: ").strip().upper()
        if not company:
            print('Company name cannot be empty!')
            continue 
        applications = search_application(company)
        if not applications:
            print("No applications found for that company!")
        else:
            for application in applications:
                id, company, position, app_date, status = application 
                display_date = datetime.strptime(app_date, "%Y-%m-%d").strftime("%d/%m/%Y")   
                print(f"""
                ID: {id}
                Company: {company}
                Position: {position}
                Application date: {display_date}
                Status: {status}
                ---------------------------------------------
    """)


    elif choice == '6':
        try:
            id = int(input("ID: "))
        except(ValueError):
            print('Enter a valid numeric ID')
            continue
        
        while True:
            new_date = input("New date DD/MM/YYYY: ").strip()
            if new_date:   
                try:
                    date_object = datetime.strptime(new_date, "%d/%m/%Y")
                    app_date = date_object.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date. Please enter a valid date and use DD/MM/YYYY format.")
            else:
                print("Date can't be empty!")
                new_date = input("New date DD/MM/YYYY: ").strip()


        update_application_date(id, app_date)
        


    elif choice == '7':
        print('Goodbye! Thanks for using Job Application Tracker.')
        break
    else:
        print('Invalid choice. Please enter a number between 1 and 7.')
        
    



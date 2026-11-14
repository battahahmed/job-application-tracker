import sqlite3
from datetime import datetime

def connect_db():
    connection = sqlite3.connect('jobs.db')
    
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def create_table():
    connection = connect_db()

    application_sql_statement = """
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY,
        company TEXT,
        position TEXT,
        application_date TEXT,
        status TEXT
    )
    """
    interview_sql_statement = """
        CREATE TABLE IF NOT EXISTS interviews (
        interview_id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id INTEGER NOT NULL, 
        interview_date TEXT NOT NULL,
        interview_type TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (application_id) REFERENCES applications(id)
    )
    """ 
    connection.execute(application_sql_statement) 
    connection.execute(interview_sql_statement)
    connection.commit()
    connection.close()



def add_application(company, position, application_date, status):
    connection = connect_db()


    sql_statement = """
        INSERT INTO applications
            (company, position, application_date, status)
        VALUES (?, ?, ?, ?)

"""

    cursor = connection.cursor()
    cursor.execute(
        sql_statement, 
        (company, position, application_date, status)
    )
    connection.commit()
    cursor.close()
    connection.close



def view_applications(user_choice):
    sort_options = {
        "1": "application_date DESC",
        "2": "application_date ASC",
        "3": "id ASC",
        "4": "id DESC"
    }

    order_by = sort_options.get(user_choice) 
    if order_by is not None:
        connection = connect_db()
        cursor = connection.cursor()
        sql_statement = f"""
            SELECT * 
            FROM applications 
            ORDER BY {order_by} 
    """
        cursor.execute(sql_statement)
        applications = cursor.fetchall()

        cursor.close()
        connection.close()
    else:
        print("Invalid choice")
        return

    return applications



def get_application_by_id(app_id):
    connection = connect_db()
    cursor = connection.cursor()

    sql_statement = """
        SELECT *
        FROM applications
        WHERE id = ?
    """

    cursor.execute(sql_statement, (app_id,))
    applications = cursor.fetchone()
    cursor.close()
    connection.close()
    return applications


 
def update_application(app_id):
    print("""
        1. Company name
        2. Job position
        3. Application status
        4. Application date
        5. Back to main menu
""") 
    update_options = {
        '1': 'company',
        '2': 'position',
        '3': 'status',
        '4': 'application_date'
    }

    column_indices = {
    'company': 1,
    'position': 2,
    'application_date': 3,
    'status': 4
}

    while True:
        application = get_application_by_id(app_id)

        if application is None:
            print("Application not found!")
            return
        
        print(f"""
            Application found!

            ID: {application[0]}
            Company name: {application[1]}
            Job position: {application[2]}
            Application date: {application[3]}
            Status: {application[4]}
        """)

        
        user_option = input("Enter your update option (1-5): ").strip()
        if user_option == '5':
            break
        elif user_option not in update_options:
            print("Enter a valid option")
        else:
            column_name = update_options[user_option]

            while True:
                new_value = input(f"Enter new value for {column_name}: ").strip()
                if not new_value:
                    print("Input cannot be empty!")
                elif column_name == 'status':
                    statuses = ['APPLIED', 'INTERVIEW', 'REJECTED', 'OFFER']
                    if new_value.upper() not in statuses:
                        print("Enter a valid status")
                    else:
                        new_value = new_value.upper()
                        break
                elif column_name == 'application_date':
                    try:
                        date_object = datetime.strptime(new_value, "%d/%m/%Y")
                        new_value = date_object.strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid date. Please enter a valid date and use DD/MM/YYYY format.")
                else:
                    break

        current_value = application[column_indices[column_name]]
        
        if column_name == 'status':
            current_value = current_value.upper()
            new_value = new_value.upper()

        if current_value == new_value:    
            print("No changes detected!")
            continue


        connection = connect_db()
        cursor = connection.cursor()
        
        try:
            print("Current value:", current_value)
            print("New value:", new_value)

            selected_option = ['yes', 'no']

            while True:
                confirmation = input("Are you sure (yes or no)?: ").strip().lower()
                if confirmation not in selected_option:
                    print("Please enter yes or no!")
            
                elif confirmation == selected_option[0]:
                    sql_statement = f"""
                        UPDATE applications
                        SET {column_name} = ?
                        WHERE id = ?
                    """
                    
                    cursor.execute(sql_statement, (new_value, app_id))

                    if cursor.rowcount == 1:
                        connection.commit()
                        print("Application updated successfully!")    
                    else:
                        connection.rollback()  
                        print("No matching application was updated!")
                    break
                
                elif confirmation == selected_option[1]:
                    print("Update cancelled!")
                    break

        except sqlite3.Error as error:
            connection.rollback()
            print(f"Database error: {error}")

        finally:

            cursor.close()
            connection.close()
        



def delete_application(application_id):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        application = get_application_by_id(application_id)

        if application is None:
            print("No application found with that ID.")
            return

        display_date = datetime.strptime(
            application[3], "%Y-%m-%d"
        ).strftime("%d/%m/%Y")

        print(f"""
        Application found!

        ID: {application[0]}
        Company name: {application[1]}
        Job position: {application[2]}
        Application date: {display_date}
        Status: {application[4]}
    """)
        selected_option = ['yes', 'no']

        while True:
            confirmation = input("Are you sure (yes or no)?: ").strip().lower()
            if confirmation not in selected_option:
                print("Please enter yes or no!")

            elif confirmation == selected_option[0]:
                sql_statement = """
                    DELETE FROM applications
                    WHERE id = ?
                """
                

                cursor.execute(sql_statement, (application_id,))

                if cursor.rowcount == 1:
                    connection.commit()
                    print("Application deleted successfully.")
                    
                else:
                    connection.rollback()
                    print("No application found with that ID.")
                break

            elif confirmation == selected_option[1]:
                print("Deletion cancelled")
                break

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:   
        cursor.close()
        connection.close()



def search_application(company_name):
    connection = connect_db()
    cursor = connection.cursor()

    sql_statement = ("""
        SELECT * 
        FROM applications 
        WHERE LOWER(company) LIKE LOWER(?)
    """)

    cursor.execute(sql_statement, (f"%{company_name}%",))
    applications = cursor.fetchall()
    print("DEBUG search results:", applications)
    cursor.close()
    connection.close()
    return applications



def filter_applications(status):
    connection = connect_db()
    cursor = connection.cursor()

    sql_statement = """
        SELECT * 
        FROM applications
        WHERE status = ? 
"""

    cursor.execute(sql_statement, (status,))
    applications = cursor.fetchall()
    cursor.close()
    connection.close()
    return applications



def check_application_dates():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT id, company, application_date FROM applications")
    applications = cursor.fetchall()

    for application in applications:
        print(application)

    cursor.close()
    connection.close()


def add_interview():
    applications = view_applications("1")
    if not applications:
        print("No applications found!")
        return
    for application in applications:
        print(f"""
            ID: {application[0]}
            Company: {application[1]}
            Job position: {application[2]}          
        """)

    while True:
        try:
            app_id = int(input("ID: ").strip())
        except ValueError:
            print("ID should be a number!")
            continue
        application_id = get_application_by_id(app_id)

        if application_id is None:
            print("Application not found!")
            continue
        
        print(f"""
            Application found!

            ID: {application_id[0]}
            Company name: {application_id[1]}
            Job position: {application_id[2]}
            Application date: {application_id[3]}
            Status: {application_id[4]}
        """)
        break

    while True:
        interview_date = input("Interview date (DD/MM/YYYY): ").strip()
        try:
            date_object = datetime.strptime(interview_date, "%d/%m/%Y")
            interview_date = date_object.strftime("%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Please enter a valid date and use DD/MM/YYYY format.")

    
    valid_types = ["TECHNICAL", "HR", "PHONE", "VIDEO", "IN-PERSON", "ONLINE"]
    while True:
        interview_type = input("Interview type: ").strip().upper()
        if not interview_type:
            print("Interview type can't be empty! Please enter an interview type.")
        elif interview_type not in valid_types:
            print("Invalid type!")
        else:
            break

    notes = input("Interview notes: ").strip()

    connection = connect_db()


    sql_statement = """
        INSERT INTO interviews
            (application_id, interview_date, interview_type, notes)
        VALUES (?, ?, ?, ?)

    """

    cursor = connection.cursor()
    cursor.execute(
        sql_statement, 
        (app_id, interview_date, interview_type, notes)
    )
    connection.commit()
    cursor.close()
    connection.close()


def view_interviews():
    connection = connect_db()
    cursor = connection.cursor()
    sql_statement = """
        SELECT
            interviews.interview_id,
            interviews.application_id,
            interviews.interview_date,
            interviews.interview_type,
            interviews.notes,
            applications.company,
            applications.position
        FROM interviews
        JOIN applications ON interviews.application_id = applications.id
"""

    cursor.execute(sql_statement)
    interview_records = cursor.fetchall()

    if not interview_records:
        print("No interviews found.")

    else:
        for interview in interview_records:
            interview_id, application_id, interview_date, interview_type, notes, company, position = interview
            display_date = datetime.strptime(interview_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            if not notes:
                notes = "No notes provided."  
            print(f"""
            Interview ID: {interview_id}
            Application ID: {application_id}
            Interview Date: {display_date}
            Interview Type: {interview_type}
            Notes: {notes}
            Company: {company}
            Position: {position}
            ---------------------------------------------
""")

    cursor.close()
    connection.close()


    return interview_records


def show_statistics():

    # 1. Initialize connection and cursor variables
    connection = None
    cursor = None

    try:
        # 2. Connect to database and create cursor
        connection = connect_db()
        cursor = connection.cursor()

        # 3. Execute all database queries
        # 4. Retrieve all required results

        # Get total applications
        sql_statement = """
        SELECT COUNT(*)
        FROM applications
    """

        cursor.execute(sql_statement)
        total_applications_count = cursor.fetchone()
        num = total_applications_count[0]


        # Get applications grouped by status
        sql_statement1 = """
            SELECT status, COUNT(*)
            FROM applications
            GROUP BY status;
        """

        cursor.execute(sql_statement1)
        total_applications_by_status = cursor.fetchall()


        # Get total interview records
        sql_statement2 = """
            SELECT COUNT(*)
            FROM interviews 
        """

        cursor.execute(sql_statement2)
        total_interviews_applications_count = cursor.fetchone()
        num2 = total_interviews_applications_count[0]


        # Get unique applications with interviews
        sql_statement3 = """
            SELECT COUNT(DISTINCT application_id)
            FROM interviews
        """

        cursor.execute(sql_statement3)
        applications_with_interviews = cursor.fetchone()
        num3 = applications_with_interviews[0]


        # Get total offers
        sql_statement4 = """
            SELECT COUNT(*)
            FROM applications 
            WHERE status = 'OFFER'
        """

        cursor.execute(sql_statement4)
        total_offers_count = cursor.fetchone()
        num4 = total_offers_count[0]

    except sqlite3.Error as error:
        # 5. Handle database errors
        print(f"Database error while retrieving statistics: {error}")
        # 6. Stop normal execution
        return

    finally:
        # 7. Close cursor and connection safely
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

    # 8. Handle zero applications using an if statement
    if num == 0:
        print("\nNo application records!")
        print("\nTotal applications: 0\n")
        print("Interview rate: 0%")
        print("Offer rate: 0%")

    # 9. Calculate statistics
    # 10. Display statistics
    else:
        # Calculate interview rate
        interview_rate = (num3 / num) * 100

        # Calculate offer rate
        offer_rate = (num4 / num) * 100

        print(f"\nTotal applications: {num}\n")
        print("Applications by status:")
        for status, count in total_applications_by_status:
            print(f"{status}: {count}")
        print(f"Interview rate: {interview_rate:.2f}%")
        print(f"Offer rate: {offer_rate:.2f}%")

    print(f"\nTotal interviews records: {num2}")
    print(f"Total offers: {num4}\n")


create_table()




"""
to test the search_application()
if __name__ == "__main__":
    results = search_application("microsoft")
    print(results)
"""

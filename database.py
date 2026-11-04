import sqlite3

def connect_db():
    connection = sqlite3.connect('jobs.db')
    return connection

def create_table():
    connection = connect_db()

    sql_statement = """
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY,
        company TEXT,
        position TEXT,
        application_date TEXT,
        status TEXT
    )
    """

    connection.execute(sql_statement)
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

def view_application(user_choice):
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

def delete_application(application_id):
    connection = connect_db()
    cursor = connection.cursor()
    sql_statement = """
        DELETE FROM applications
        WHERE id = ?
"""
    cursor.execute(sql_statement, (application_id,))

    if cursor.rowcount == 0:
        print("No application found with that ID.")
    else:
        print("Application deleted successfully.")

    connection.commit()
    cursor.close()
    connection.close()

def update_application(application_id, new_status):
    connection = connect_db()
    cursor = connection.cursor() 

    sql_statement = """
        UPDATE applications
        SET status = ?
        WHERE id = ?
"""
    cursor.execute(sql_statement, (new_status, application_id)) 
    if cursor.rowcount == 0:
        print('No matching application was updated.')
    else:
        print('Application status updated successfully!')
    connection.commit()
    cursor.close()
    connection.close()

def update_application_date(application_id, new_date):
    connection = connect_db()
    cursor = connection.cursor() 

    sql_statement = """
        UPDATE applications
        SET application_date = ?
        WHERE id = ?
"""
    cursor.execute(sql_statement, (new_date, application_id)) 
    if cursor.rowcount == 0:
        print('No matching application was updated.')
    else:
        print('Application date updated successfully!')
    connection.commit()
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


"""
to test the search_application()
if __name__ == "__main__":
    results = search_application("microsoft")
    print(results)
"""

def check_application_dates():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT id, company, application_date FROM applications")
    applications = cursor.fetchall()

    for application in applications:
        print(application)

    cursor.close()
    connection.close()

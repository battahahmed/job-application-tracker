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

def view_application():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM applications")
    applications = cursor.fetchall()

    cursor.close()
    connection.close()

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



def search_application(company_name):
    connection = connect_db()
    cursor = connection.cursor()

    sql_statement = ("""
        SELECT * 
        FROM applications 
        WHERE LOWER(company) = LOWER (?)
    """)
    cursor.execute(sql_statement, (company_name,))
    applications = cursor.fetchall()
    cursor.close()
    connection.close()
    return applications


"""
to test the search_application()
if __name__ == "__main__":
    results = search_application("microsoft")
    print(results)
"""

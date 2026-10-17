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
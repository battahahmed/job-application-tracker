from database import *

create_table()
'''
add_application(
    'Google',
    'Ceo',
    '2026/10/17',
    'Applied'
)
'''

applications = view_application()

for application in applications:
    print(application)
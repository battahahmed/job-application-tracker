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

delete_application(2)

update_application(3, 'Interview')

applications = view_application()

for application in applications:
    print(application)




from pyrogram import Client
import sqlite3


with sqlite3.connect('database.db') as connection:
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE if not exists "sessions" (
	"id"	INTEGER,
	"session_name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
)
''')


def add_account_to_db(session_name):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''select max(id)
    from sessions
    ''')
    cursor.execute(f'''insert into sessions
    (session_name)
    values(
        '{session_name}'
    )
    ''')
    connection.commit()
    connection.close()

print('''be panele modiriate account khosh omadid!
inja mitonin be tedade delkhah,robot besazid
--------------------------------------------------
''')

while(True):
    session_name = input('name session ra vared koind: ')
    try:
        with Client(session_name) as app:
            app.send_message("me", 'seesion ijad shod!')
        add_account_to_db(session_name)
    except:
        print('in session az ghabl mojod ast!')

    else:
        print('seesion ijad shod!')


    
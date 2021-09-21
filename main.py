from pyrogram import Client
import sqlite3








def get_session_list():
    session_list = list()
    connection = sqlite3.connect('database.db')

    cursor = connection.cursor()

    cursor.execute('''select session_name
    from sessions
    ''')

    session_tuples = cursor.fetchall()


    for tup in session_tuples:
        session_list.append(tup[0])

    return session_list




session_list = get_session_list()

#print(session_list)
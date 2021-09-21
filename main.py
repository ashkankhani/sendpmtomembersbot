from pyrogram import Client
import sqlite3
import re
from pyrogram.errors import BadRequest,FloodWait
#pyrogram.errors.exceptions.bad_request_400.UsernameInvalid: [400 USERNAME_INVALID]: The username is invalid (caused by "contacts.ResolveUsername
#pyrogram.errors.exceptions.bad_request_400.UserAlreadyParticipant: [400 USER_ALREADY_PARTICIPANT]: The user is already a participant of this chat (caused by "messages.ImportChatInvite"
#pyrogram.errors.exceptions.flood_420.FloodWait [420 FLOOD_WAIT_X]
LINK = 'project_gp_nahad'
TEXT = 'سلام'



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


# def get_group_members(session):
#     with Client(session) as app:
#         Client



def join_chat(session_list,link):
    res = re.findall(r'^.*t\.me/(\w*)$',link)
    if(len(res)):
        link = res[0]
    for session in session_list:
        with Client(session) as app:
            try:
                app.join_chat(link)
            except BadRequest as e:
                id = e.ID
                if(id == 'USERNAME_INVALID'):
                    print('link eshtebah ast!')
                elif(id == 'UserAlreadyParticipant'):
                    print(f'karbare {session} dar grouh az ghabl bood!')
            except FloodWait as e:
                sleep_time = e.x
                print(f'{session} bayad {sleep_time} sanie esterahat kone!')
            except:
                print('error')
            else:
                print(f'{session} be grouh add shod!')


session_list = get_session_list()
join_chat(session_list,LINK)
#group_members = get_group_members(session_list[0])




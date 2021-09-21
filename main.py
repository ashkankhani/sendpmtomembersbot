from pyrogram import Client
import sqlite3
import re
from pyrogram.errors import BadRequest,FloodWait
from time import sleep
#pyrogram.errors.exceptions.bad_request_400.UsernameInvalid: [400 USERNAME_INVALID]: The username is invalid (caused by "contacts.ResolveUsername
#pyrogram.errors.exceptions.bad_request_400.UserAlreadyParticipant: [400 USER_ALREADY_PARTICIPANT]: The user is already a participant of this chat (caused by "messages.ImportChatInvite"
#pyrogram.errors.exceptions.flood_420.FloodWait [420 FLOOD_WAIT_X]

LINK = 'https://t.me/joinchat/8cEvVi1qCzM2NDVk'
TEXT = 'سلام'
MAX_SEND_PER_SESSION = 2



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


def get_group_members(session,group_id):
    print(group_id)
    with open('usernames.txt' , 'w') as f:
        with Client(session) as app:
            members_logs = app.iter_chat_members(chat_id = group_id)
            for member in members_logs:
                if(not member.user.is_bot):
                    f.write(f'{member.user.id}\n')
                #member_list.append(member.user.id)

    #return member_list
        
        
    



def join_chat(session_list,link):
    
    res = re.findall(r'^.*t\.me/(\w*)$',link)

    if(len(res)):
        link = res[0]
    

    for session in session_list:
        with Client(session) as app:
            try:
                join = app.join_chat(link)
                id = join.id
            except BadRequest as e:
                e_id = e.ID
                if(e_id == 'USERNAME_INVALID'):
                    print('link eshtebah ast!')
                elif(e_id == 'USER_ALREADY_PARTICIPANT'):
                    print(f'karbare {session} dar grouh az ghabl bood!')
            except FloodWait as e:
                sleep_time = e.x
                print(f'{session} bayad {sleep_time} sanie esterahat kone!')
                sleep(sleep_time)
            except:
                print('error')
            else:
                print(f'{session} be grouh add shod!')
    



        
        return id
                

    
    
    

def send_message_to_members(session_list,text,max_send):
    with open('usernames.txt' , 'r+') as f:
        user_ids = f.readlines()
        for session in session_list:
            with Client(session) as app:
                tedad = 0 #==> tedade bedon=one error
                for i in range(0,max_send):
                    user_id = user_ids[i].replace('\n' , '')
                    app.send_message(chat_id = user_id , text = text)
                    print(user_id)
                    tedad += 1

            f.seek(0)
            f.truncate()
            f.writelines(user_ids[tedad:])



session_list = get_session_list()
#group_id = join_chat(session_list,LINK)
try:
    group_id = join_chat(session_list,LINK)
except UnboundLocalError:
    print('dar join shodan moshkeli vojood darad....\nlotfan barasi konid!')
else:
    get_group_members(session_list[0] ,group_id)

send_message_to_members(session_list,TEXT,MAX_SEND_PER_SESSION)

#print(group_members)




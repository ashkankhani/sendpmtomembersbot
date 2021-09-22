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
MAX_SEND_PER_SESSION = 1





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
    with open('usernames.txt' , 'w') as f:
        with Client(session) as app:
            members_logs = app.iter_chat_members(chat_id = group_id)
        
            for member in members_logs:
                if(not member.user.is_bot and member.user.username):
                    f.write(f'{member.user.username}\n')

        
        
    



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
        for session in session_list:
            user_names = f.readlines()
            b = len(user_names) #==>mahdoode
            if(max_send < b):
                b = max_send    #tanzim ro maximum
            with Client(session) as app:
                tedad = 0 #==> tedade bedon error
                for i in range(0,b):
                    user_name = user_names[i].replace('\n' , '')
                    app.send_message(chat_id = user_name , text = text)
                    tedad += 1

            f.seek(0)
            f.truncate()
            f.writelines(user_names[tedad:])



session_list = get_session_list()


while(True):
    gozine = input('''yek gozine entekhab konid:
1.join + jam avari id ha
2.ersal pm be hame afrad
''')
    if(gozine=='1'):
        try:
            group_id = join_chat(session_list,LINK)
        except UnboundLocalError:
            print('dar join shodan moshkeli vojood darad....\nlotfan barasi konid!')
        else:
            get_group_members(session_list[0] ,group_id)
    elif(gozine=='2'):
        send_message_to_members(session_list,TEXT,MAX_SEND_PER_SESSION)





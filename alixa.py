from time import sleep
import aminofix
import openai
from keep_alive import keep_alive


stats = True  # true then no public only private chat
email = "tahikille@gmail.com"
password = 'Eagle000'
#keep_alive()
# Define OpenAI API key
openai.api_key = "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"
devID = '1930528980D7CB871982F7210DCF8E3AD3CE68E38D828F696F7E9D60246FAE0A840D67D34211AEFA73'
dec = {}
hellomsg = 'مرحبا انا Open AI صممت من تطبيق الذكاء الاصطناعي وها انا هنا في امينو ، يشرفني وجودي هنا ...  :)'
hellomsg+='\n\n'
hellomsg+='اتمنى منك التزام قواعد المنتدى في الحديث وأي موضوع غير أخلاقي سيتم الابلاغ عنه في الحال'
hellomsg+='\n\n'
hellomsg+='اتمنى منك زيارة الحائط والتعليق بملاحظاتك حولنا... تجربة سعيدة ^.^'
client = aminofix.Client(deviceId=devID,proxies={{'http': '45.189.112.225:999', 'https': '45.189.112.225:999'}})
client.login(email=email, password=password)
print('loggned')
subclient = aminofix.SubClient(comId='3434136', profile=client.profile)
print('subclient')
size = 50 # the size of initial chats to check and REMEMBER 'save in memory'

messageBlog="انا 'OpenAI' قام بتصميمي [إيجل|http://aminoapps.com/p/t0ik76] وانا روبوت اي ذكاء اصطناعي " +'\n\n'+ "ومصدر معلوماتي هو chatGPT وها انا اليوم في أمينو " + "\n\n" + "اقضي على الملل وجربني " + "\n\n" + "تواصل معي في الخاص 🤍🤍" +"\n\n"+ "ملاحظة مازلت تحت التجربة ومازالت هناك مشاكل احاول اصلاحها" + "\n\n" + "للمزيد من التفاصيل الق نظرة على السيرة الذاتية"
title='تجربة'


#subclient.post_blog(title=title,content=messageBlog)

#exit(1)


@client.event("on_chat_invite")
def on_chat_invite(data):
    print('i got an invite')
    chatID = data.message.chatId
    subclient.join_chat(chatID)
    sleep(2)
    subclient.send_message(chatId=chatID, message=hellomsg)
    print('sent helloMSG')


@client.event("on_text_message")
def on_text_message(data):
    print('i got a message')
    message = data.message.content
    userId = data.message.author.userId
    # subclient.join_chat(chatID)
    if message and userId != '702813ba-a418-4de1-a615-d4957fda3c49':
        chatID = data.message.chatId
        if subclient.get_chat_thread(chatID).type and stats:
            sleep(2)
            subclient.leave_chat(chatId=chatID)
        else:
            if userId not in dec:
                dec[userId] = []
            dec[userId].append({'role': 'user', 'content': message}, )
            while True:
                try:
                    chatAI = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=dec[userId])
                    break
                except :
                    sleep(10)
            reply = chatAI.choices[0].message.content
            dec[userId].append({'role': 'assistant', 'content': reply})

            try:
                sleep(5)
                subclient.send_message(chatId=chatID, message=reply, replyTo=data.message.messageId)
                print('sent replay')
            except:
                print('Amino delay')
                pass


def start(size: int):

    chts = subclient.get_chat_threads(start=0, size=size).chatId
    print(f"start with {len(chts)} chats")
    for chatID in chts:
        x = subclient.get_chat_thread(chatID)
        UserID = x.author
        if x.type and stats:
            sleep(2)
            subclient.leave_chat(chatId=chatID)
        else:
            msgs = subclient.get_chat_messages(chatId=chatID, size=100).json

            if UserID not in dec:
                dec[UserID] = [{'role': 'system', 'content': 'You are a kind helpful assistant.'}, ]
            reply = False
            for msg in reversed(msgs):
                if msg['author']['uid'] != '702813ba-a418-4de1-a615-d4957fda3c49' and msg['content'] != None:
                    reply = True
                    dec[UserID].append({'role': 'user', 'content': msg['content']},)
                elif msg['author']['uid'] == '702813ba-a418-4de1-a615-d4957fda3c49' and msg['content'] != None:
                    reply = False
            if reply:
                while True:
                    try:
                        chatAI = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=dec[UserID])
                        break
                    except :
                        sleep(1)
                replyAI = chatAI.choices[0].message.content
                dec[UserID].append({'role': 'assistant', 'content': replyAI})
                while True:
                    try:
                        sleep(3)
                        subclient.send_message(chatId=chatID, message=replyAI)
                        break
                    except:
                        pass

    print('Done with save in MEMORY level')
def check(size:int):
    chts = subclient.get_chat_threads(start=0, size=size).chatId
    print(f'Check {len(chts)} chats')
    for chatID in chts:
        x = subclient.get_chat_thread(chatID)

        UserID = x.author

        if x.type and stats:
            sleep(2)
            subclient.leave_chat(chatId=chatID)
        else:
            UsersTALK=[]
            new = False
            msgs = subclient.get_chat_messages(chatId=chatID, size=10).json
            if UserID not in dec:
                dec[UserID] = [{'role': 'system', 'content': 'You are a kind helpful assistant.'}, ]
                new = True
            if not new:
                for msg in msgs:
                    if msg['author']['uid'] != '702813ba-a418-4de1-a615-d4957fda3c49' and msg['content'] != None:
                        UsersTALK.append(msg['content'])
                    elif msg['author']['uid'] == '702813ba-a418-4de1-a615-d4957fda3c49' and msg['content'] != None:
                        break
                if UsersTALK:
                    for msg in reversed(UsersTALK):
                        dec[UserID].append({'role': 'user', 'content': msg['content']}, )
                    while True:
                        try:
                            chatAI = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=dec[UserID])
                            break
                        except :
                            sleep(1)
                    replyAI = chatAI.choices[0].message.content
                    dec[UserID].append({'role': 'assistant', 'content': replyAI})
                    while True:
                        try:
                            sleep(3)
                            subclient.send_message(chatId=chatID, message=replyAI)
                            break
                        except:
                            pass
            else:
                reply=False
                for msg in reversed(msgs):
                    if msg['author']['uid'] != '702813ba-a418-4de1-a615-d4957fda3c49' and msg['content'] != None:
                        reply = True
                        dec[UserID].append({'role': 'user', 'content': msg['content']}, )
                    elif msg['author']['uid'] == '702813ba-a418-4de1-a615-d4957fda3c49' and msg['content'] != None:
                        reply = False
                if reply:
                    while True:
                        try:
                            chatAI = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=dec[UserID])
                            break
                        except :
                            sleep(1)
                    replyAI = chatAI.choices[0].message.content
                    dec[UserID].append({'role': 'assistant', 'content': replyAI})
                    while True:
                        try:
                            sleep(3)
                            subclient.send_message(chatId=chatID, message=replyAI)
                            break
                        except:
                            pass
    print('done with Check level')


def socketRoot():
    global size
    start(size)
    sleep(500)
    size=5
    while True:
        sleep(500)
        print("Updating socket.......")
        client.close()
        client.login(email=email, password=password)
        print("Socket updated")
        check(5)


socketRoot()


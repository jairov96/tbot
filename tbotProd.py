import telepot
import sys
import time

from telepot.loop import MessageLoop

botInfo = bot.getMe()

canon = 0
nikon = 0
olympus = 0
sony = 0

canonString = "canon"
nikonString = "nikon"
olympusString = "olympus"
sonyString = "sony"

answer = "succes"

def handle(msg):
    global canon
    global nikon
    global olympus
    global sony

    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    message = msg['text']

    print(msg['text'])

    if canonString in message.lower():
        canon = canon + 1
        print(canon)

    if nikonString in message.lower():
        nikon = nikon + 1
        print(nikon)

    if olympusString in message.lower():
        olympus = olympus + 1
        print(olympus)

    if sonyString in message.lower():
        sony = sony + 1
        print(sony)
        
    endString = """Hoy, tenemos estos ratings.
    Canon = {}
    Nikon = {}
    Olympus = {}
    Sony = {}
    
    """.format(canon, nikon, olympus, sony)

    if message == '/fanboy':
        bot.sendMessage(chat_id, endString)

    if message == '/isalive':
        bot.sendMessage(chat_id, 'is alive')


MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

input("")
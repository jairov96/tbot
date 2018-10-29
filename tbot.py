import telepot
import sys
import time
import sqlite3

from telepot.loop import MessageLoop
bot = telepot.Bot('x')

dbConnection = sqlite3.connect('shurbot.db',check_same_thread=False)
dbCursor = dbConnection.cursor()

botInfo = bot.getMe()


canon = 0
nikon = 0
olympus = 0
sony = 0

canonString = "canon"
nikonString = "nikon"
olympusString = "olympus"
sonyString = "sony"



def handle(msg): 
    global canon
    global nikon
    global olympus
    global sony

    content_type, chat_type, chat_id = telepot.glance(msg)

    message = msg['text'] 
    user = msg['from']['username']
    id = msg['message_id']

    #print(user + " " + msg['text']) #For debugging purposes


    if canonString in message.lower():
        dbCursor.execute("INSERT INTO shur VALUES(?,?,?,?)",(id,user,1,0))
        canon = canon + 1
        print(canon)

    if nikonString in message.lower():
        nikon = nikon + 1
        print(nikon)

    if olympusString in message.lower():
        olympus = olympus + 1
        print(olympus)

    if sonyString in message.lower():
        dbCursor.execute("INSERT INTO shur VALUES(?,?,?,?)",(id,user,0,1))
        sony = sony + 1
        print(sony)
        
    endString = """Hoy, tenemos estos ratings.
    Canon = {}
    Nikon = {}
    Olympus = {}
    Sony = {}

    """.format(canon, nikon, olympus, sony)



    #This is the list of commands users can interact with through the chat
    if message == '/fanboy':
        bot.sendMessage(chat_id, endString)

    if message == '/isalive':
        bot.sendMessage(chat_id, 'is alive')

    if message == '/retrieve':
        X = for row in dbCursor.execute('SELECT sum(canon) FROM shur ORDER BY id'):
            print(row)
        print(X)



MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')
input("")
    

import telepot
import sys
import time
import sqlite3

from telepot.loop import MessageLoop

#Define variables, I know, not an ideal practice.
canon = 0
nikon = 0
olympus = 0
sony = 0

#Here I define the camera brands as string. Suggestions welcome to improvide this!
canonString = "canon"
nikonString = "nikon"
olympusString = "olympus"
sonyString = "sony"

#Initiating a SQLITE databse
db = sqlite3.connect(':memory:')
cursor = db.cursor()
cursor.execute('''CREATE TABLE main(id INTEGER PRIMARY KEY, name TEXT, cameraBrand TEXT)''')
db.commit()

def handle(msg): #This is the actual message we receive from telegram.
    global canon 
    global nikon
    global olympus
    global sony

#This is nice here to be able to quickly look for this info later while testing, will be removed on prod
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    message = msg['text'] 
    user = msg['from']['username']
    id = msg['message_id']

    #print(user + " " + msg['text']) #For debugging purposes

    
    if canonString in message.lower():
        canon = canon + 1
        cursor.execute('''INSERT INTO main(id, name, cameraBrand)
                        VALUES(?,?,?)'''), (id,user,"canon")
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

    if message == '/retrieve':
        cursor.execute('''SELECT id,name,cameraBrand FROM main''')
        userFromDb = cursor.fetchone()
        print(userFromDb)

MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

input("")

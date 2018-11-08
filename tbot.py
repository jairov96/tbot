import telepot, sys, os, time, sqlite3, argparse
from telepot.loop import MessageLoop



# Defining arguments send through the console
parser = argparse.ArgumentParser()
parser.add_argument("-prod", help='Runs in production', action="store_true")
parser.add_argument("-s", "--silent", help='Does not show the output on terminal', action="store_true")
parser.add_argument("-debug", help="Debug mode", action="store_true")
args = parser.parse_args()

#Set DB connectiy
dbConnection = sqlite3.connect('shurbot.db',check_same_thread=False)
dbCursor = dbConnection.cursor()


# Get some environment variables
BOT_API = os.environ["BOT_API"]
print("api " + BOT_API)
if args.prod:
    BOT_API = os.environ["BOT_API_PROD"]

# Declare bot object
bot = telepot.Bot(BOT_API)
botInfo = bot.getMe()
if args.debug:
    print(botInfo)

#Define required variables
canon = 0
nikon = 0
olympus = 0
sony = 0
panasonic = 0

canonString = "canon"
nikonString = "nikon"
olympusString = "olympus"
sonyString = "sony"
panasonicString = "panasonic"

def handle(msg): 
    global canon
    global nikon
    global olympus
    global sony
    global panasonic

    content_type, chat_type, chat_id = telepot.glance(msg)

    message = msg['text'] 
    user = msg['from']['username']
    id = msg['message_id']

    if args.debug:
        print(user + " " + msg['text'])

    if canonString in message.lower():
        dbCursor.execute("INSERT INTO shur VALUES(?,?,?,?,?,?,?)",(id,user,1,0,0,0,0))
        canon = canon + 1
        print(canon)

    if nikonString in message.lower():
        dbCursor.execute("INSERT INTO shur VALUES(?,?,?,?,?,?,?)",(id,user,0,1,0,0,0))
        nikon = nikon + 1
        print(nikon)

    if olympusString in message.lower():
        dbCursor.execute("INSERT INTO shur VALUES(?,?,?,?,?,?,?)",(id,user,0,0,1,0,0))
        olympus = olympus + 1
        print(olympus)

    if sonyString in message.lower():
        dbCursor.execute("INSERT INTO shur VALUES(?,?,?,?,?,?,?)",(id,user,0,0,0,1,0))
        sony = sony + 1
        print(sony)

    if panasonicString in message.lower():
        dbCursor.execute("INSERT INTO shur VALUES(?,?,?,?,?,?,?)",(id,user,0,0,0,0,1))
        panasonic = panasonic + 1
        print(panasonic)

    dbConnection.commit()


    endString = """Hoy, tenemos estos ratings.
    Canon = {}
    Nikon = {}
    Olympus = {}
    Sony = {}
    Panasonic = {}

    """.format(canon, nikon, olympus, sony, panasonic)



    #This is the list of commands users can interact with through the chat
    if message == '/fanboy':
        bot.sendMessage(chat_id, endString)

    if message == '/isalive':
        bot.sendMessage(chat_id, 'is alive')

    if message == '/retrieve':
        
        for camera in dbCursor.execute('select sum(canon) from shur where user="%s"' % user):
            endcanon = camera
        for camera in dbCursor.execute('select sum(nikon) from shur where user="%s"' % user):
            endnikon = camera
        for camera in dbCursor.execute('select sum(olympus) from shur where user="%s"' % user):
            endolympus = camera
        for camera in dbCursor.execute('select sum(sony) from shur where user="%s"' % user):
            endsony = camera
        for camera in dbCursor.execute('select sum(panasonic) from shur where user="%s"' % user):
            endpanasonic = camera

        #for row in dbCursor.execute('select user, sum(canon), sum(nikon), sum(olympus), sum(sony), sum(panasonic) from shur where user="%s"' % user):
        #    print(row)
        
        endString = """Has mencionado las siguientes marcas tantas veces:
        Canon = {}
        Nikon = {}
        Olympus = {}
        Sony = {}
        Panasonic = {}
        """.format(endcanon, endnikon, endolympus, endsony, endpanasonic)
        
        bot.sendMessage(chat_id, endString)


MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')
input("")
    

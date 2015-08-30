import socket, string, os, atexit, sys
import argparse
from operator import itemgetter
from datetime import timedelta, datetime
from socket import timeout
import json

__DEBUG__ = False

HOST = "irc.twitch.tv"
NAME = ""
PORT = 6667
PASS = ""
CHANNEL = ""
readbuffer = ""
MODT = False
wordsDictionary = {}

#Documents time at start of execution
now = datetime.now()

#Setup arguments parser
parser = argparse.ArgumentParser(description='Twitch chat bot.')
parser.add_argument('--channel', type=str, help='Override Settings to switch channel')
parser.add_argument('--words', type=int, help='Number of unique words to listen to until quitting', default=100)
parser.add_argument('--clear_settings', action='store_true', help='Clears cached settings for name, oAuth, channel, etc.')
args = parser.parse_args()

#Open "filter" file and load the chat filters
if (os.path.isfile("filter.txt") == True):
	fileIO = open("filter.txt", "r")
	if fileIO.mode == "r":
		filter = fileIO.readlines()
	fileIO.close()
else:
	print "[Warning] Filter file not found! (filter.txt)"

#Setup application with user settings
data = dict()
dataChanged = False
if os.path.isfile("settings.txt"):
	file = open("settings.txt", "r")
	data = json.load(file)
	file.close()
if args.clear_settings:
    data = dict()
#import name
if data.has_key("NAME"):
	NAME = data["NAME"]
else:
    newValue = raw_input("What is your bot's name?\n")
    NAME = newValue
    data["NAME"] = newValue
    dataChanged = True
#import pass
if data.has_key("PASS"):
	PASS = data["PASS"]
else:
    newValue = raw_input("Obtain an oAuth password at twitchapps.com/tmi\nWhat is your oAuth password??\n")
    data["PASS"] = newValue
    PASS = newValue
    dataChanged = True
#import channel
if data.has_key("CHANNEL"):
	CHANNEL = data["CHANNEL"]
else:
    newValue = raw_input("What channel should I listen to?\n")
    data["CHANNEL"] = newValue
    CHANNEL = newValue
    dataChanged = True

if args.channel:
    CHANNEL = args.channel
    print args.channel

if dataChanged:
    file = open("settings.txt", "w+")
    json.dump(data, file)
    file.close()
    print "Settings changed"

s = socket.socket()
s.connect((HOST,PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NAME + "\r\n")
s.send("JOIN #" + CHANNEL + "\r\n")
s.settimeout(10)

@atexit.register
def OutputChatData():
    f = open("output.txt", "w+")
    temp = sorted(wordsDictionary.items(), reverse = True, key=itemgetter(1))
    for k in temp:
        f.write(str(k) + "\n")
    f.close()
    print "Created output file!"

def ReadChat():
    global readbuffer, MODT
    try:
        readbuffer = readbuffer + s.recv(1024)
    except timeout:
        if True:
            print "[Info] Caught socket recieve timeout"
    temp = string.split(readbuffer, "\n")
    if not MODT:
        print temp
    readbuffer = temp.pop()
    for line in temp:
        if(line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])

        else:
            parts = string.split(line, ":")

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:
                    message = parts[2][:len(parts[2]) -1]
                except:
                    message = ""

                usernamesplit = string.split(parts[1], "!")
                username = usernamesplit[0]

                if MODT:
                    #print username + ": " + message
                    message = message.translate(string.maketrans("",""), string.punctuation)
                    words = message.lower().split(" ")
                    counter = 0
                    for word in words:
                        if wordsDictionary.has_key(word):
                            wordsDictionary[word] = wordsDictionary[word] + 1
                            #print "Repeated word: " + word + " x " + str(wordsDictionary[word])
                        else:
                            if word not in filter and word.startswith("!") == False:
                                wordsDictionary[word] = 1
                                counter = counter + 1
                                #print "New word: " + word
                    print message + (" -> (%d new unique words)" % counter)
                    global args
                    if len(wordsDictionary) > args.words:
                        sys.exit()


                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
                        print "********************************************"
                        print "Connected to Twitch; Listening to chat on channel #" + str(CHANNEL)
                        print "********************************************"

while datetime.now() - now < timedelta(minutes = 10):
    #   print str(datetime.now() - now) + " out of " + str(timedelta(minutes = 10))
    ReadChat()

import socket, string, os, atexit, sys
import argparse
from operator import itemgetter
import json

HOST = "irc.twitch.tv"
NAME = ""
PORT = 6667
PASS = ""
CHANNEL = ""
readbuffer = ""
MODT = False
wordsDictionary = {'Word': 0}


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

#import name
if data.has_key("NAME"):
	NAME = data["NAME"]
else:
	newValue = raw_input("What is your bot's name?\n")
	data["NAME"] = newValue
	dataChanged = True
#import pass
if data.has_key("PASS"):
	PASS = data["PASS"]
else:
	newValue = raw_input("What is your oAuth password??\n")
	data["PASS"] = newValue
	dataChanged = True
#import channel
if data.has_key("CHANNEL"):
	CHANNEL = data["CHANNEL"]
else:
	newValue = raw_input("What channel should I listen to?\n")
	data["CHANNEL"] = newValue
	dataChanged = True
parser = argparse.ArgumentParser(description='Twitch chat bot.')
parser.add_argument('--channel', type=str, help='Override Settings to switch channel')
args = parser.parse_args()
if args.channel:
    CHANNEL = args.channel

if dataChanged:
	file = open("settings.txt", "w+")
	json.dump(data, file)
	file.close()

s = socket.socket()
s.connect((HOST,PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NAME + "\r\n")
s.send("JOIN #" + CHANNEL + "\r\n")

@atexit.register
def OutputChatData():
    f = open("output.txt", "w+")
    temp = sorted(wordsDictionary.items(), reverse = True, key=itemgetter(1))
    for k in temp:
        f.write(str(k) + "\n")
    f.close()
    print "Created output file!"

def ReadChat():
    global readbuffer
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()
    for line in temp:
        if(line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])
            print line[0] + " ||| " + line[1]

        else:
            parts = string.split(line, ":")

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:
                    message = parts[2][:len(parts[2]) -1]
                except:
                    message = ""

                usernamesplit = string.split(parts[1], "!")
                username = usernamesplit[0]

                global MODT
                if MODT:
                    #print username + ": " + message
                    words = message.lower().split(" ")
                    print words
                    for word in words:
                        if wordsDictionary.has_key(word):
                            wordsDictionary[word] = wordsDictionary[word] + 1
                            #print "Repeated word: " + word + " x " + str(wordsDictionary[word])
                        else:
                            if word not in filter:
                                wordsDictionary[word] = 1
                                #print "New word: " + word
                    if len(wordsDictionary) > 100:
                        sys.exit()


                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
                        print "Connected to Twitch; Listening to chat."

while 1:
    ReadChat()

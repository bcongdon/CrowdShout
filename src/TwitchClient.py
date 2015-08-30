import socket, string, os, atexit, sys
from operator import itemgetter

HOST = "irc.twitch.tv"
NAME = "Crowdshoutbot"
PORT = 6667
PASS = "oauth:kawkm0vci7c3oqeiom5d74u1lat26u"
readbuffer = ""
MODT = False
#CHANNEL = raw_input("Which channel should be watched? \n")
wordsDictionary = {'Word': 0}

#Open "filter" file and load the chat filters
if os.path.isfile("filter.txt"):
    fileIO = open("filter.txt", "r")
    if fileIO.mode == "r":
        filter = fileIO.readlines()
    fileIO.close()
else:
    print "[Warning] Filter file not found! (filter.txt)"
################

#Setup application with user settings
if os.path.isfile("settings.txt"):
    #LOAD SETTINGS#
    print "loading settings"
else:
    fileIO = open("settings.txt", "w+")
    #PROMPT USER FOR SETTINGS#
    fileIO.close()
################

s = socket.socket()
s.connect((HOST,PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NAME + "\r\n")
s.send("JOIN #sodapoppin \r\n")

@atexit.register
def OutputChatData():
    f = open("output.txt", "w+")
    temp = sorted(wordsDictionary.items(), key=itemgetter(1))
    for k in temp:
        f.write(str(k) + "\n")
    f.close()
    print "done!"

while True:
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

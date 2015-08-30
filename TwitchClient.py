import socket, string
import os

HOST = "irc.twitch.tv"
NAME = "Crowdshoutbot"
PORT = 6667
PASS = "oauth:kawkm0vci7c3oqeiom5d74u1lat26u"
readbuffer = ""
MODT = False
#CHANNEL = raw_input("Which channel should be watched? \n")
wordsDictionary = {'Word': 0}

fileIO = open("Filter.txt", "r")
if fileIO.mode == "r":
    filter = fileIO.readlines()

s = socket.socket()
s.connect((HOST,PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NAME + "\r\n")
s.send("JOIN #sodapoppin \r\n")

while True:
    readbuffer = readbuffer + s.recv(1024)
    #print readbuffer
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
                    for word in words:
                        if wordsDictionary.has_key(word):
                            wordsDictionary[word] = wordsDictionary[word] + 1
                            print "Repeated word: " + word + " x " + str(wordsDictionary[word])
                        else:
                            if word not in filter:
                                wordsDictionary[word] = 1
                                print "New word: " + word

                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True

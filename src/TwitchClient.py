import json
import os
import urllib2

def IsChannelOnline(channelName):
    url ="https://api.twitch.tv/kraken/streams/" + channelName
    try:
        contents = urllib2.urlopen(url)
    except:
        print "Error: Failed to get status of \"" + channelName + "\""
        return False
    contents = json.load(contents)
    try:
        if contents.has_key("stream"):
            return contents
    except:
        return False

def GetTopChannels():
    url ="https://api.twitch.tv/kraken/streams"
    try:
        contents = urllib2.urlopen(url)
    except:
        print "Error: Could not load streams."
        return None
    contents = json.load(contents)
    highestStream = contents["streams"][0]
    for stream in contents["streams"]:
        if stream["viewers"] > highestStream["viewers"]:
            highestStream = stream
    chat_prop_url = "https://api.twitch.tv/api/channels/" + highestStream["channel"]["name"] + "/chat_properties"
    try:
        chat_properties = urllib2.urlopen(chat_prop_url)
    except:
        print "Could not load chat properties. Exiting..."
        os._exit(1);
    chat_properties = json.load(chat_properties)
    newHost = chat_properties["chat_servers"][3].split(':')[0]
    global HOST
    HOST = newHost
    print HOST
    return highestStream["channel"]["name"]
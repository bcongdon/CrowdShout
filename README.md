# CrowdShout
A realtime tool for Twitch streamers to gauge the mood of their chat.

## Motivation

With Twitch viewership exploding, it can be difficult for streamers to make sense of their chat streams. Past a certain threshold of viewership, it is essentially impossible for a streamer to read individual messages, much less filter out all the spam present in most large twitch streams. Even with large teams of chat moderators, determining the mood of the chat, or the chat's responses to a streamer's question can be prohibitively difficult, causing many channels to switch to slow or subscriber-only mode.

CrowdShout aims to assist in reclaiming meaning from the onslaught of Twitch viewers' comments by analyzing the content of recent chat messages and presenting a realtime "digest" of the chat which can be understood at a glance.

## Usage
Optional arguments:
  -h, --help         show this help message and exit

  --channel CHANNEL  Override Settings to switch channel

  --words WORDS      Number of unique words to listen to until quitting

  --clear_settings   Clears cached settings for name, oAuth, channel, etc.

  --simple_chat      Outputs only user chat info. (Becomes passive chat
                     window)
                     
  --realtime         Outputs real time chat data

## References
Thanks to Exos for their python Twitch IRC client script: http://pastebin.com/PMx00Fsi

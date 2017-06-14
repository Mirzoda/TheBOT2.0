from irc import *
import os
import random

channel = "#pythonbottest"
server = "irc.quakenet.org"
port = 6667
nickname = "TheBOT2.0"

irc = IRC()
irc.connect(server, port, channel, nickname)


while 1:
    text = irc.get_text()
    print text

    if "PRIVMSG" in text and channel in text and "hello" in text:
        irc.send(channel, "Hello!")
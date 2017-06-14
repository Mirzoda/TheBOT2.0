from setup import *
import os
import random

channel = "#pythonbottest"
server = "irc.quakenet.org"
port = 6667
nickname = "TheBOT2_0"

irc = Bot();
irc.join(channel)
#irc.privmsg("Supermirza12", channel, "This is a test")
#while 1:
    #text = irc. irc.get_text()
    #print text
#
    #if "PRIVMSG" in text and channel in text and "hello" in text:
    #    irc.send(channel, "Hello!")
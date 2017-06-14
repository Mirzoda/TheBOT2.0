import socket
import sys

class IRC:
    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, chan, msg):
        self.irc.send("PRIVMSG " + chan + " " + msg + "n")

    def connect(self, server, port, channel, botnick):
        print "connecting to:" + server
        self.irc.connect((server, port))
        self.irc.send("quote PASS " + botnick + ":Testn")
        self.irc.send("USER " + botnick + " " + botnick + " " + botnick + " :This is a fun bot!n")
        self.irc.send("NICK " + botnick + "n")
        self.irc.send("JOIN " + channel + "n")

    def get_text(self):
        text=self.irc.recv(2040)

        if text.find('PING') != -1:
            self.irc.send('PONG ' + text.split()[1] + 'rn') 

        return text
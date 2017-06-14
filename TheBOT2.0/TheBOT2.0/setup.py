#!/usr/bin/env python2

"""A really simple IRC bot."""

import sys
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

class Bot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % self.nickname

    def joined(self, channel):
        self.sendLine("I has entered the channel")
        print "Joined %s." % channel

    def privmsg(self, user, channel, msg):
        if msg.startswith(self.username + ":"):
            command = msg.split(':')[1]
            if command == "HELLO":
                self.say(channel, "Hello " + user.split('!')[0])
            elif command == "TEST":
                print "TEST"
                self.msg(user, "You don't like me?")
                self.privmsg(user, channel, "You don't like me?2")
                self.say(channel, "This is indeed a test")
            elif command == "QUIT":
                self.quit("I'm gone :(")

class BotFactory(protocol.ClientFactory):
    protocol = Bot

    def __init__(self, channel, nickname='TheBOT2_0'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Connection lost. Reason: %s" % reason
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed. Reason: %s" % reason

if __name__ == "__main__":
    reactor.connectTCP('irc.quakenet.org', 6667, BotFactory('#pythonbottest'))
    reactor.run()

    
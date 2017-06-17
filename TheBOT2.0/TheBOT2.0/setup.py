#!/usr/bin/env python2

"""A really simple IRC bot."""
import sys
import ast
import re
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
from settings import *

class Bot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed On"

    def joined(self, channel):
        self.say(channel, "I has entered the channel!")
        print "Joined channel " + channel

    def privmsg(self, user, channel, msg):
        isAdmin = False
        #Change later to [1] to use identnames (currently testing on webchat)
        username = user.split('!')[0]

        if username in Admins:
            isAdmin = True

        try:
            c = Commands()
            startChar = msg[:1]
            #if msg == "KILL":
            #    self.quit("ForceKill")
            if startChar == "@":
                command = msg.split('@')[1]
                #print "Command: '" + command + "'"

                if command == "Commands":
                    self.say(channel, "I know these commands: " + "; ".join(c.GetAllCommands()))
                elif command == "Bye":
                    if isAdmin:
                        self.quit("ByeBye")
            elif startChar == "!":
                command = msg.split('!')[1]
                if command == "":
                    return
                self.say(channel, c.GetRandomResponse(command))
            elif msg.startswith(self.nickname + ": !"):
                if isAdmin:
                    r = re.compile('' + self.nickname + '\: \!([a-zA-Z0-9]*) (.*)')
                    aMessage = r.match(msg)
                    if aMessage is not None:
                        command = aMessage.group(1)
                        response = aMessage.group(2)
                        c.UpdateCommand(command, response)
                else:
                    self.say(channel, "Only admins may add commands")
        except BaseException as ex:
            print "privmsg Exception Message: " + ex.message            
            print "privmsg Exception: " + repr(ex)

class Commands():
    def GetRandomResponse(self, command):
        #print "Start GetRandomResponse|Argument " + command

        try:
            temp = open(CommandFile)
        except IOError:
            # Could not open file (does't exist)
            return "I don't know commands! Make some for me"
        
        commandFile = open(CommandFile)
        dictCommands = ast.literal_eval(commandFile.read())
        
        returnText = "I don't know this command!"
        if command in dictCommands:
            returnText = dictCommands[command]

        commandFile.close()
        #print "End GetRandomResponse|Return " + returnText
        return returnText

    def UpdateCommand(self, command, response):
        #print "Start UpdateCommand|Arguments " + command + "/" + response

        try:
            temp = open(CommandFile, "r+")
        except IOError:
            temp = open(CommandFile, "w+")
            #Default Command
            dict = { "Hello" : "Hello World!" }
            temp.write(str(dict))
            temp.close()
        
        commandFile = open(CommandFile, "r+")
        dictCommands = ast.literal_eval(commandFile.read())
        
        # Create/Update command with response
        dictCommands[command] = response
        
        # Switch to write
        commandFile.seek(0)
        commandFile.write(str(dictCommands))
        # Close File
        commandFile.close()
        #print "End UpdateCommand"

    def GetAllCommands(self):
        #print "Start GetAll"

        try:
            temp = open(CommandFile)
        except IOError:
            # Could not open file (does't exist)
            return "I don't know commands! Make some for me"
        
        commandFile = open(CommandFile, "r")
        dictCommands = ast.literal_eval(commandFile.read())

        #print "End GetAll"
        return dictCommands.keys()

class BotFactory(protocol.ClientFactory):
    protocol = Bot

    def __init__(self, channel, nickname):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Connection lost. Reason: %s" % reason
        self.stopFactory()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed. Reason: %s" % reason
        self.stopFactory()

if __name__ == "__main__":
    # Runned by this file
    reactor.connectTCP(Server, Port, BotFactory(Channel, BotName))
    reactor.run()
#else:
    # Imported by another module
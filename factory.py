#!/usr/bin/env python

# Copyright 2011 Igor Popov
#
# This file is part of ihpbot, which is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import imp
import inspect
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

import config
import createdb
import commands

###
if not os.path.exists('db/ihpbot.sqlite'):
    createdb.start()
###

class Bot(irc.IRCClient):
    def __init__(self):
        self.command = ""

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        print "Signed on as %s." % self.nickname
        for channel in self.factory.channels:
            self.join(channel)

    def joined(self, channel):
        print "Joined %s." % channel
    
    def send_reply(self, data, user, channel):
        target = channel if channel.startswith('#') else user
        self.msg(target, data)
        print config.nickname + " > (" + target + "): " + data

    def privmsg(self, user, channel, msg):
        username = user.split('!')[0]
        print username + ": " + msg
        if ( msg[0] == config.command_prefix ):
            self.command = msg[1:]
            self.process_command(username, ( channel ))

    def evalCommand(self, commandname, user, channel):
        imp.reload(commands)
        command_function=getattr(commands, commandname, None)
        if command_function != None:
            if inspect.isfunction(command_function):
                command_function(self, user, channel)
    
    def process_command(self, user, channel):
        command = (self.command).split()
        self.evalCommand(command[0].lower(), user, channel)

class BotFactory(protocol.ClientFactory):
    protocol = Bot

    def __init__(self, channels, nickname=config.nickname):
        self.channels = channels
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Connection lost. Reason: %s" % reason
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed. Reason: %s" % reason

if __name__ == "__main__":
    reactor.connectTCP(config.server, config.port, BotFactory(config.channels.split(',')))
    reactor.run()

#!/usr/bin/env python

# Copyright 2011 IgorPopov
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

from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
import config

class Bot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        print "Signed on as %s." % self.nickname
        for channel in self.factory.channels:
            self.join(channel)

    def joined(self, channel):
        print "Joined %s." % channel

    def privmsg(self, user, channel, msg):
        username = user.split('!')[0]
        print username + ": " + msg
        if ( msg[0] == config.command_prefix ):
            self.factory.command = msg[1:]
            self.factory.process_command(username, ( channel ))

class BotFactory(protocol.ClientFactory):
    protocol = Bot

    def __init__(self, channels, nickname=config.nickname):
        self.channels = channels
        self.nickname = nickname
        self.command = ""

    def clientConnectionLost(self, connector, reason):
        print "Connection lost. Reason: %s" % reason
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed. Reason: %s" % reason
    
    def process_command(self, user, channel):
        command = (self.command).split()

if __name__ == "__main__":
    reactor.connectTCP(config.server, config.port, BotFactory(config.channels.split(',')))
    reactor.run()

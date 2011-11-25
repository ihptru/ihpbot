#!/usr/bin/env python3

# Copyright 2011 Popov Igor
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
import socket
import time
import sqlite3
import re

import config
import createdb
import commands

class IRC:
    
    def __init__(self, conf_conn, host, port, nickname, channels, prefix, nickserv, nickserv_pw):
        self.irc_host = host
        self.irc_port = port
        self.irc_nick = nickname
        self.prefix = prefix
        self.channels = channels
        self.conf_conn = conf_conn
        self.nickserv = nickserv
        self.nickserv_pw = nickserv_pw
        self.irc_sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.command = ""
        self.start_time = time.mktime(time.strptime( time.strftime('%Y-%m-%d-%H-%M-%S'), '%Y-%m-%d-%H-%M-%S'))
        self.connected = False

    def ircbot(self):
        if not os.path.exists('db/'+self.conf_conn+'.sqlite'):
            createdb.start(self)
        while True:
            #exit codes:
            # 1 - could not connect to irc server
            # 2 - excess flood
            # 3 - manual quit
            # 4 - nick is in use
            exit_code = self.connect()
            if (exit_code == 1):
                time.sleep(5)
                continue
            elif (exit_code == 2):
                print("[%s] Restarting the bot" % self.conf_conn)
                time.sleep(5)
                self.irc_sock.close()
                continue
            elif (exit_code == 3):
                print("[%s] Exit" % self.conf_conn)
                break
            else:
                break

    def connect(self):
        try:
            self.irc_sock.connect ((self.irc_host, self.irc_port))
            self.connected = True
        except:
            print (("Error: Could not connect to IRC; Host: %s Port: %s")  % (self.irc_host, self.irc_port))
            return 1
        print (("[%s] Connected to: %s:%s") % (self.conf_conn, self.irc_host, self.irc_port))

        def set_bot(self):
            str_buff = ("NICK %s \r\n") % (self.irc_nick)
            self.irc_sock.send (str_buff.encode())
            print (("[%s] Setting bot nick to %s") % (self.conf_conn, self.irc_nick))

            str_buff = ("USER %s 8 * :X\r\n") % (self.irc_nick)
            self.irc_sock.send (str_buff.encode())
            print (("[%s] Setting User") % (self.conf_conn))

            for channel in self.channels.split():
                str_buff = ( "JOIN %s \r\n" ) % (channel)
                self.irc_sock.send (str_buff.encode())
                print (("[%s] Joining channel %s") % (self.conf_conn, channel))

            if self.nickserv == True:
                print (("[%s] Sending request to identify with NickServ...") % (self.conf_conn))
                data = "identify "+self.nickserv_pw
                self.irc_sock.send ( (("PRIVMSG %s :%s\r\n") % ('NickServ', data)).encode() )

        set_bot(self)

        while True:
            exit_code = self.listen()
            if (exit_code == 4):
                self.irc_nick = self.irc_nick + "_"
                set_bot(self)
                continue
            elif (exit_code == 3):
                return 3
            elif (exit_code == 2):
                return 2
            else:
                return 0

    def listen(self):
        while self.connected:
            recv = self.irc_sock.recv( 4096 )
            recv = self.decode_stream(recv)
            data = self.handle_recv(str(recv))
            for recv in data:
                if recv.find ( "PING" ) != -1:
                    self.irc_sock.send ( ("PONG " + recv.split()[1] + "\r\n").encode() )
        return 0

    def decode_stream(self, stream):
        try:
            return stream.decode("utf8")
        except:
            return stream.decode("CP1252")

    #handle as single line request as multiple ( split recv into pieces before processing it )
    def handle_recv(self, recv):
        regex = re.compile('(.*?)\r\n')
        recv = regex.findall(recv)
        return recv

    def db_data(self):
        conn = sqlite3.connect('db/'+self.conf_conn+'.sqlite')   # connect to database
        cur = conn.cursor()
        return (conn, cur)

if __name__ == "__main__":
    def create_dirs(dirs):
        for dirname in dirs:
            try:
                os.mkdir(dirname)
                os.chmod(dirname, 0o700)
            except OSError as e:
                if e.args[0]==17:   #Directory already exists
                    pass    #Ignore
                else:
                    raise e #Raise exception again

    create_dirs(['db','logs'])

    config_data = eval('config.'+config.servers[0])
    irc = IRC(config.servers[0], config_data['host'], config_data['port'], config_data['nick'], config_data['channels'], config_data['prefix'], config_data['nickserv'], config_data['nickserv_pw'])
    try:
        irc.ircbot()
    except KeyboardInterrupt:
            print("Exit")
            exit

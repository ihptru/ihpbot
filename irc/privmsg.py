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

import re

def parser(self,  recv):
    irc_user_nick = recv.split ( '!' ) [ 0 ] . split ( ":" ) [ 1 ]
    irc_user_message = self.data_to_message(recv)
    chan = recv.split() [ 2 ]  #channel
    chan_raw = chan.replace('#','')
    print ( ( "[%s] %s: %s" ) % (self.conf_conn, irc_user_nick, irc_user_message) )
    conn, cur = self.db_data()
    sql = """INSERT INTO "msg_%(chan_raw)s"
            (message)
            VALUES
            (
            '%(irc_user_message)s'
            )
    """ % vars()
    cur.execute(sql)
    conn.commit()
    cur.close()
    # Message starts with command prefix?
    if ( irc_user_message != '' ):
        if ( irc_user_message[0] == self.prefix ):
            self.command = irc_user_message[1:].replace("'","''")
            self.process_command(irc_user_nick, ( chan ))
    
    # Start analysing message
    analyse(self,  irc_user_message.replace("'", "''"))

def analyse(self, message):
    
    def check_incorrect(self,  conn,  cur,  question,  answer):
        pass

    def check_tables(self,  conn,  cur,  message):
        for channel in self.channels.split():
            tb_name = 'msg_'+channel.replace('#','')
            sql = """SELECT uid,message FROM "%(tb_name)s"
            """ % vars()
            cur.execute(sql)
            records = cur.fetchall()
            for i in range(len(records)):
                pass
            conn.commit()

    words = message.split()
    amount_words = float(len(words))
    conn,  cur = self.db_data()
    sql = """SELECT question,answer FROM correct_response
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    
    class GetOutOfLoop(Exception):
        pass
    
    answer = ''
    
    try:
        for i in range(len(records)):
            match = 0
            question = records[i][0]
            for word in words:
                if word in question.split():
                    match += 1
            if match != 0:
                if amount_words/100*match >= 0.8:
                    answer = records[i][1]
                    raise GetOutOfLoop
    except GetOutOfLoop:
        pass

    if ( answer != '' ):    # found match in `correct_response` table
        check_incorrect(self,  conn,  cur,  question,  answer)
    else:   # nothing found in `correct_response` table, go on checking channel tables
        check_tables(self,  conn,  cur,  message)

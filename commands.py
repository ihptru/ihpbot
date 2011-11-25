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

import sqlite3
import config

def correct(self, user, channel):
    #if not self.Admin(user, channel):
    #    return
    command = (self.command).split()
    if ( len(command) > 1 ):
        usage = "Usage: " + config.command_prefix + "correct"
        self.send_notice(usage, user)
        return
    conn = sqlite3.connect('db/ihpbot.sqlite')
    cur = conn.cursor()
    sql = """SELECT question,answer FROM last_answer
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0 ):
        message = "Nothing to confirm..."
        self.send_notice(message, user)
        return
    elif ( len(records) == 1 ):
        sql = """INSERT INTO correct_response
                (question,answer)
                VALUES
                (
                '"""+records[0][0]+"""','"""+records[0][1]+"""'
                )
        """
        cur.execute(sql)
        conn.commit()
    self.send_notice("Done", user)
    cur.close()

def incorrect(self, user, channel):
    #if not self.Admin(user, channel):
    #    return
    command = (self.command).split()
    if ( len(command) > 1 ):
        usage = "Usage: " + config.command_prefix + "incorrect"
        self.send_notice(usage, user)
        return
    conn = sqlite3.connect('db/ihpbot.sqlite')
    cur = conn.cursor()
    sql = """SELECT question,answer FROM last_answer
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0 ):
        message = "Nothing to mark as incorrect..."
        self.send_notice(message, user)
    elif ( len(records) == 1 ):
        sql = """INSERT INTO incorrect_response
                (question,answer)
                VALUES
                (
                '"""+records[0][0]+"""','"""+records[0][1]+"""'
                )
        """
        cur.execute(sql)
        conn.commit()
    self.send_notice("Done", user)
    cur.close()

def delete_correct(self, user, channel):
    #if not self.Admin(user, channel):
    #    return
    command = (self.command).split()
    usage = "Usage: " + config.command_prefix + "delete_correct {question|answer} string"
    if ( len(command) < 3 ):
        self.send_notice(usage, user)
        return
    conn = sqlite3.connect('db/ihpbot.sqlite')
    cur = conn.cursor()
    if ( command[1].lower() == 'question' ):
        delete_what = 'question'
    elif ( command[1].lower() == 'answer' ):
        delete_what = 'answer'
    else:
        self.send_notice(usage, user)
        return
    request = " ".join(command[2:])
    sql = """SELECT uid,"""+delete_what+""" FROM correct_response
            WHERE upper("""+delete_what+""") LIKE upper('%"""+request+"""%')  
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0 ):
        self.send_notice("Nothing found...", user)
    elif ( len(records) == 1 ):
        sql = """DELETE FROM correct_response
                WHERE uid = """+str(records[0][0])+"""
        """
        cur.execute(sql)
        conn.commit()
        message = "Removed entry where " + delete_what + " is: " + str(records[0][1])
        self.send_notice(message, user)
    else:
        self.send_notice("Too many matches...", user)

def delete_incorrect(self, user, channel):
    #if not self.Admin(user, channel):
    #    return
    command = (self.command).split()
    usage = "Usage: " + config.command_prefix + "delete_incorrect {question|answer} string"
    if ( len(command) < 3 ):
        self.send_notice(usage, user)
        return
    conn = sqlite3.connect('db/ihpbot.sqlite')
    cur = conn.cursor()
    if ( command[1].lower() == 'question' ):
        delete_what = 'question'
    elif ( command[1].lower() == 'answer' ):
        delete_what = 'answer'
    else:
        self.send_notice(usage, user)
        return
    request = " ".join(command[2:])
    sql = """SELECT uid,"""+delete_what+""" FROM incorrect_response
            WHERE upper("""+delete_what+""") LIKE upper('%"""+request+"""%')  
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0 ):
        self.send_notice("Nothing found...", user)
    elif ( len(records) == 1 ):
        sql = """DELETE FROM incorrect_response
                WHERE uid = """+str(records[0][0])+"""
        """
        cur.execute(sql)
        conn.commit()
        message = "Removed entry where " + delete_what + " is: " + str(records[0][1])
        self.send_notice(message, user)
    else:
        self.send_notice("Too many matches...", user)

def add_correct(self, user, channel):
    #if not self.Admin(user, channel):
    #    return
    command = (self.command).split()
    if ( len(command) < 3 ):
        message = "Usage: " + config.command_prefix + "add_correct {question} {answer}"
        self.send_notice(message, user)
        return
    try:
        question_answer = " ".join(command[1:])
        question = question_answer.split('} {')[0].replace('{','').strip()
        answer = question_answer.split('} {')[1].replace('}','').strip()
    except Exception as e:
        print ("add_correct(): ", e)
        return
    conn = sqlite3.connect('db/ihpbot.sqlite')
    cur = conn.cursor()
    sql = """SELECT answer FROM correct_response
            WHERE answer = '"""+answer+"""' AND question = '"""+question+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) != 0 ):
        self.send_notice("Record already exists", user)
        return
    sql = """INSERT INTO correct_response
            (question,answer)
            VALUES
            (
            '"""+question+"""','"""+answer+"""'
            )
    """
    cur.execute(sql)
    conn.commit()
    self.send_notice("Done", user)
    cur.close()

def add_incorrect(self, user, channel):
    #if not self.Admin(user, channel):
    #    return
    command = (self.command).split()
    if ( len(command) < 3 ):
        message = "Usage: " + config.command_prefix + "add_incorrect {question} {answer}"
        self.send_notice(message, user)
        return
    try:
        question_answer = " ".join(command[1:])
        question = question_answer.split('} {')[0].replace('{','').strip()
        answer = question_answer.split('} {')[1].replace('}','').strip()
    except Exception as e:
        print ("add_incorrect(): ", e)
        return
    conn = sqlite3.connect('db/ihpbot.sqlite')
    cur = conn.cursor()
    sql = """SELECT answer FROM incorrect_response
            WHERE answer = '"""+answer+"""' AND question = '"""+question+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) != 0 ):
        self.send_notice("Record already exists", user)
        return
    sql = """INSERT INTO incorrect_response
            (question,answer)
            VALUES
            (
            '"""+question+"""','"""+answer+"""'
            )
    """
    cur.execute(sql)
    conn.commit()
    self.send_notice("Done", user)
    cur.close()

def help(self, user, channel):
    command = (self.command).split()
    if ( len(command) == 1 ):
        self.send_reply( ("I can't help you..."), user, channel)

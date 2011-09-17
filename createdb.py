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
import sqlite3
import config

def start():
    try:
        os.mkdir("db")
        os.chmod("db", 0o700)
    except:
        print("Error! Can not create a directory, check permissions and try again")
        return
    print("Creating databases")
    msgs()
    last_answer()
    correct_response()
    incorrect_response()

def msgs():
    conn = sqlite3.connect('db/ihpbot.sqlite')
    cur = conn.cursor()
    for channel in config.channels.replace('#','').split(','):
        print "..."
        sql = """CREATE TABLE "msg_"""+channel+"""" (
            uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
            message VARCHAR NOT NULL
            )        
        """
        cur.execute(sql)
        conn.commit()
    cur.close()

def last_answer():
    print "..."
    conn = sqlite3.connect('db/ihpbot.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE last_answer (
        uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        question VARCHAR NOT NULL,
        answer VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    cur.close()

def correct_response():
    print "..."
    conn = sqlite3.connect('db/ihpbot.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE correct_response (
        uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        question VARCHAR NOT NULL,
        answer VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    cur.close()

def incorrect_response():
    print "..."
    conn = sqlite3.connect('db/ihpbot.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE incorrect_response (
        uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        question VARCHAR NOT NULL,
        answer VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    cur.close()

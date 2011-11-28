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

def start(self):
    print("Creating databases")
    conn, cur = self.db_data()
    
    msgs(self, conn, cur)
    last_answer(conn, cur)
    correct_response(conn, cur)
    incorrect_response(conn, cur)
    
    cur.close()
    print("Done")

def msgs(self, conn, cur):
    for channel in self.channels.replace('#','').split():
        print ("...")
        sql = """CREATE TABLE "msg_%(channel)s" (
            uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
            message VARCHAR NOT NULL
            ) 
        """ % vars()
        cur.execute(sql)
        conn.commit()

def last_answer(conn, cur):
    print ("...")
    sql = """CREATE TABLE "last_answer" (
        uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        question VARCHAR NOT NULL,
        answer VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

def correct_response(conn, cur):
    print ("...")
    sql = """CREATE TABLE "correct_response" (
        uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        question VARCHAR NOT NULL,
        answer VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

# incorrect table has more power above correct one
def incorrect_response(conn, cur):
    print ("...")
    sql = """CREATE TABLE "incorrect_response" (
        uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        question VARCHAR NOT NULL,
        answer VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

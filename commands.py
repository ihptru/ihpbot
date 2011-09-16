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

def correct(self, user, channel):
    pass

def incorrect(self, user, channel):
    pass
    
def help(self, user, channel):
    command = (self.command).split()
    if ( len(command) == 1 ):
        self.send_reply( ("I can't help you..."), user, channel)
        

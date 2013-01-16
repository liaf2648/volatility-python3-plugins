# Volatility
# Copyright (C) 2007,2008 Volatile Systems
# Copyright (C) 2010,2011,2012 Michael Hale Ligh <michael.ligh@mnin.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details. 
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA 
#

import volatility.utils as utils
import volatility.plugins.gui.constants as consts
import volatility.plugins.gui.sessions as sessions

class Gahti(sessions.Sessions):
    """Dump the USER handle type information"""

    def render_text(self, outfd, data):

        profile = utils.load_as(self._config).profile

        # Get the OS version being analyzed 
        version = (profile.metadata.get('major', 0),
                   profile.metadata.get('minor', 0))

        # Choose which USER handle enum to use 
        if version >= (6, 1):
            handle_types = consts.HANDLE_TYPE_ENUM_SEVEN
        else:
            handle_types = consts.HANDLE_TYPE_ENUM

        self.table_header(outfd,
                         [("Session", "8"),
                          ("Type", "20"),
                          ("Tag", "8"),
                          ("fnDestroy", "[addrpad]"),
                          ("Flags", ""),
                         ])

        for session in data:
            gahti = session.find_gahti()
            if gahti:
                for i, h in list(handle_types.items()):
                    self.table_row(outfd,
                                    session.SessionId,
                                    h,
                                    gahti.types[i].dwAllocTag,
                                    gahti.types[i].fnDestroy,
                                    gahti.types[i].bObjectCreateFlags)

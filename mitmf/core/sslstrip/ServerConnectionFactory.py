# Copyright (c) 2014-2016 Moxie Marlinspike, Marcello Salvati
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#

import logging

from core.logger import logger
from twisted.internet.protocol import ClientFactory

formatter = logging.Formatter("%(asctime)s [ServerConnectionFactory] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
log = logger().setup_logger("ServerConnectionFactory", formatter)

class ServerConnectionFactory(ClientFactory):

    def __init__(self, command, uri, postData, headers, client):
        self.command      = command
        self.uri          = uri
        self.postData     = postData
        self.headers      = headers
        self.client       = client

    def buildProtocol(self, addr):
        return self.protocol(self.command, self.uri, self.postData, self.headers, self.client)
    
    def clientConnectionFailed(self, connector, reason):
        log.debug("Server connection failed.")

        destination = connector.getDestination()

        if (destination.port != 443):
            log.debug("Retrying via SSL")
            self.client.proxyViaSSL(self.headers['host'], self.command, self.uri, self.postData, self.headers, 443)
        else:
            try:
                self.client.finish()
            except:
                pass

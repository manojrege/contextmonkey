#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017, Technische Universität Berlin
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# - Neither the name of the Technische Universitaet Berlin nor the names
#   of its contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Genymotion client connection."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

from twisted.internet import task
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic  import LineReceiver

class GennyMotionClient(LineReceiver):
    """Base class for connection to GennyMotion emulator."""

    def connectionMade(self):
        """Handle transport connection using keep alive messages."""
        self.transport.setTcpKeepAlive(1)
        
    def clearLineBuffer(self):
        """Clear buffer data."""
        pass
    
    def dataReceived(self,data):
        """Handle data received."""
        pass
        
    def setLineMode(self, extra=''):
        """Set the client in line received mode."""
        pass
    
    def setRawMode(self, data):
        """Set the client in raw reeived mode."""
        pass
    
    def rawDataReceived(self, data):
        """Handle data received in raw mode."""
        pass
    
    def lineRecieved(self, line):
        """Handle data received in line mode."""
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()

    
    def sendLine(self, line):
        """Send line data to server."""
        self.transport.write(line)
    
    def lineLengthExceeded(self, line):
        """Handle when maximum line length reached."""
        pass

class GennyMotionGpsProtocolClient(GennyMotionClient):
    """Class for connection to GennyMotion emulator for GPS protocol."""

    sensorName = 'gps'
    accuracy = None        #[0; 200]
    altitude = None       #[-20; 10000]
    bearing = None        #[0; 359]
    latitude = None        #[-90; 90]
    longitude = None       #[-180; 180]
    status = None
    
    def sendData(self, **values):
		"""issue a set command for GPS sensor."""
		if "longitude" in values:
			self.longitude = values["longitude"]
		else:
			raise Exception('Missing parameter "longitude" for GPS set command')
			return
			
		if "latitude" in values:
			self.latitude = values["latitude"]
		else:
			raise Exception('Missing parameter "latitude" for GPS set command')
			return
			
		if "altitude" in values:
			self.altitude = values["altitude"]
		else:
			self.altitude = 0
			
		if "bearing" in values:
			self.bearing = values["bearing"]
		else:
			self.bearing = 5
		
		print('sending string: geo fix %.5f %.5f %.2f %d' % (self.longitude, self.latitude, self.altitude, self.satellites))
		self.sendLine(('gps setlongitude %.5f\n' % (self.longitude)).encode('UTF-8'))
		self.sendLine(('gps setlatitude %.5f\n' % (selself.latitude)).encode('UTF-8'))
		self.sendLine(('gps setaltitude %.5f\n' % (self.altitude)).encode('UTF-8'))

    def getData(self):
        """Get GPS sensor data."""
        # TODO: issue 'get' command and really query for current data
        data = {'longitude': self.longitude, 'latitude': self.latitude, 'altitude': self.altitude, 'bearing': self.bearing}
        return data
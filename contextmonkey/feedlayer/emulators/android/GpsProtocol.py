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

"""Gps Protocol for setting and getting geolocation values from Android Emulator."""

__author__ = "Thomas Hoffmann"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Thomas Hoffmann"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import time

from contextmonkey.feedlayer.emulators.android.GeneralSensorProtocol import GeneralSensorProtocol
from contextmonkey.ContextMonkeyLogger import feed

class GpsProtocol(GeneralSensorProtocol):
    """Provide methods for setting and getting geolocation values from Android Emulator."""
     
    sensorName = 'Gps'
    longitude = 0
    latitude = 0
    altitude = 0
    satellites = 0
 
    def sendData(self, uuid, **values):
        """Issue set command for setting GPS sensor."""
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
        if "satellites" in values:
            self.satellites = values["satellites"]
        else:
            self.satellites = 5
        command='sending string: geo fix %.5f %.5f %.2f %d' % (self.longitude, self.latitude, self.altitude, self.satellites)
        self.sendLine(command.encode('UTF-8'))
        feed.log('GPSPROTOCOL-sendData', command)
        feed.log('GPSPROTOCOL-sendData',self.sensorName+" End Time:"+str("%0.20f" % time.time())+" "+str(uuid))
        
    def getData(self):
        """Issue a get command for getting current value of GPS sensor."""

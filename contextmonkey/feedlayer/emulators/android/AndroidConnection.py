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

"""Connection to the Android emulator for making API calls."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import traceback

from twisted.internet import reactor
from twisted.internet import defer

from contextmonkey.ContextMonkeyExceptions import DisconnectedModalityError
from contextmonkey.ContextMonkeyLogger import feed

class AndroidConnection(object):
    """Provide methods for connecting to Android emulator."""

    def __init__(self, emulator, host=None, port=None):
        """Initialize."""
        self.emulator = emulator
        self.host = host
        self.port = port

    def registerEmulator(self,emulator):
        """Register emulator with the framework."""
        if ':' not in self.emulator.connection['addr']:
            self.host = '127.0.0.1'
            self.port = self.emulator.connection['addr']
        else:
            self.host, self.port = self.emulator.connection['addr'].split(':', 1)

        self.port = int(self.port)
        feed.log("ANDROIDCONNECTION-registerEmulator",'Registered emulator with data:')
        feed.log("ANDROIDCONNECTION-registerEmulator",'Host: %s' % self.host)
        feed.log("ANDROIDCONNECTION-registerEmulator",'Port: %d' % self.port)
        return True

    def connectSensorCallback(self, uuid, sensor, factory, **value):
        """Callback function for connectSensor."""
        self.emulator.activeSensors.update({sensor: factory})
        self.setSensorValue(sensor, uuid, **value)

    def connectSensorErrback(self, reason):
        """Handle error in connectSensor."""
        feed.log("ANDROIDCONNECTION-connectSensorErrback",'Connection attempt to sensor failed: %s' %(reason.getErrorMessage()))
                  

    def connectSensor(self, sensor, uuid, **value):
        """Connect to sensor in Android emulator."""
        clModule = __import__("contextmonkey.feedlayer.emulators.%s.%sSensorClientFactory" % (self.emulator.emulatorname.lower(), self.emulator.emulatorname.capitalize()), fromlist=["%sSensorClientFactory" % self.emulator.emulatorname.capitalize()])
        clFactory = getattr(clModule, "%sSensorClientFactory" % self.emulator.emulatorname.capitalize())
        d = defer.Deferred()
        factory = clFactory(sensor, d)
        d.addCallback(self.connectSensorCallback, sensor, factory, **value)
        d.addErrback(self.connectSensorErrback)
        d.callback(uuid)
        reactor.connectTCP(self.host, self.port, factory)
        feed.log("ANDROIDCONNECTION-connectSensor","%s connected" % sensor)

    def setSensorValue(self, sensor, uuid, **value):
        """Issue a set command to sensor on Android emulator."""
        if self.emulator is None:
            raise SystemError('You must first register an emulator with the EmulatorManager!')
        if sensor in self.emulator.activeSensors:
            try:
                self.emulator.activeSensors[sensor].sendValue(uuid, **value)
                feed.log("ANDROIDCONNECTION-setSensorValue",str(uuid))
            except DisconnectedModalityError:
                feed.log("ANDROIDCONNECTION-setSensorValue",'Sensor %s seems to be disconnected, removing ...' % sensor)
                self.disconnectSensor(sensor)
            except:
                feed.log("ANDROIDCONNECTION-setSensorValue",traceback.print_exc())
        else:
            self.connectSensor(sensor, **value)


    def disconnectSensor(self, sensor):
        """Disconnect from a sensor tcp connection and removes it from EmulatorManager instance."""
        if self.emulator is None:
            raise SystemError('You must first register an emulator with the EmulatorManager!')

            if not sensor in self.emulator.activeSensors:
                raise SystemError(
                    'The requested sensor "%s" is not registered with the current emulator.' % sensor)
            else:
                try:
                    self.emulator.activeSensors[sensor].connectedProtocol.transport.loseConnection()
                except:
                    pass

                del self.emulator.activeSensors[sensor]
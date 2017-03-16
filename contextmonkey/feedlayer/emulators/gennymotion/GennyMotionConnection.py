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
#__________________          ___________________           ___________________
#|                |          |                 |           |                 |
#|                |          |                 |           |                 |
#|   GennyMotion  |<-------->|   GennyMotion   |<--------->|   GennyMotion   |
#|     Telnet     |          |      Shell      |           |     Emulator    |
#|________________|          |_________________|           |_________________|



"""Implementation for connection to GennyMotion emulator."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import os
import random

from twisted.internet import reactor
from twisted.internet import defer

from contextmonkey.feed.emulators.gennymotion.GennyMotionTelnetFactory import GennyMotionTelnetFactory

class GennyMotionConnection(object):
    """Provide methods for Genymotion connection."""

    def __init__(self, emulator, host=None, port=None):
        """Initialize."""
        self.emulator = emulator
        self.host = host
        self.port = port
        print "GennyMotion connection %s" % self.emulator.emulatorname.capitalize()

    def registerEmulator(self,emulator):
        """Start GennyMotion Telnet Server."""
        if ':' not in self.emulator.connection['addr']:
            self.host = '127.0.0.1'
            self.port = self.emulator.connection['addr']
        else:
            self.host, self.port = self.emulator.connection['addr'].split(':', 1)

        self.port = int(self.port)
        
        gennymotionfactory = GennyMotionTelnetFactory('/Applications/GenymotionShell.app/Contents/MacOS/genyshell','192.168.57.101')
        reactor.listenTCP(self.port, gennymotionfactory)
        
        print('Registered emulator with data:')
        print('Host: %s' % self.host)
        print('Port: %d' % self.port)
        return True

    def connect_init(self, modality, **value):
        """Open a new connection to a sensor based on emulator information."""
        gennymotionfactory = GennyMotionTelnetFactory('/Applications/GenymotionShell.app/Contents/MacOS/genyshell','192.168.57.101')
        reactor.listenTCP(8000, gennymotionfactory)
        
        clModule = __import__("contextmonkey.feed.emulators.gennymotion.%sClientFactory" % self.emulator.emulatorname, fromlist=["%sClientFactory" 
        % self.emulator.emulatorname])
        clFactory = getattr(clModule, "%sClientFactory" % self.emulator.emulatorname)
        d = defer.Deferred()
        factory = clFactory(sensor, d)
        d.addCallback(self.connectSensorCallback, sensor, factory, **value)
        d.addErrback(self.connectSensorErrback)
        reactor.connectTCP(self.host, self.port, factory)

    def connectSensorCallback(self, nothing, sensor, factory, **value):
        """Provide callback to connectSensor."""
        self.emulator.activeSensors.update({sensor: factory})
        self.setSensorValue(sensor, **value)

    def connectSensorErrback(self, reason):
        """Handle sensor connection error."""
        print('Connection attempt to sensor failed: %s' %(reason.getErrorMessage()))
                  

    def connectSensor(self, sensor, **value):
        """Open a new connection to a sensor based on emulator information."""
        from twisted.internet import reactor
        
        clModule = __import__("contextmonkey.feed.emulators.gennymotion.%sClientFactory" % self.emulator.emulatorname, fromlist=["%sClientFactory" % self.emulator.emulatorname])
        clFactory = getattr(clModule, "%sClientFactory" % self.emulator.emulatorname)
        d = defer.Deferred()
        factory = clFactory(sensor, d)
        d.addCallback(self.connectSensorCallback, sensor, factory, **value)
        d.addErrback(self.connectSensorErrback)
        reactor.connectTCP(self.host, self.port, factory)


    def disconnectSensor(self, sensor):
        """Disconnect from a sensor tcp connection and remove it from EmulatorManager instance."""
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
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

"""Provides SensorClientFactory for Android Emulator."""

__author__ = "Thomas Hoffmann"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Thomas Hoffmann"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../../../../')

import time

from twisted.python.failure import Failure
from twisted.internet.protocol import ClientFactory

from contextmonkey.feedlayer.emulators.android.GpsProtocol import GpsProtocol
from contextmonkey.feedlayer.emulators.android.AccelerationProtocol import AccelerationProtocol
from contextmonkey.feedlayer.emulators.android.NetworkProtocol import NetworkProtocol
from contextmonkey.feedlayer.emulators.android.MagneticFieldProtocol import MagneticFieldProtocol
from contextmonkey.feedlayer.emulators.android.CameraProtocol import CameraProtocol
from contextmonkey.ContextMonkeyExceptions import DisconnectedModalityError
from contextmonkey.ContextMonkeyLogger import feed
from contextmonkey.ContextMonkeyEngine import contextmonkeyreactor

class AndroidSensorClientFactory(ClientFactory):
    """Initialize and map trace set request to the sensor."""
    availableSensors = { 'Gps': GpsProtocol,
                                'acceleration': AccelerationProtocol,
                                'network': NetworkProtocol,
                                'magneticfield': MagneticFieldProtocol,
                                'camera': CameraProtocol
                                }
    protocol = None
    deferred = None
    connectedProtocol = None

    def __init__(self, sensor, deferred):
        """Identify correct protocol for given sensor name."""
        try:
            self.protocol = self.availableSensors[sensor]
        except Exception as e:
            raise SystemError('No Sensor available by name %s' % sensor)
        self.sensor = sensor
        self.deferred = deferred

    def buildProtocol(self, address):
        """Build protocol and store it in this instance."""
        proto = ClientFactory.buildProtocol(self, address)
        self.connectedProtocol = proto
        return proto

        def connectionLost(self, reason):
            """Handle connection loss."""
        self.connectedProtocol = None
        feed.log('ANDROIDSENSORCLIENTFACTORY-connectionLost','%d - Connection to sensor %s was terminated: %s' % time.time(), self.sensor, reason.getErrorMessage())

        def clientConnectionFailed(self, connector, reason):
            """Handle a failed connection attempt to the sensor."""
        if not self.deferred is None:
            d, self.deferred = self.deferred, None
            d.errback(Failure(Exception('Connection to %s sensor failed' % self.sensor)))
        else:
            contextmonkeyreactor.stop()
            raise SystemError('The connection attempt to %s sensor failed more than once. Check if emulator is running' % self.sensor)

    def commandFailed(self, reason):
        """Handle a failed set/get command prototype."""
        feed.log('ANDROIDSENSORCLIENTFACTORY-commandFailed',str(reason))
        #if self.deferred is not None:
            #d, self.deferred = self.deferred, None
            #d.errback(reason)

    def sendValue(self, uuid, **value):
        """Send sensor value to the sensor."""
        if self.connectedProtocol is None:
            raise DisconnectedModalityError('Could not set value - sensor "%s" is not connected!' % self.sensor)
        feed.log('ANDROIDSENSORCLIENTFACTORY-sendValue',str(self.connectedProtocol.sensorName+" Begin Time:"+str("%0.20f" % time.time())+" "+str(uuid)))
        feed.log('ANDROIDSENSORCLIENTFACTORY-sendValue',str(self.connectedProtocol))
        feed.log('ANDROIDSENSORCLIENTFACTORY-sendValue-timestamp:',str(uuid)+" "+str("%0.20f" % time.time()))
        feed.log('ANDROIDSENSORCLIENTFACTORY-sendValue-timestamp:',str(value))
        self.connectedProtocol.sendData(uuid, **value)

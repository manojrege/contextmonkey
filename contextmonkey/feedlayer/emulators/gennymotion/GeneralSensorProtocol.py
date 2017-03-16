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

"""General sensor communication protocol functions for Genymotion Emulator."""

__author__ = "Thomas Hoffmann"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Thomas Hoffmann"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

from twisted.protocols.basic import LineReceiver
from twisted.python.failure import Failure
from subprocess import check_output, CalledProcessError


class GeneralSensorProtocol(object):
    """Base class for making Genymotion emulator API calls."""
    
    def __init__(self):
        """Initialize."""
        self.sensorName = None
        self.ip = '192.168.57.101'
    
    def setapiCommandList(self,sensorname):
        """Provide sensor API command list for setting sensors."""
        command = {'gps':{'acc':'gps setaccuracy', 'alt':'gps setaltitude', 'bearing':'gps setbearing'
        , 'lat':'gps setlatitude', 'lon':'gps setlongitude', 'sat':'gps setstatus'}}
        return command[sensorname]
    
    def getapiCommandList(self,sensorname):
        """Provide sensor API command list for getting sensors."""
        command = {'gps':{'acc':'gps getaccuracy', 'alt':'gps getaltitude', 'bearing':'gps getbearing'
        , 'lat':'gps getlatitude', 'lon':'gps getlongitude', 'sat':'gps getstatus'}}
        
        return command[sensorname]
    
    def getCommandLineOptions(self,sensorname):
        """Return command line options for sensor."""
        return {'x'}
    
    def getPath(self):
        """Provide path for genyshell."""
        return '/Applications/GenymotionShell.app/Contents/MacOS/genyshell'

    def sendData(self, attribute, **values):
        """Issue a set command for the sensor."""
        if self.sensorName is None:
            raise SystemError('sendData cannot be called as long as sensorName is unknown')
        
        values = self.validateInput(**values)
        cmdlist = self.setapiCommandList(self.sensorName)
        cmd = cmdlist[attribute]
        for option in self.getCommandLineOptions(self.sensorName):
            cmd += " "+str(values[option])
        try:
            p = check_output([self.getPath(), '-r',self.ip,'-c', cmd])
            print p
        except CalledProcessError, e:
            print "Failed to execute"
            
    def getData(self,attribute):
        """Issue a set command for the sensor."""
        if self.sensorName is None:
            raise SystemError('sendData cannot be called as long as sensorName is unknown')
        cmdlist = self.getapiCommandList(self.sensorName)
        cmd = cmdlist[attribute]
        try:
            p = check_output([self.getPath(), '-r',self.ip,'-c', cmd])
            print p
        except CalledProcessError, e:
            print "Failed to execute"
            
    def validateInput(self, **values):
        """Validate input."""
        if not 'x' in values:
            print('Missing x value - assuming zero')
            values.update({'x': 0})
        return values

    def lineReceived(self, line):
        """Handle incoming data."""
        pass

    def connectionLost(self, reason):
        """Handle connection losses."""
        pass

    def connectionMade(self):
        """Set connection to keep-alive mode."""
        pass 
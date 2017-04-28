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

"""Build and configure Genymotion client."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import os
import sys
import inspect
import random
import fnmatch
import importlib

from twisted.internet import task
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic  import LineReceiver

import contextmonkey.feed.emulators.gennymotion.GennyMotionClient

def findmatch(members,classprefix):
    """Find match for class member."""
    lst = [n for (n,c) in members]
    return fnmatch.filter(lst,classprefix)

def generate_dictionary_classnames(classlist):
   """Generate class name."""
   return {eval("GennyMotionClient."+classname+".sensorName"):eval("GennyMotionClient."+classname) 
   for classname in classlist}
    

class GennyMotionClientFactory(ClientFactory):
    """Implementation for building and configuring GenyMotion client."""

    availableModality = generate_dictionary_classnames(findmatch(inspect.getmembers(GennyMotionClient, 
    		   inspect.isclass),"GennyMotion*ProtocolClient"))
    protocol = None
    deferred = None
    connectedProtocol = None
    
    def __init__(self,modality,deferred):
        """Initialize."""   
        try:
            self.protocol = self.availableModality[modality]
        except:
            raise(SystemError, "Sensor not present")
        self.defer = deferred
        self.modality = modality
    
    def buildProtocol(self,address):
        """Build Genymotion client protocol."""
        proto = ClientFactory.buildProtocol(self, address)
        self.connectedProtocol = proto
        return proto
        
    def startedConnecting(self, connector):
        """Begin connection."""
        pass
    
    def clientConnectionFailed(self, connector, reason):
        """Handle client connection failure."""
        print reason.getErrorMessage()
        d = self.deferred
        self.deferred = None
        d.errback(reason)
    
    def clientConnectionLost(self, connector, reason):
        """Handle lost connection."""
        self.connectedProtocol = None
        print reason.getErrorMessage()
        self.defer.callback(None)
    
    def sendValue(self, **value):
        """Send command with sensor data values."""
    	if self.connectedprotocol == None:
    	    raise DisconnectedSensorError('Could not set value - sensor "%s" is not connected!' % self.modality)
        self.connectedprotocol.sendData(self,**value)



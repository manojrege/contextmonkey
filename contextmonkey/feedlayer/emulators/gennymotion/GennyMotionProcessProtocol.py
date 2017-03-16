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

"""Implementation of interprocess communication between GennyMotion shell and ContextMonkey."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.protocol import ProcessProtocol

class GennyMotionProcessProtocol(ProcessProtocol):
    """Provide methods for inter-process communication between Genymotion shell and emulator handler."""

    def __init__(self, emulator=None, path = None, deferred=None):
        """Initialize."""
        self.emulator = emulator
        self.path = path
        self.command = 'gps setlatitude 23\n'
        self.output = ""
        self.deferred = deferred
        self.outputcount=0
 
    def connectionMade(self):
        """Handle connection established."""
        pass
    
    def outReceived(self, data):
        """Handle data received."""
        #self.transport.loseConnection()
        self.output+=data
        self.outputcount+=1
        print self.output
        print str(self.outputcount)
        if "GPS Latitude set to" in self.output:
            #self.deferred.callback(self.output)
            self.output=""
            #reactor.callLater(1.0,self.sendData,'gps setlatitude '+str(random.randint(-90,90))+'\n')
        elif "Failed" in self.output:
            self.errReceived("Failed to set value")
        
    def errReceived(self, data):
        """Handle error."""
        print "Some error occured"
        print data
    
    def inConnectionLost(self):
        """Handle lost connection."""
        print "stdin closed"
    
    def processEnded(self, reason):
        """Handle process ended."""
        print "process ended"
        pass      
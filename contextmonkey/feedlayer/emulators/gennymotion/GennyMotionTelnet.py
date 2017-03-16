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

"""Implementation of Telnet Server enabling inter-process communication to GennyMotion Shell."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import os

from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory

from contextmonkey.feed.emulators.gennymotion.GennyMotionProcessProtocol import GennyMotionProcessProtocol

#'/Applications/GenymotionShell.app/Contents/MacOS/genyshell'

class GennyMotionTelnet(Protocol):
    """Provide methods for telnet implementation."""

    cmd = None;
    ip = None;
    
    def __init__(self,cmd, ip):
        """Initialize."""
        self.pp = None
        self.cmd = cmd
        self.ip = ip
    
    def connectionMade(self):
        """Handle upon connection establishment."""
        self.pp = GennyMotionProcessProtocol()
        reactor.spawnProcess(self.pp,self.cmd,[self.cmd,'-r','192.168.57.101'],env={'HOME': os.environ['HOME']})
    
    def dataReceived(self, data):
        """Handle received data."""
        print "Telnet received data %s"% data
        self.pp.transport.write(data)
    
    def connectionLost(self, reason):
        """Handle lost connection."""
        self.pp.transport.loseConnection()
        

    

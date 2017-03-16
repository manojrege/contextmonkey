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

"""Implementation of ITraceModfy interface for accelerometer traces."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append('../../../')

import random
import traceback
from zope.interface import implements

from contextmonkey.protofiles import sensor_pb2
from contextmonkey.tracelayer.interfaces.ITraceModify import ITraceModify

@implementer(ITraceModify)
class JiitAccelerometer(object):
    """Class providing implementation of ITraceModfy for OpenSignal traces."""
    
    filterattributes = None

    def __init__(self):
        """Initialize JiitAcceleroMeterModify filter."""
        self.tracedatalist = []

    def filterTrace(self, tracedata, uuid):
        """Remove unwanted attributes from the accelerometer traces."""
        attributelist = ['x', 'y', 'z']
        valuelist=tracedatalist.split(',')[1:3]
        tempdict = {}
        for key,value in zip(attributelist,valuelist):
            try:
                tempdict[key] = float(value)
            except:
                print traceback.format_exc()
        return tempdict

    def handlefailure(self, dummy=None):
        """Handle trace fetching failure."""
        pass           
        
    def processTrace(self,tracedatalist, uuid):
        """Perform Unit conversions."""
        return tracedatalist
        
        
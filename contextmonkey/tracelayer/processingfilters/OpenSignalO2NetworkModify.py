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

"""OpenSignal Network data processing filter for O2 carrier."""

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

import json
import time
import traceback
from zope.interface import implementer

from contextmonkey.tracelayer.interfaces.ITraceModify import ITraceModify
from contextmonkey.ContextMonkeyExceptions import FilterTraceError
from contextmonkey.ContextMonkeyLogger import tracelayer

@implementer(ITraceModify)
class OpenSignalO2NetworkModify(object):
    """Implementation of ITraceModfy interface for OpenSignal traces of O2 carrier."""
    
    filterattributes = None

    def __init__(self):
        """Initialize OpenSignalNetworkModify object."""
        self.tracedata = None

    def filterTrace(self, tracedata, **kwargs):
        """Remove unwanted attributes from the OpenSignal trace."""
        try:
            tracelayer.log("OPENSIGNALNETWORKMODIFY-filterTrace","In filter trace")
            tracelayer.log("OPENSIGNALNETWORKMODIFY-filterTrace",str(tracedata))
            begin=time.time()
            tempdict = {}
            kwargs={'carrierName':'O2','carrierType':'type3G','attributes':['networkName','averageRssiDb','downloadSpeed','uploadSpeed','pingTime']}
            b = json.loads(tracedata)
            carrierlist = b['networkRank']
            networkattributes = None
            for carrier in carrierlist:
                networklist = carrierlist[carrier]
              
                if kwargs['carrierType'] in networklist:
                    networkattributes = networklist[kwargs['carrierType']]
                    if kwargs['carrierName'] in networkattributes['networkName']:
                        for key in kwargs['attributes']:
                            tempdict.update({key:networkattributes[key]})
                        end=time.time()-begin
                        tracelayer.log("OPENSIGNALNETWORKMODIFY-TraceProcessing",str(end*1000))
                        tracelayer.log("OPENSIGNALNETWORKMODIFY-filterTrace",str(tempdict))
                        return tempdict
            raise FilterTraceError("Network name missing")
                            
        except:
            raise FilterTraceError("Unable to process trace")
            tracelayer.log("OPENSIGNALNETWORKMODIFY-filterTrace",traceback.print_exc())
            

    def handlefailure(self, dummy=None):
        """Handle failure of fetching OpenSingal trace, by generating default values."""
        tracelayer.log("OPENSIGNALNETWORKMODIFY-handlefailure","A failure occured")
        tempdict = {'uploadSpeed':574.72,'averageRssiDb':22,'downloadSpeed':1213.44,'pingTime':98} #KB/s ms
        return tempdict              
        
    def processTrace(self,tracedata, **kwargs):
        """Perform Unit conversions from kbps to bps."""
        tracelayer.log("OPENSIGNALNETWORKMODIFY-processTrace",str(tracedata))
        tracedata['uploadSpeed']= float(tracedata['uploadSpeed'])*1024*8                    #in bits/s
        tracedata['downloadSpeed']= float(tracedata['downloadSpeed'])*1024*8
        tracelayer.log("OPENSIGNALNETWORKMODIFY-processTrace",str(tracedata))
        return tracedata

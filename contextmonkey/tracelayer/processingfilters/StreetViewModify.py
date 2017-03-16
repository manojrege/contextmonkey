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

"""StreetView image data processing filter."""

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

import time
import subprocess
import traceback
from zope.interface import implementer

from contextmonkey.tracelayer.interfaces.ITraceModify import ITraceModify
from contextmonkey.ContextMonkeyGlobal import cachepath
from contextmonkey.ContextMonkeyExceptions import ContextMonkeyTraceProcessingFailedError
from contextmonkey.ContextMonkeyLogger import tracelayer

@implementer(ITraceModify)
class StreetViewModify(object):
    """Implementation of ITraceModfy interface for StreetView image traces."""
    
    filterattributes = None

    def __init__(self):
        """Initialize StreetVieModify filter."""
        self.tracedata = None

    def filterTrace(self, tracedata, uuid, **kwargs):
        """Remove unwanted attributes from the tracedata."""
        tracelayer.log("StreetViewModify-filterTrace-timestamp:",str("%0.20f" % time.time())+" "+str(uuid))
        return tracedata

    def handlefailure(self, dummy=None):
        """Handle image fetching failure."""
        #tracelayer.log("StreetViewModify-handleFailure-timestamp:",str(time.time())+" "+str(uuid))
        pass             
        
    def processTrace(self,tracedata, uuid, **kwargs):
        """Perform image format conversion."""
        try:
            tracelayer.log("StreetViewModify-processTrace1-timestamp:",str("%0.20f" % time.time())+" "+str(uuid))
            global cachepath
            tracedata=cachepath+'/'+str(tracedata)+'.jpg'
            print tracedata
            filename,extension = path.splitext(tracedata)
            command = 'ffmpeg -loglevel panic -i '+tracedata+' -s 640x400 -pix_fmt yuv422p -thread 0 -f v4l2 /dev/video0'
            subprocess.call(command.split(),shell=False)
            with open(tracedata, "rb") as binary_file:
                data = binary_file.read()
            tracelayer.log("StreetViewModify-processTrace2-timestamp:",str("%0.20f" % time.time())+" "+str(uuid))
            return {'image':data,'encoded':len(data),'original':len(data),'camera_type':'back'}
        except:
            raise ContextMonkeyTraceProcessingFailedError(traceback.print_exc())

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

"""Get trace as a file from a database service using HTTPS protocol with GET method."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../../../../' ) 

import traceback
import urllib
import time

from subprocess import call
from twisted.internet.defer import Deferred
from twisted.internet import defer
from twisted.internet.ssl import ClientContextFactory
from twisted.internet import reactor
from twisted.web.client import downloadPage

from contextmonkey.tracelayer.handlers.database.DatabaseRequestHandler import DatabaseRequestHandler
from contextmonkey.ContextMonkeyLogger import tracelayer
from contextmonkey.tracelayer.DataSourceManager import DataSourceManager
from contextmonkey.ContextMonkeyGlobal import cachepath
from contextmonkey.ContextMonkeyLogger import tracelayer

class HTTPSFileDownloadRequestHandler(DatabaseRequestHandler):
    """Provide methods to download trace file from a database service using HTTPS."""
    
    url = None
    filename = None
    extension = None
    deferred = Deferred()
    contextFactory=ClientContextFactory()
   
    def __init__(self):
        """Initialize."""
        pass

    def failure(self,reason,reason1):
        """Handle file download failure."""
        tracelayer.log("HTTPSFileDownloadRequestHandler-failure","Request failed "+ str(reason))

    def success(self,dummy=None,uuid=None,modality=None):
        """Forward the trace file for filtering and processing."""
        d = Deferred()
        d.addCallback(DataSourceManager.filter_data, uuid, modality)
        d.callback(uuid)
        tracelayer.log("HTTPSFileDownloadRequestHandler-success-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid)) 

    def executeFetch(self,uuid,modality):
        """Send HTTPS GET request for downloading trace file from a database service."""
        try:
            global cachepath
            self.url = modality.datasource.url+"?"+urllib.urlencode(modality.datasource.queryparameters)
            self.extension=modality.datasource.extension
            self.filename=cachepath+'/'+str(uuid)+'.'+self.extension
            self.deferred = downloadPage(self.url,self.filename,contextFactory = self.contextFactory).addCallback(self.success,uuid,modality)
            tracelayer.log("HTTPSFileDownloadRequestHandler-executeFetch-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
            return defer.gatherResults([self.deferred])
        except:
            traceback.print_exc()

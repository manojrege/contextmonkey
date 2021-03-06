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

"""Get trace from a database service using HTTPS protocol with GET method."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../../../' )

import urllib
import time

from subprocess import call
from twisted.internet.defer import Deferred
from twisted.web.client import Agent, readBody
from twisted.python.log import err
from twisted.web.client import Agent
from twisted.internet import reactor
from twisted.internet.ssl import ClientContextFactory
from twisted.web.http_headers import Headers

from DatabaseRequestHandler import DatabaseRequestHandler
from contextmonkey.ContextMonkeyLogger import tracelayer

class HTTPClientContextFactory(ClientContextFactory):
    """Provide methods for Twisted Web Client."""

    def __init__(self):
        """Initialize."""
        pass

    def getContext(self, hostname, port):
        """Provide Twisted Web client context."""
        return ClientContextFactory.getContext(self)

class HTTPSGetRequestHandler(DatabaseRequestHandler):
    """Provide methods to obtain traces from a database service using HTTPS GET method."""
    
    body = None
    agent = Agent(reactor, HTTPClientContextFactory())
    url = None
    params = None
    headers = Headers({'Content-Type': ['application/json; charset=utf-8'], 'User-Agent': ["Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11"],'Accept-Encoding': ["gzip, deflate, sdch"]})

    def __init__(self):
        """Initialize."""
        pass
           
    def bodyFormat(self, response,uuid,modality):
        """Extract HTTPS trace response."""
        d = readBody(response)
        d.addCallback(self.getBody)
        d.addCallback(self.success,uuid,modality)
        d.addErrback(self.failure)
        tracelayer.log("HTTPSGetRequestHandler-bodyFormat-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
        return self.body

    def success(self,dummy=None,uuid=None,modality=None):
        """Forward the trace for filtering and processing."""
        d = Deferred()
        d.addCallback(DataSourceManager.filter_data, uuid, modality)
        d.callback(dummy)
        tracelayer.log("HTTPSGetRequestHandler-success-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
        
 
    def failure(self, reason):
        """Handle trace fetching failure."""
        tracelayer.log("HTTPSGETREQUESTHANDLER-FAILURE","Request failed "+ str(reason))

    def getBody(self, body):
        """Get response body of the HTTPS based trace fetching request."""
        self.body = body
        tracelayer.log("HTTPSGetRequestHandler-getBody",unicode(self.body, errors='ignore'))
        return self.body  

    def executeFetch(self,uuid, modality):
        """Send HTTPS GET request for fetching trace from a database service."""
        try:
            self.url = modality.datasource.url+"?"+urllib.urlencode(modality.datasource.queryparameters)
            d = self.agent.request('GET', self.url,self.headers)
            d.addErrback(self.failure)
            d.addCallback(self.bodyFormat,uuid,modality)
            tracelayer.log("HTTPSGetRequestHandler-executeFetch-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid)) 
            return d
        except:
            tracelayer.log("HTTPSGetRequestHandler-executeFetch:",traceback.print_exc())
        
        
           

 


    



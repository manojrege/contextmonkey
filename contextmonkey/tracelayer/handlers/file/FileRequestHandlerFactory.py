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

"""Map trace fetching request from a trace file to handler."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../../../') 

import linecache
import random
import requests
import importlib
import traceback
from subprocess import call
from collections import namedtuple

from twisted.internet import reactor
from twisted.web.client import downloadPage
from twisted.internet.ssl import ClientContextFactory
from twisted.internet import ssl
from twisted.internet.defer import Deferred

from ContextMonkeyExceptions import ContextMonkeyUnSupportedTraceFormatError
from contextmonkey.tracelayer.handlers.file.ContextMonkeyFileCache import ContextMonkeyFileCache

class FileRequestHandlerFactory(object):
    """Initialize file handlers and map trace request to the appropriate handler."""

    fileprotocol = None
    filetype = {'text':'TEXTFileRequestHandler','csv':'CSVFileRequestHandler','json':'JSONFileRequestHandler','xml':'XMLFileRequestHandler'}
    dsdict = {'json', 'binary', 'xml'}
    currentprotocol = None
    currentiterator = 0
    contextmonkeyfiles = ContextMonkeyFileCache()
    
    def __init__(self,**kwargs):
        """Initialize file handler."""
        self.kwargs = kwargs
        
    def build(self):
        """Build the file handler protocol."""
        d = Deferred()
        d.addCallback(self.loadProtocol, **self.kwargs)
        d.addErrback(self.loadProtocolFailed)
        d.callback(None)  

    def loadProtocol(self, dummy=None, **kwargs):
        """Load file handler protocol."""
        try:
            filename = kwargs['tracefile']
            self.contextmonkeyfiles.addFileToCache(filename)
            formattype = kwargs['formattype'] ### text, csv, json, xml
            proto = self.filetype[formattype]
            module_ = importlib.import_module("contextmonkey.tracelayer.handlers.file."+proto)
            class_ = getattr(module_,proto)
            self.currentprotocol = class_(filename)
        except Exception as inst:
             print (traceback.print_exc())
             print (type(inst))
             print (inst)

    def loadProtocolFailed(self, reason):
        """Handle protocol load failure."""
        print "Loading protocol failed" + str(reason)
        
    def executeFetch(self,uuid, modality):
        """Handle trace fetch request from a file."""
        if self.currentprotocol == None:
            raise SystemError("No appropriate protocol loaded")
            return
        d = Deferred()
        d.addCallback(self.currentprotocol.executeFetch,modality)
        d.addErrback(self.loadProtocolFailed)
        d.callback(uuid)   
        return d
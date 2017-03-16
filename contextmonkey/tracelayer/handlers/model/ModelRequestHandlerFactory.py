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

"""Map trace fetching request from a trace model to a handler."""

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

class ModelRequestHandlerFactory(object):
    """Initialize model handlers and map trace request to the appropriate handler."""

    modelprotocol = None
    protocoltype = {'singlephase':'SinglePhaseRequestHandler','twophase':'TwoPhaseModelRequestHandler'}
    currentprotocol = None

    def __init__(self,**kwargs):
        """Initialize model handler."""
        self.kwargs = kwargs
        
    def build(self):
        """Build the model handler protocol."""
        d = Deferred()
        d.addCallback(self.loadProtocol, **self.kwargs)
        d.addErrback(self.loadProtocolFailed)
        d.callback(None)

    def loadProtocol(self, dummy=None, **kwargs):
        """Load model handler protocol."""
        try:
            fetchtype = kwargs['modeltype']  
            formattype = kwargs['formattype'] 
            proto = self.protocoltype[fetchtype]
            module_ = importlib.import_module("contextmonkey.tracelayer.handlers.model."+proto)
            class_ = getattr(module_,proto)
            self.currentprotocol = class_()
            
        except Exception as inst:
             traceback.print_exc()

    def loadProtocolFailed(self, reason):
        """Handle protocol load failure."""
        print "Loading protocol failed" + str(reason)
        
    def executeFetch(self, uuid, modality):
        """Handle trace fetch request from a model."""
        if self.currentprotocol == None:
            raise SystemError("No appropriate protocol loaded")
        d = Deferred()
        d.addCallback(self.currentprotocol.executeFetch,modality)
        d.addErrback(self.loadProtocolFailed)
        d.callback(uuid)
        return d
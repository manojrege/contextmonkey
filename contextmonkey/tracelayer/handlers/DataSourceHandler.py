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

"""Data-source handler operations in the trace layer."""

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

import linecache
import random
import requests
import importlib
import time

from subprocess import call
from collections import namedtuple
from twisted.internet import reactor
from twisted.web.client import downloadPage
from twisted.internet.ssl import ClientContextFactory
from twisted.internet import ssl
from twisted.internet.defer import Deferred

from contextmonkey.ContextMonkeyExceptions import ContextMonkeyEmulatorLoadException
from contextmonkey.tracelayer.handlers.file.FileRequestHandlerFactory import FileRequestHandlerFactory
from contextmonkey.tracelayer.handlers.model.ModelRequestHandlerFactory import ModelRequestHandlerFactory
from contextmonkey.tracelayer.handlers.database.DatabaseRequestHandlerFactory import DatabaseRequestHandlerFactory
from contextmonkey.ContextMonkeyLogger import tracelayer

class DataSourceHandler(object):
    """Provide methods to fetch traces from file, model, and database."""

    protocol = None
    dstype = {'file':'File', 'database':'Database', 'model':'Model'}

    datasourcehandlerconnection = None
    # Naming Convention  'contextmonkey.tracelayer.{_datasourcetype}RequestHandler

    def __init__(self, datasourcetype,**kwargs):
        """Initialize appropriate source handler factory."""
        self.protocol = self.dstype[datasourcetype]
        self.kwargs = kwargs
        module_ = importlib.import_module("contextmonkey.tracelayer.handlers.%s.%sRequestHandlerFactory" % (self.protocol.lower(),self.protocol))
        class_ = getattr(module_, "%sRequestHandlerFactory" % (self.protocol))
        self.datasourcehandlerconnection = class_(**self.kwargs)
        self.datasourcehandlerconnection.build()

    def executeFetch(self, uuid, modality):
        """Forward trace fetch request to appropriate source handler factory."""
        if self.datasourcehandlerconnection is not None:
            d = Deferred()
            d.addCallback(self.datasourcehandlerconnection.executeFetch, modality)
            d.callback(uuid)
            tracelayer.log("DATASOURCEHANDLER-executeFetch-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
            return d
        else:
            raise SystemError("Handler connection not initialized")

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

"""Generates traces and reads traces from the file - Two phase."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import time
import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../../../../' )

import traceback
import importlib

from subprocess import call
from subprocess import Popen, PIPE
from collections import namedtuple
from twisted.internet.defer import Deferred
from twisted.internet import reactor
from twisted.web.client import downloadPage
from twisted.internet.ssl import ClientContextFactory
from twisted.internet import ssl

from ModelRequestHandler import ModelRequestHandler
from contextmonkey.ContextMonkeyLogger import tracelayer

def runpipes(cmd):
    """Run command to generate a trace file using a model."""
    if '|' in cmd:
        cmdlist = cmd.split('|')
    else:
        cmdlist = [cmd]
    p = {}
    index = 0
    for command in cmdlist:
        if index == 0:
            p[index]=Popen(command,stdin=None, stdout=PIPE, stderr=PIPE, shell=True) 
        else:
            p[index]=Popen(command,stdin=p[index-1].stdout, stdout=PIPE, stderr=PIPE, shell=True)
        index = index + 1
    (output, err) = p[index-1].communicate()
    exit_code = p[0].wait()

class TwoPhaseModelRequestHandler(ModelRequestHandler):
    """Provide methods to obtain traces from a model in two phases."""

    def __init__(self):
        """Initialize trace file connection."""
        self.datasourcehandlerconnection=None
        
    def failure(self, reason):
        """Handle trace file generation and trace read failure."""
        pass

    def executeFetch(self,uuid, modality):
        """Generate traces and load appropriate filehandler to read a trace file in the cache."""
        try:
            if self.datasourcehandlerconnection is None:
                self.generateScenario(uuid, modality)
                module_= importlib.import_module("contextmonkey.tracelayer.handlers.file.FileRequestHandlerFactory")
                class_ = getattr(module_, "FileRequestHandlerFactory")
                self.datasourcehandlerconnection = class_(**{"tracefile":modality.datasource.filepath,"formattype":modality.datasource.datasourceformat})
                self.datasourcehandlerconnection.build()
            d = Deferred()
            d.addCallback(self.datasourcehandlerconnection.executeFetch, modality)
            d.callback(uuid)
            tracelayer.log("TWOPHASEMODELREQUESTHANDLER-executeFetch-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
            return d
        except Exception as e:
            traceback.print_exc() 
                  
    def generateScenario(self,uuid, modality):
        """Generate trace file from a given scenario using the command."""
        runpipes(modality.datasource.command)

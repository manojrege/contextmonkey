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

"""Context Layer APIs to other layers. All methods are static."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
import os

sys.path.append(os.path.dirname(__file__) + '/../../' )

import importlib
import time

from twisted.internet.defer import Deferred
from twisted.internet import reactor
from twisted.python import log

from contextmonkey.ContextMonkeyGlobal import modalitylist
from contextmonkey.ContextMonkeyLogger import context
from contextmonkey.libs import util
    
def receiveValue(result, uuid, modality):
    """Put the received trace in the queue."""
    modalitylist[modality.name].value=result
    sim=importlib.import_module('contextmonkey.ContextSimulation')
    mag=importlib.import_module('contextmonkey.contextlayer.ContextManagerInstance')
    index = util.listindexmatching(mag.cm.physicalcontextmodality,modality.name,"name")
    mag.cm.physicalcontextmodalityqueues.enqueue(index,modalitylist[modality.name],1)
    context.log("ContextLayerAPI-receiveValue-timestamp:",str("%0.20f" % time.time())+" "+str(uuid)) 
    return
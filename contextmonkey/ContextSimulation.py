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

"""Context Simulation APIs. exposed to the developer."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright 2015"
__credits__ = ["Manoj R. Rege"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append('../')

import traceback

from twisted.internet import reactor
from networkx import nodes

from contextmonkey.tracelayer.DataSourceManagerInstance import dm
from contextmonkey.feedlayer.EmulatorManagerInstance import em
from contextmonkey.contextmodel.ContextTrace import PhysicalContextModality, VirtualContextModality
from contextmonkey.ContextMonkeyExceptions import DependencyError
from contextmonkey.ContextMonkeyGlobal import modalitylist
from contextmonkey.contextmodel.ContextTrace import ContextGraph

cg = ContextGraph()
dm = dm
em = em

def createContextSimulation():
    """Create a simulation."""
    pass

def addModality(modalityset):
    """Add modalities to the simulation."""
    for modality in modalityset:
        modalitylist[modality.name] = modality
                 
def createContextGraph(*args,**kwargs):
    """Create a context graph."""
    cg.createContextGraph(*args,**kwargs)

def addEmulator(emulator):
    """Add an emulator to the context simulation."""
    em.loadEmulatorConnectionHandler(emulator)
    
def runTime(time):
    """Define simulation run duration."""
    global simTime
    try:
        if time <= 0:
            raise SystemError("Simulation time cannot be 0")
        simTime=time
        print simTime
    except Exception as e:
        traceback.print_exc()
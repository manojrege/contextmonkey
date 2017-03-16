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

"""Example: Simulating Mobility with Accelerometer."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import contextmonkey.ContextMonkeyEngine as engine 
import contextmonkey.ContextSimulation as sim

from contextmonkey.contextmodel.DataSource import Model
from contextmonkey.contextmodel.DataSource import TraceFile
from contextmonkey.contextmodel.ContextTrace import PhysicalContextModality
from contextmonkey.contextmodel.Emulator import Emulator

#Modalities and data-sources
dsnet = Model(queryparameterlist=['lat','lng','distance','network_type','apikey'], 
              modeltype = 'twophase', 
              datasourceformat = "csv", 
              path='',
              command='/Users/manoj/Downloads/bonnmotion-3.0.1/bin/bm IntervalFormat -l 2 -s -f /Users/manoj/Downloads/bonnmotion-3.0.1/bin/randomwaypoint',
              datasourcetype="model",
              filepath='/Users/manoj/Downloads/bonnmotion-3.0.1/bin/randomwaypoint.if')
                       
locmod = PhysicalContextModality(name = 'Gps', 
                                 samplingrate = 2, 
                                 feedrate = 1, 
                                 datasource = dsnet, 
                                 tracevector=['accuracy', 'altitude', 'bearing', 'latitude', 'longitude', 'status'],
                                 traceprocessing="BonnMotionModify")

dsac = TraceFile(queryparameterlist=None,
				 datasourceid = 1,
				 datasourcetype = 'file', 
				 datasourceformat = 'csv', 
				 filepath = '/Users/manoj/Downloads/accelerometer-1/trace1/Measurer.csv', 
				 header = 'true',
				 length=8)

acmod = PhysicalContextModality(name = 'acceleration', 
                                samplingrate = 100, 
                                feedrate = 100, 
                                datasource = dsac, 
                                tracevector=['x','y','z'], 
                                traceprocessing="JiitAccelerometer")

#Create Context Model

sim.addModality([locmod])

sim.createContextGraph(locmod.name)

#Add emulator
emulator = Emulator('Android', {'addr': '127.0.0.1:5554'})
sim.addEmulator(emulator)

#Simulation Duration in seconds
sim.runTime(100)

# Start simulation
engine.start()


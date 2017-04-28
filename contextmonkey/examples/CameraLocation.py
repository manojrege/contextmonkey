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

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../../')

import contextmonkey.ContextMonkeyEngine as engine 
import contextmonkey.ContextSimulation as sim

from contextmonkey.contextmodel.DataSource import Database
from contextmonkey.contextmodel.DataSource import TraceFile
from contextmonkey.contextmodel.ContextTrace import PhysicalContextModality
from contextmonkey.contextmodel.Emulator import Emulator

import random 

#Download it from CRAWDAD
tracefilepath="TRACEFILE FILE PATH GOES HERE"

sampling_period=20

#YOUR API KEY
API_KEY="################"

ds = Database(queryparameterlist=['lat','lng','distance','network_type','apikey'], keymapping = dict(lat='latitude',lng='longitude'),datasourceid=2, datasourcetype="database", datasourceformat = "json", url='http://api.opensignal.com/v2/networkstats.json', queryparameters=dict(lat = "37.7907",lng = "-122.4058",distance = "20",network_type = "3",apikey = API_KEY))
netmod = PhysicalContextModality(name = 'network', samplingrate = 1.0/sampling_period, feedrate = 1.0/sampling_period, datasource = ds,traceprocessing="OpenSignalNetworkModify", tracevector=['name', 'rssi', 'averageRssiDb', 'downloadSpeed', 'uploadSpeed', 'pingTime'])

dsloc = TraceFile(queryparameterlist=None,datasourceid = 1,datasourcetype = 'file', datasourceformat = 'text', filepath=tracefilepath, header = 'true',length=100)
locmod = PhysicalContextModality(name = 'gps', samplingrate = 1.0/sampling_period, feedrate = 1.0/sampling_period, datasource = dsloc, tracevector=['accuracy', 'altitude', 'bearing', 'latitude', 'longitude', 'status'],traceprocessing="CabspottingLocationModify")
locmod.value = {'latitude':random.random()*100,'longitude':random.random()*100,'altitude':random.random()*100}

dsmf = TraceFile(queryparameterlist=None,datasourceid = 1,datasourcetype = 'file', datasourceformat = 'text', filepath = tracefilepath, header = 'true',length=8703)
accelmod = PhysicalContextModality(name = 'acceleration', samplingrate = 100, feedrate = 100, datasource = dsmf, tracevector=['x','y','z'], traceprocessing="CompassModifyText")

dbcam = Database(queryparameterlist=['size','location','heading','pitch','key'],keymapping=dict(size="600x400",location="latitude,longitude",heading="151.78",pitch="-0.76"), datasourcetype="database",datasourceformat="binary",url='https://maps.googleapis.com/maps/api/streetview',queryparameters=dict(size = "640x480",location = "46.414382,10.013988",heading = "151.78",pitch = "-0.76"),extension='jpg',fetchtype='secure')
cammod=PhysicalContextModality(name='camera',samplingrate=0.5,feedrate=0.5,datasource=dbcam,tracevector= ['image','original','encoded','camera_type'],traceprocessing="StreetViewModify")

sim.createContextGraph(locmod.name,cammod.name, netmod.name, e0=(locmod.name,cammod.name), e1=(locmod.name,netmod.name))
   
#Add emulator
emulator = Emulator('Android', {'addr': '127.0.0.1:5554'})
sim.addEmulator(emulator)


#Simulation Duration in seconds
sim.runTime(100)

# Start simulation
engine.start()



This is a project to develop a framework for context generation in mobile emulators for testing and evaluation of 
mobile apps. ContextMonkey is a Python based framework that simulates context scenarios by leveraging traces from 
various sources such as trace databases (like Google StreetView, OpenSignal Maps), models & libraries (like Bonnmotion and SUMO), 
and trace files in an interdependent and correlated manner. ContextMonkey has integrated support for context generation 
in stock based Android and Genymotion emulator. The framework is intended for experimental use only.

CONTACT
----------------------

Manoj R. Rege <rege@tkn.tu-berlin.de>
    
    
ContextMonkey OVERVIEW
----------------------

A brief overview of what this code does can be found in the paper

https://goo.gl/motEqE

A detailed version is available at

https://goo.gl/oIaVrY


LICENSE
----------------------

Copyright (c) 2017, Technische Universitaet Berlin
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
- Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
- Neither the name of the Technische Universitaet Berlin nor the names
of its contributors may be used to endorse or promote products derived
from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

EXAMPLE
----------------------

The below example generates a location dependent camera context simulation in the Stock Android Emulator::

   #!/usr/bin/env python
   
   import contextmonkey.ContextMonkeyEngine as engine
   import contextmonkey.ContextSimulation as sim
   from contextmonkey.contextmodel.Datasource import Database
   from contextmonkey.contextmodel.DataSource import Tracefile
   from contextmonkey.Contextmodel import PhysicalContextModality
   from contextmonkey.Emulator import Emulator
   
   #Define modalities and data-sources

   dsnet = Database(queryparameterlist=['lat','lng','distance','network_type','apikey'], keymapping = dict(lat='latitude',lng='longitude'), datasourceformat = "json", url='http://api.opensignal.com/v2/networkstats.json', queryparameters=dict(lat = "37.7907",lng = "-122.4058",distance = "20",network_type = "3",apikey = "@@@@@@@@@"),fetchtype="HTTP")
   netmod = PhysicalContextModality(name = 'network', samplingrate = 0.01, feedrate = 0.01, datasource = dsnet, traceprocessing="OpenSignalNetworkModify", tracevector=['name', 'rssi', 'averageRssiDb', 'downloadSpeed', 'uploadSpeed', 'pingTime'])

   tfloc = TraceFile(datasourcetype = 'file', datasourceformat = 'text', path=tracefilepath, header = 'true',length=100)
   locmod = PhysicalContextModality(name = 'gps', samplingrate = 0.01, feedrate = 0.01, datasource = tfloc, tracevector=['accuracy', 'altitude', 'bearing', 'latitude', 'longitude', 'status'],traceprocessing="LocationModify")

   dbcam = Database(queryparameterlist=['size','location','heading','pitch','key'],keymapping=dict(size="600x400",location="latitude,longitude",heading="151.78",pitch="-0.76"),  datasourcetype="database",datasourceformat="binary",url='https://maps.googleapis.com/maps/api/streetview',queryparameters=dict(size = "640x480",location = "46.414382,10.013988",heading = "151.78",pitch = "-0.76"),extension='jpg',fetchtype="HTTPS")
   cammod= PhysicalContextModality(name='camera',samplingrate=0.01,feedrate=0.01,datasource=dbcam,tracevector= ['image','original','encoded','camera_type'],traceprocessing="StreetViewModify")

   #Create a Context Model

   sim.addModality([cammod,locmod,nwmod])
   sim.createContextGraph(locmod.name,netmod.name,cammod.name e0=(locmod.name,netmod.name),e1=(locmod.name,camod.name))

   #Add an emulator
   
   emulator = Emulator('Android',{'addr':'127.0.0.1:5554'})
   sim.addEmulator(emulator)

   # Start the simulation
   
   sim.runTime(600)
   engine.start()
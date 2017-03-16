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

"""Context manager operations in the context layer."""

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

import time
import traceback
import uuid

from twisted.internet.defer import Deferred
from twisted.internet import reactor
from twisted.python import log

from contextmonkey.ContextSimulation import dm
from contextmonkey.ContextSimulation import cg
from contextmonkey.ContextMonkeyExceptions import ContextModalityError
from contextmonkey.contextmodel.ContextTrace import ContextGraph
from contextmonkey.contextmodel.ContextTrace import PhysicalContextModality
from contextmonkey.contextmodel.ContextTrace import VirtualContextModality
from contextmonkey.contextmodel.DataSource import Database
from contextmonkey.contextmodel.DataSource import TraceFile
from contextmonkey.contextlayer.ContextQueues import ContextQueues
from contextmonkey.contextlayer.ContextModalityTimer import ContextModalityTimer
from contextmonkey.libs import util
from contextmonkey.ContextMonkeyGlobal import modalitylist
from contextmonkey.tracelayer.handlers.DataSourceHandler import DataSourceHandler

from contextmonkey.protofiles import sensor_pb2
from contextmonkey.ContextMonkeyLogger import context
import contextmonkey.ContextSimulation as sim

t1 = time.time()

class ContextManager(object):
    """Implementation of ContextManager."""
    
    global dm
    global t1
    
    def __init__(self):
        """Initialize list of all physical and virtual context modalities and data queues."""    
        self.physicalcontextmodality = []
        self.physicalcontextmodalityqueues = ContextQueues()
        self.physicalcontextmodalitydependency = []
        self.virtualcontextmodality = []
        self.virtualcontextmodalitydependency = []
        self.tracetimer = []
        self.feedtimer = []
     
    def add_physical_contextModality(self, modality, dependencygraph=None):     
        """Add physical context modality to the existing list of modalities."""
        try:
            self.physicalcontextmodality.append(modality)
            self.physicalcontextmodalitydependency.append(dependencygraph)
            self.physicalcontextmodalityqueues.add_a_queue(0)
            self.tracetimer.append(ContextModalityTimer(modality.name,1.0/modality.samplingrate))
            self.feedtimer.append(ContextModalityTimer(modality.name,1.0/modality.feedrate)) 
            return True
        except:
            context.log(traceback.print_exc())
            raise(ContextModalityError, "Could not add PhysicalContextModality")


    def add_virtual_contextModality(self, modality, dependencygraph):
        """Add virtual context modality to the existing list of modalities."""
        try:
            self.virtualcontextmodality.append(modality)
            self.virtualcontextmodalitydependency.append(depdendencygraph.getContextDependency(modality.modalityname))
            for dependency in self.virtualcontextmodalitydepedency[-1]:
                itr=listindexmatching(self.physicalcontextmodality,dependency, "name")
                self.physicalcontextmodality[itr].virtualdependence=+1
                self.tracetimer.append(ContextModalityTimer(modality.name, 1.0/modality.samplingrate))
                self.feedtimer.append(ContextModalityTimer(modality.name, 1.0/modality.feedrate))
            return True
        except:
            raise(ContextDepdencyError,"Could not add Virtual context modality")

    def delete_physical_contextModality(self, modality):
        """Delete only the physical context modality from existing list."""
        index = listindexmatching(self.physicalcontextmodality,modality.name,"name")   
        if index is None:
            raise(ContextModalityError, "No such physical context modality exists") 
        #Use strict checking - If virtual dependency exists don't delete
        elif check_dependency(self.physicalcontextmodality[index]): 
            raise(ContextModalityError, "Failed to remove Physical ContextModality- Existing physical context dependency")        
        elif check_depdency(modality,self.virtualcontextmodality[index]):
            raise(ContextModalityError, "Failed to remove Physical ContextModality- Existing virtual context dependency")
        else:
            del self.physicalcontextmodality[index]
            del self.physicalcontextmodalitydependency[index]
            del self.physicalcontextmodalityqueues[index]
            del self.tracetimer[listindexmatching(self.physicalcontextmodality, modality.name,"contextmodalityid")]     
        return True

    def delete_virtual_contextModality(self, modality):
        """Delete a virtual context modality from existing list."""
        index = listindexmatching(self.virtualcontextmodality, modality.name, "name")
        if index is None:
            raise(ContextModalityError, "No such virtual context modality exists")
        else:
            del self.virtualcontextmodality[index]
            for dependency in self.virtualcontextmodalitydependency[index]:
                itr=listindexmatching(self.physicalcontextmodality,dependency,"name")
                self.physicalcontextmodality[itr].virtualdependence= self.physicalcontextmodality[itr].virtualdependence - 1    
            del self.virtualcontextmodalitydependency[index]
            del self.tracetimer[listindexmatching(self.virtualcontextmodality,modality.name,"contextmodalityid")]   
            return
    
    #TODO: Implement cascade delete operation for physical context modality
    def cascade_delete_physical_context_modality(self,modality):
        """Delete physical context modalities including all dependencies."""
        pass
        
    #TODO: Implement cascade delete operation for virtual context modality  
    def cascade_delete_virtual_context_modality(self,modality):
        """Delete virtual context modalities including all dependencies."""
        pass

    def getPhysicaltracevalue(self,modality):
        """Callback associated with trace timer for a physical context modality."""
        global modalitylist
        for depdendency in cg.getDependency(modality[0].name):
            modalitylist[depdendency].value      
        d = Deferred()
        modality=self.construct_queryparameters(modality[0])
        d.addCallback(dm.getContextTraceValue, modality) 
        id = uuid.uuid4()
        d.callback(id)
        context.log("CONTEXTMANAGER-getPhysicaltracevalue-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(id))
        return
        
	#FIXME: Catch index None exception
    def start_physical_contextmodality_simulation(self, modality):
        """Start TimerService for a given physical modality."""
        try:
            index = util.listindexmatching(self.physicalcontextmodality,modality.name,"name")
            print str(index)
            # TODO: API function call from the feed layer"
            self.tracetimer[index].start(self.getPhysicaltracevalue, modality)
            self.feedtimer[index].start(self.feedvalue,modality)
        except Exception:
            context.log("CONTEXTMANAGER-start_physical_contextmodality_simulation",traceback.format_exc())
            raise(ContextModalityError, "Failed to start the timer for context"
                  "modality")
    
    #FIXME: Catch index None exception   
    def stop_physical_contextmodality_simulation(self,modality=None):
        """Stop Timerservice for a given physical modality."""
        try:
            index=listindexmatching(self.physicalcontextmodality,modality.name,"contextmodalityid")
            self.tracetimer[index].stop()
        except:
            raise(ContextModalityError,"Failed to stop context modality timer")
    
    #FIXME: Catch index None exception
    def start_virtual_contextmodality_simulation(self,modality,callback,**kwargs):
        """Start TimerService for a given virtual modality."""
        try:
            index=listindexmatching(self.virtualcontextmodality,modality.name,"contextmodalityid")
            self.tracetimer[index].start(callback, kwargs)
        except:
            raise(ContextModalityError,"Failed to start the timer for context modality")
    
    #FIXME: Catch index None exception        
    def stop_virtual_contextmodality_simulation(self,modality=None):
        """Stop Timerservice for a given virtual modality."""
        try:
            index=listindexmatching(self.physicalcontextmodality,modality.name,"contextmodalityid")
            self.tracetimer[index].stop()
        except:
            raise(ContextModalityError,"Failed to stop context modality timer")

    #NOTE: rate of a virtual sensor = min (rate of dependencies, rate of virtual function)
    #FIXME: Exceptions Index None
    def verify_virtual_computation_rate(self,modalityrate,dependency):
        """Estimate the frequency of the virtual computation."""
        temprate=[rate]
        for modality in dependency:
            index=listindexmatching(self.physicalcontextmodality,modality,"name")
            temprate.append(self.physicalcontextmodality[index].rate)
        return min(temprate)
    
    #NOTE - Callback associated with trace timer for a virtual context modality
    def virtualtracevalue(self, index):
       """Callback associated with trace timer for a virtual context modality."""
       #TODO: From protobuf to"
       d=Deferred()
       d.addCallback(self.physicalcontextmodalityqueues.getitem)
       d.addCallback(compute)
       d.addCallback(self.physicalcontextmodalityqueues[index].enqueue)
       d.callback(1)
    
    def feedvalue(self,modality):
        """Dequeue the trace send it to the feed layer."""
        try:
            d=Deferred()
            index = util.listindexmatching(self.physicalcontextmodality,modality[0].name,"name")
            d.addCallback(self.physicalcontextmodalityqueues.getitem)
            d.addCallback(sim.em.setModalityValue)
            d.callback(index)
        except Exception as e:
            traceback.print_exc()

    def construct_queryparameters(self, modality):
        """Construct query parameters for the trace request."""
        # Create a single dictionary of all current vales of modality depdencies
        global modalitylist
        result = {}
        index = util.listindexmatching(self.physicalcontextmodality,modality.name,"name")
        for depmod in self.physicalcontextmodalitydependency[index]:
            print(depmod)
            result.update(modalitylist[depmod].value)
            #Set values 
            #Main assumption is that the key values across all modalities are consistent
            context.log("CONTEXTMANAGER-CONSTRUCT_QUERYPARAMETERS",str(modalitylist[modality.name].datasource.queryparameterlist))
            try:
                for k in modalitylist[modality.name].datasource.queryparameterlist:
                    try:
                        retrieval_key = modalitylist[modality.name].datasource.keymapping[k]
                        individual_keys=retrieval_key.split(',')
                        temp=""
                        for i in individual_keys:
                            try:
                                temp+=str(result[i])+","
                                context.log("CONTEXTMANAGER-CONSTRUCT_QUERYPARAMETERS",str(result[i]))
                            except:
                                modalitylist[modality.name].datasource.queryparameters[k]=modalitylist[modality.name].datasource.keymapping[k]
                                break
                        if not temp[:-1] == "":
                            modalitylist[modality.name].datasource.queryparameters[k]=temp[:-1]
                    except Exception:
                        context.log("CONTEXTMANAGER-CONSTRUCT_QUERYPARAMETERS","No such key in the keymapping")
            except:
                context.log("CONTEXTMANAGER-CONSTRUCT_2QUERYPARAMETERS",str(traceback.print_exc()))
                #modalitylist[modality.name].datasource.queryparameters[k] = None

        context.log("CONTEXTMANAGER-CONSTRUCT_1QUERYPARAMETERS",str(modalitylist[modality.name].datasource.queryparameters))
        return modalitylist[modality.name]
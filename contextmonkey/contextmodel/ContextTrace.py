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

"""ContextMonkey data model definitions."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import uuid
import networkx as nx

from threading import Timer
from abc import ABCMeta, abstractmethod

from ContextMonkeyExceptions import DependencyError

class ContextModality():
    """Abstract class defining Context Modality."""
    
    __metaclass__ = ABCMeta

    def __init__(self, name, samplingrate, feedrate, datasource=None, dependency=None, tracevector=None, units=None, traceprocessing=None, modalityobject = None, value=None):
        """Initialize."""
        self.name = name
        self.modalityid = uuid.uuid4()
        self.samplingrate = samplingrate
        self.feedrate = feedrate
        self.datasource = datasource
        self.dependency = dependency
        self.tracevector = tracevector
        self.units = units
        self.traceprocessing = traceprocessing
        self.modalityobject = modalityobject
        self.value= value
        

class PhysicalContextModality(ContextModality):
    """Class representing physical context."""
    
    def __init__(self, name, samplingrate, feedrate, datasource, tracevector, dependency=None, units=None, traceprocessing=None):
        """Initialize."""
        super(PhysicalContextModality, self).__init__(name=name, samplingrate=samplingrate, feedrate=feedrate, datasource=datasource, tracevector=tracevector, dependency=dependency, units=units, traceprocessing=traceprocessing)
        self.virtualdependence = 0

class VirtualContextModality(ContextModality):
    """Class representing virtual context."""
    
    def __init__(self, name, samplingrate, feedrate, dependency, computation, tracevector):
        """Initialize."""
        super(VirtualContextModality, self).__init__(name, samplingrate=samplingrate, feedrate=feedrate, dependency=dependency, tracevector= tracevector)
        self.function = computation

class VirtualComputation(object):
    """Class representing Virtual Computation."""
    
    def __init__(self, librarypath, command, cmdlineparameters=None):
        """Initialize."""
        self.librarypath = librarypath
        self.command = command
        self.cmdlineparameters = cmdlineparameters

class ContextGraph(object):
    """Class representing context modality dependencies, defined using a global DAG."""
    
    def __init__(self):
        """Instantiate a context graph."""
        self.graph = nx.DiGraph()

    def createContextGraph(self, *args, **kwargs):
        """Create context dependency graph."""
        self.graph.add_nodes_from(args)
        for key, value in kwargs.items():
            self.graph.add_edge(value[0], value[1])
        if not nx.is_directed_acyclic_graph(self.graph):
            self.graph = nx.DiGraph()
            raise DependencyError("Circular dependencies in Context depedency graph")
        return True

    def get_connected_components(self):
        """Return connected components of graph."""
        return nx.weakly_connected_components(self.graph)
        
    def get_graph_nodes(self):
        """Return the nodes in the context graph."""
        return self.graph.nodes()

    def getbreadthfirstsearch(self):
        """Perform a Breadth First Search Traversal over DAG from source and return the nodes sorted."""    
        return self.graph.bfs_predecessors(self.graph)

    def getDependency(self, node):
        """Return predecessor nodes in the context graph."""
        return self.graph.predecessors(node)

    def getdepthfirstsearch(self):
        """Perform Depth First Search Traversal over DAG from source and return the nodes sorted."""
        dependencylist = []
        return self.get_connected_components()

    #TODO: Implement this method - it provides list of dependencies to ContextManager to fetch the necessary 
    #values from Feed Layer 
    def getContextDependency(self, name):
        """Return list of context dependencies for a given context."""
        pass
        
    #TODO: Implement this method - it returns True if the given context modality is used for some virtual computation
    #function
    def check_virtual_dependency(self, modality):
        """Verify if a modality is used in virtual computation."""
        pass
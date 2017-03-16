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

"""Data source manager operations in the trace layer."""

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

import json
import shutil
import importlib
import time

from twisted.internet.defer import Deferred
from zope.interface import implementer

from contextmonkey.tracelayer.interfaces.ITraceSource import ITraceSource
from contextmonkey.contextlayer.ContextLayerAPI import receiveValue
from contextmonkey.tracelayer.handlers.DataSourceHandler import DataSourceHandler
from contextmonkey.ContextMonkeyGlobal import modalitylist
from contextmonkey.ContextMonkeyLogger import tracelayer
from contextmonkey.tracelayer.interfaces.ITraceLayer import ITraceLayerAPI
from contextmonkey.tracelayer.handlers.DataSourceHandler import DataSourceHandler
from contextmonkey.ContextMonkeyExceptions import *
from contextmonkey.tracelayer.TraceFormatManager import TraceFormatManager

@implementer(ITraceLayerAPI)
class DataSourceManager(object):
    """Provide methods to orchestrate trace fetching from different data-sources - File, Model, Database.""" 

    databasehandlers = {}
    filehandlers = {}
    modelhandlers = {}
    traceformatmanager = TraceFormatManager()
    
    def circular_increment (self,current_iterator, max_length):
        """Increment file iterator."""
        if current_iterator > max_length:
            return 0  
        return current_iterator+1


    def __init__(self):
        """'Initialize."""
        pass
    
    def construct_queryparameters(self, queryparameterlist, paramvalues):
        """Construct the trace fetching request based on query-parameters."""
        queryparameters={}
        for key,value in zip(queryparameterlist, paramvalues):
            queryparameters[key]=value
        return queryparameters

    def executeFetch(self, uuid, modality):
        """Send trace fetching request to the appropriate source handler."""
        global modalitylist
        #########DATABASE##########
        d = Deferred()
        if modality.datasource.datasourcetype == 'database':
            try:
                print modality.name+"type found"
                d.addCallback(self.databasehandlers[currentmodality.name].executeFetch,modality=modality)
                tracelayer.log("DATASOURCEMANAGER-executeFetch-database-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
            except Exception as e:
                self.databasehandlers[modality.name]= DataSourceHandler('database', fetchtype=modality.datasource.fetchtype, formattype=modality.datasource.datasourceformat)
                d.addCallback(self.databasehandlers[modality.name].executeFetch,modality=modality)
                tracelayer.log("DATASOURCEMANAGER-executeFetch-database-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
        
        #########FILE##########
        elif modality.datasource.datasourcetype == 'file':
            modality.datasource.fileiterator = self.circular_increment(modality.datasource.fileiterator,modality.datasource.length)
            
            try:
                d.addCallback(self.filehandlers[modality.name].executeFetch, modality= modality)
                tracelayer.log("DATASOURCEMANAGER-executeFetch-file-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
            except Exception as e:
                self.filehandlers[modality.name] = DataSourceHandler('file', tracefile= modality.datasource.filepath, formattype=modality.datasource.datasourceformat)
                tracelayer.log("DATASOURCEMANAGER-executeFetch-file-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
                d.addCallback(self.filehandlers[modality.name].executeFetch, modality= modality)
                
        #########MODEL##########
        elif modality.datasource.datasourcetype == 'model':
            modality.datasource.fileiterator = self.circular_increment(modality.datasource.fileiterator,10)
            try:
                d.addCallback(self.modelhandlers[modality.name].executeFetch, modality= modality)
                tracelayer.log("DATASOURCEMANAGER-executeFetch-model-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
            except Exception as e:
                self.modelhandlers[modality.name] = DataSourceHandler('model', modeltype=modality.datasource.modeltype, formattype=modality.datasource.datasourceformat)
                tracelayer.log("DATASOURCEMANAGER-executeFetch-model-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
                d.addCallback(self.modelhandlers[modality.name].executeFetch, modality= modality)        
        else:
            pass
        d.callback(uuid)
        return uuid
    
    def handletracefailure(self, reason):
        """Handle trace fetching failures."""
        print reason
        tracelayer.log("DATASOURCEMANAGER TRACEFAILURE",reason)

    def getContextTraceValue(self, uuid, modality):
        """Provide API to the context layer to get trace."""
        d = Deferred()
        d.addCallback(self.executeFetch,modality)
        d.callback(uuid)
        tracelayer.log("DATASOURCEMANAGER-getContextTraceValue-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
        return d

    @staticmethod
    def filter_data(tracedata, uuid, modality):
        """Filter & process, and forward trace for format conversion."""
        module_ = importlib.import_module("contextmonkey.tracelayer.processingfilters.%s" % (modality.traceprocessing))
        class_ = getattr(module_, "%s" % modality.traceprocessing)
        ostm = class_()
        d = Deferred()
        d.addCallback(ostm.filterTrace,uuid)
        d.addErrback(ostm.handlefailure)
        d.addCallback(ostm.processTrace,uuid)
        d.addCallback(DataSourceManager.traceformatmanager.toProtobuf,modality)
        d.addCallback(receiveValue,uuid, modality)
        d.callback(tracedata)
        tracelayer.log("DataSourceManager-filterData-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid)) 
        return d

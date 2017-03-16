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

"""Convert traces from Protobuf to emulator data format."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import importlib
import inspect

from zope.interface import implementer
from contextmonkey.interfaces.IFormat import IFormat

@implementer(IFormat)
class FeedFormatManager(object):
    """Implementation of IFormat interface for converting trace from protobuf format."""
    
    def __init__(self):
        """Initialize."""
        pass
       
    def fromProtobuf(self, modality):
        """Method converting from protobuf to dict."""
        classname = self.modality_based_class_importer(modality)
        obj = classname()
        obj.ParseFromString(modality.value)
        attrlist=self.get_attribute_list(classname)
        tracevector={}
        for attr in attrlist:
            tracevector[attr]=getattr(obj,attr)
        return tracevector
        
    #Dynamically load the protobuf definition file based on modality
    def modality_based_class_importer(self,modality):
        """Method for importing the class based on the modality."""
        #TODO: Provide dynamic path to the folder
        module = importlib.import_module("protofiles.sensor_pb2")
        classtype = getattr(module, modality.name)
        return classtype
    
    def get_attribute_list(self,classname):
        """Return all attributes of a class having property type."""
        attributes = inspect.getmembers(classname, lambda a:not(inspect.isroutine(a)))
        return [a[0] for a in attributes if(isinstance(a[-1],property))]

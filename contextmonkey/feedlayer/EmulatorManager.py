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


''' Implements ContextMonkey EmulatorManager that loads emulator specfic handler to communicate
    with emulator specific api'''

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
import os
sys.path.append(os.path.dirname(__file__)+'/../../')
import time

from contextmonkey.contextmodel.Emulator import Emulator
from contextmonkey.feedlayer.FeedFormatManager import FeedFormatManager
from contextmonkey.ContextMonkeyLogger import feed
from contextmonkey.ContextMonkeyExceptions import DisconnectedModalityError
import importlib
import traceback


class EmulatorManager(object):

    def __init__(self,emulator = None):
        ''' Emulator Manager constructor'''
        self.emulator = emulator
        self.emulatorconnection = None
        self.feedformatmanager = FeedFormatManager()
	
    def loadEmulatorConnectionHandler(self, emulator):
        '''Loads appropriate emulator connection handler'''
        if not isinstance(emulator, Emulator):
            raise TypeError('emulator provided in argument must be instance of class Emulator')
        self.emulator = emulator
        module_ = importlib.import_module("contextmonkey.feedlayer.emulators.%s.%sConnection" % (self.emulator.emulatorname.lower(), self.emulator.emulatorname))
        class_ = getattr(module_, "%sConnection" % self.emulator.emulatorname)
        self.emulatorconnection = class_(self.emulator)
        self.emulatorconnection.registerEmulator(self.emulator)
        
        '''except Exception as ex:
            #raise ContextMonkeyEmulatorLoadException("Failed to load emulator connection handler")
            print ex
            print type(ex)
            print sys.exc_info()[2]'''

    def setModalityValue(self, modality):
        '''issues commands to set a specific sensor to a specific value 
        connects to a sensor, if no connection is present
        '''
        modality.value=dict(self.feedformatmanager.fromProtobuf(modality))
        if self.emulator is None:
            raise SystemError('You must first register an emulator with the EmulatorManager!')
        if modality.name in self.emulator.activeSensors:
            try:
                feed.log("EMULATORMANAGER-setModalityValue",str(self.emulator.activeSensors[modality.name]))
                self.emulator.activeSensors[modality.name].sendValue(modality.modalityid,**modality.value)
                feed.log("EmulatorManager-filterData-timestamp:",str("%0.20f" % time.time())+" "+str(modality.modalityid)) 
            except DisconnectedModalityError:
                feed.log("EMULATORMANAGER-setModalityValue",'Sensor %s seems to be disconnected, removing ...' % modality.name)
                self.emulatorconnection.disconnectSensor(modality.name)
            except:
                feed.log("EMULATORMANAGER-setModalityValue",traceback.format_exc())

        else:
            feed.log("EMULATORMANAGER-setModalityValue","Connecting to "+modality.name+".......")
            self.emulatorconnection.connectSensor(modality.name, modality.modalityid, **modality.value)


    def getModalityValue():
       #TODO: Get the modality sensor value from emulator 
       pass

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

"""Read traces from a TEXT trace file."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import sys
import os
sys.path.append(os.path.dirname(__file__) + '../../../../')

import urllib
import linecache
import time 

from twisted.internet.defer import Deferred
from twisted.python.log import err
from twisted.web.client import Agent, readBody
from twisted.internet import reactor
from twisted.web.http_headers import Headers

from contextmonkey.tracelayer.handlers.file.FileRequestHandler import FileRequestHandler
from contextmonkey.tracelayer.handlers.file.ContextMonkeyFileCache import TEXTFileCache
from contextmonkey.tracelayer.DataSourceManager import DataSourceManager
from contextmonkey.ContextMonkeyLogger import tracelayer

class TEXTFileRequestHandler(FileRequestHandler):
    """Provide methods to obtain traces from a TEXT trace file."""

    textfilecache = TEXTFileCache()

    def __init__(self,filename):
        """Add TEXT file to cache."""
        self.textfilecache.addFileToCache(filename)
    
    def failure(self, reason):
        """Handle file read failure."""
        tracelayer.log("TEXTFileRequestHandler-failure-","Request failed "+str(reason))

    def printline(self, line):
        """Print line."""
        print (line)
        print (sys.getsizeof(line))
        return

    def success(self,dummy=None,uuid=None,modality=None):
        """Handle file line read success."""
        d = Deferred()
        d.addCallback(DataSourceManager.filter_data,uuid,modality)
        tracelayer.log("TEXTFileRequestHandler-success-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
        d.callback(dummy)

    def fileread(self,filename,fileiterator):
        """Perform file read based on line number."""
        try:
            line = self.textfilecache.getTrace(filename, iterator=fileiterator)
            return line
        except IOError:
            print ("File not found")
        else:
            #raise ContextMonkeyUnSupportedTraceFormatError
            print ("Error")

    def executeFetch(self,uuid, modality):
        """Handle a trace fetch request."""
        filename = modality.datasource.filepath
        fileiterator = modality.datasource.fileiterator
        d = Deferred()
        d.addCallback(self.fileread,fileiterator)
        d.addErrback(self.failure)
        d.addCallback(self.success,uuid,modality)
        d.callback(filename)
        tracelayer.log("TEXTFileRequestHandler-fileread-timestamp:",str(modality.name)+" "+str("%0.20f" % time.time())+" "+str(uuid))
        return d


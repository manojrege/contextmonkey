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

"""ContextMonkey wide cache containing files for all modalities."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import json
import yaml
import xml.etree.ElementTree as ET

class ContextMonkeyFileCache(object):
    """Generic base class for trace file cache."""
     
    filecache = {}

    def __init__(self):
        """Initialize file cache."""
        pass

    def addFileToCache(self, filename):
        """Put trace file in cache."""
        pass

    def getTrace(self, **params):
        """Read a line from trace file."""
        pass

class TEXTFileCache(ContextMonkeyFileCache):
    """Class for adding TEXT trace file to cache and reading trace line."""
    
    def __init__(self):
        """Initialize TEXT file cache."""
        pass

    def addFileToCache(self, filename):
        """Put TEXT file in cache."""
        if not filename in self.filecache.keys():
            f = open(filename, 'r')
            self.filecache[filename] = f.read().split('\n')
            f.close()

    def getTrace(self, filename, **params):
        """Read line from TEXT file in the cache."""
        #print type(self.filecache[filename])
        try:
            return self.filecache[filename][params['iterator']:params['iterator']+1]
        except:

            return self.filecache[filename][params['iterator']:len(params['iterator'])-1] + self.filecache[filename][0:100 - len(params['iterator']) - params['iterator']] 

class CSVFileCache(ContextMonkeyFileCache):
    """Class for adding CSV trace file to cache and reading trace line."""
    
    def __init__(self):
        """Initialize CSV file cache."""
        pass

    def addFileToCache(self, filename):
        """Put CSV file in cache."""
        if not filename in self.filecache.keys():
            f = open(filename, 'r')
            self.filecache[filename] = f.read().split('\n')
            f.close()

    def getTrace(self, filename, **params):
        """Read line from CSV file in the cache."""
        print (self.filecache[filename][params['iterator']])
        return self.filecache[filename][params['iterator']]


class JSONFileCache(ContextMonkeyFileCache):
    """Class for adding JSON trace file to cache and reading trace line."""

    def __init__(self):
        """Initialize JSON file cache."""
        pass
        
    def addFileToCache(self,filename):
        """Put JSON file in cache."""
        if not filename in self.filecache.keys():
            f = open(filename, 'r')
            self.filecache[filename] = json.loads(f.read())
            f.close()

    def getTrace(self, filename,**params):
        """Read line from JSON file in the cache."""
        return self.filecache[filename][params['iterator']]


class YAMLFileCache(ContextMonkeyFileCache):
    """Class for adding YAML trace file to cache and reading trace line."""

    def __init__(self):
        """Initialize YAML file cache."""
        pass

    def addFileToCache(self, filename):
        """Put YAML file in cache."""
        if not filename in self.filecache.keys():
            f = open(filename,'r')
            self.filecache[filename] = yaml.load(f.read())
            f.close()

    def getTrace(self, filename, **params):
        """Read line from YAML file in the cache."""
        #print(self.filecache[filename][params['iterator']])
        return self.filecache[filename][params['iterator']]


class XMLFileCache(ContextMonkeyFileCache):
    """Class for adding XML trace file to cache and reading trace line."""
    
    def __init__(self):
        """Initialize XML file cache."""
        pass

    def addFileToCache(self, filename):
        """Put XML file in cache."""
        if not filename in self.filecache.keys():
            tree = ET.parse(filename)
            self.filecache[filename] = tree.getroot()

    def getTrace(self, filename, **params):
        """Read line from XML file in the cache."""
        #print "in xml get trace"
        #print self.filecache[filename][params['iterator']]
        #print ET.tostring(self.filecache[filename][params['iterator']],encoding='utf8', method='xml')
        return  ET.tostring(self.filecache[filename][params['iterator']],encoding='utf8', method='xml')

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

"""Protocol for the camera sensor inside Android emulator."""

__author__ = "Manoj R. Rege"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Manoj R. Rege"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import base64
import traceback
import time

from contextmonkey.feedlayer.emulators.android.GeneralSensorProtocol import GeneralSensorProtocol
from contextmonkey.ContextMonkeyLogger import feed

class CameraProtocol(GeneralSensorProtocol):
    """Provide methods for set and get Camera sensor in Android emulator."""
    
    sensorName = 'camera'
    image = 0
    encoded = 0
    original = 0
    camera_type = 'front'

    def __init__(self):
        """Initialize the module for feeding images to the /dev/video0."""
        #try:
            #TODO: Expected to be replaced by proper camera set API of Android Emulator in future version
            #Popen(["ffmpeg -loop 1 -framerate 1/5 -i ../data/cache/*.jpg -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video0 </dev/null >/dev/null 2> ffmpeg.log &"], shell=True)
        #except Exception as e:
        #    print("ffmpeg plugin missing")
            
    def sendData(self, uuid, **values):
        """Issue a set command for camera sensor."""
        try:
            if "image" in values:
                self.image = base64.b64encode(values["image"])
            else:
                raise Exception('Missing parameter "image" for Camera set command')
                return
            if "encoded" in values:
                self.encoded = values["encoded"]
                self.encoded=len(self.image)
            else:
                raise Exception('Missing parameter "encoded" size for Camera set command')
                return
            if "original" in values:
                self.original = values["original"]
                self.original = len(values["image"])
            else:
                raise Exception('Missing parameter "original" size for Camera set command')
                return
            if "camera_type" in values:
                self.camera_type = values["camera_type"]
                self.camera_type='back'
            else:
                self.camera_type = "front"

            command = "camera set {} {} {} {}".format(self.camera_type, self.original,self.encoded, self.image.decode('utf-8'))
            #self.sendLine(command.encode())
            feed.log('CAMERAPROTOCOL-sendData', command)
            feed.log('CAMERAPROTOCOL-sendData',self.sensorName+" timestamp:"+str("%0.20f" % time.time())+" "+str(uuid))

        except:
            feed.log('CAMERAPROTOCOL-sendData',traceback.print_exc())

    def getData(self):
        """Issue a get command for camera sensor."""

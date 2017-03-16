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

"""Protocol for the acceleration sensor inside Android emulator."""

__author__ = "Thomas Hoffmann"
__copyright__ = "Copyright (c) 2017, Technische Universität Berlin"
__credits__ = ["Thomas Hoffmann"]
__version__ = "1.0"
__maintainer__ = "Manoj R. Rege"
__email__ = "rege@tkn.tu-berlin.de"
__status__ = "Prototype"

import time

from contextmonkey.feedlayer.emulators.android.GeneralSensorProtocol import GeneralSensorProtocol
from contextmonkey.ContextMonkeyLogger import feed

class AccelerationProtocol(GeneralSensorProtocol):
    """Provide methods for set and get Acceleration sensor in Android emulator."""

    sensorName = 'acceleration'
    x = 0
    y = 0
    z = 0

    def sendData(self, uuid, **values):
        """Issue a set command for acceleration sensor."""
        if "x" in values:
            self.x = float(values["x"])
        else:
            raise Exception('Missing parameter "x" for network set command')
            return
        if "y" in values:
            self.y = float(values["y"])
        else:
            raise Exception('Missing parameter "downloadSpeed" for network set command')
            return
	
        if "z" in values:
            self.z = float(values["z"])
        else:
            raise Exception('Missing parameter "pingTime" for network set command')
            return
        command = 'sensor set acceleration %.5f:%.5f:%.5f' % (self.x, self.y, self.z)
        self.sendLine(command.encode('UTF-8'))
        feed.log('ACCELERATIONPROTOCOL-sendData', command)
        feed.log('ACCELERATIONPROTOCOL-sendData',self.sensorName+" End Time:"+str("%0.20f" % time.time())+" "+str(uuid))

        def getData(self):
            """Issue a get command for acceleration sensor."""

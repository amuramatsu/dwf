#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 3

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 10/17/2013

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import math
import time

rgdSamples = []
CHANNEL = 0
for i in range(4096):
    rgdSamples.append(math.sin(i / 4096.0 * math.pi))

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device...")
dwf_ao = dwf.DwfAnalogOut()

print("Generating custom waveform...")
dwf_ao.nodeEnableSet(CHANNEL, dwf_ao.NODE_CARRIER, True)
dwf_ao.nodeFunctionSet(CHANNEL, dwf_ao.NODE_CARRIER, dwf_ao.FUNC_CUSTOM)
dwf_ao.nodeDataSet(CHANNEL, dwf_ao.NODE_CARRIER, rgdSamples)
dwf_ao.nodeFrequencySet(CHANNEL, dwf_ao.NODE_CARRIER, 10e3)
dwf_ao.nodeAmplitudeSet(CHANNEL, dwf_ao.NODE_CARRIER, 2.0)
dwf_ao.configure(CHANNEL, True)
print("Generating waveform for 10 seconds...")
time.sleep(10)
print("done.")
dwf_ao.close()

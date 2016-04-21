#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 1/11/2016

   Requires:                       
       Python 2.7, 3.3 or later
       numpy, matplotlib
"""

import dwf
import time
import numpy as np
import matplotlib.pyplot as plt

#constants
HZ_ACQ = 100
N_SAMPLES = 1000

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device")
hdwf = dwf.Dwf()

print("Preparing to read sample...")

print("Generating sine wave...")
dwf_ao = dwf.DwfAnalogOut(hdwf)
dwf_ao.nodeEnableSet(0, dwf_ao.NODE_CARRIER, True)
dwf_ao.nodeFunctionSet(0, dwf_ao.NODE_CARRIER, dwf_ao.FUNC_SINE)
dwf_ao.nodeFrequencySet(0, dwf_ao.NODE_CARRIER, 1.0)
dwf_ao.nodeAmplitudeSet(0, dwf_ao.NODE_CARRIER, 2.0)
dwf_ao.configure(0, True)

#set up acquisition
dwf_ai = dwf.DwfAnalogIn(hdwf)
dwf_ai.channelEnableSet(0, True)
dwf_ai.channelRangeSet(0, 5.0)
dwf_ai.acquisitionModeSet(dwf_ai.ACQMODE_SCAN_SHIFT)
dwf_ai.frequencySet(HZ_ACQ)
dwf_ai.bufferSizeSet(N_SAMPLES)

#wait at least 2 seconds for the offset to stabilize
time.sleep(2)

#begin acquisition
dwf_ai.configure(0, True)

plt.axis([0, N_SAMPLES, -2.5, 2.5])
plt.ion()
hl, = plt.plot([], [])
hl.set_xdata(np.arange(0, N_SAMPLES))

while True:
    sts = dwf_ai.status(True)

    cValid = dwf_ai.statusSamplesValid()

    # get samples
    rgdSamples = dwf_ai.statusData(0, cValid)
    print(cValid)
    hl.set_ydata(rgdSamples)
    plt.draw()
    plt.pause(0.01)

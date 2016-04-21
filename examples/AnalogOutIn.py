#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 2

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 10/17/2013

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import time
import matplotlib.pyplot as plt

print("Version: " + dwf.FDwfGetVersion())

cdevices = dwf.DwfEnumeration()
print("Number of Devices: " + str(len(cdevices)))

if len(cdevices) == 0:
    print("no device detected")
    quit()

print("Opening first device")
hdwf = dwf.Dwf()

print("Configure and start first analog out channel")
dwf_ao = dwf.DwfAnalogOut(hdwf)
dwf_ao.nodeEnableSet(0, dwf_ao.NODE_CARRIER, True)
print("1 = Sine wave")
dwf_ao.nodeFunctionSet(0, dwf_ao.NODE_CARRIER, dwf_ao.FUNC_SINE)
dwf_ao.nodeFrequencySet(0, dwf_ao.NODE_CARRIER, 3000.0)
print()
dwf_ao.configure(0, True)

print("Configure analog in")
dwf_ai = dwf.DwfAnalogIn(hdwf)
dwf_ai.frequencySet(1e6)
print("Set range for all channels")
dwf_ai.channelRangeSet(-1, 4.0)
dwf_ai.bufferSizeSet(1000)

print("Wait after first device opening the analog in offset to stabilize")
time.sleep(2)

print("Starting acquisition")
dwf_ai.configure(1, True)

print("   waiting to finish")
while True:
    if dwf_ai.status(True) == dwf_ai.STATE_DONE:
        break
    time.sleep(0.1)
print("   done")

print("   reading data")
rg = dwf_ai.statusData(0, 1000)

hdwf.close()

dc = sum(rg) / len(rg)
print("DC: " + str(dc) + "V")

plt.plot(rg)
plt.show()

#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 10/17/2013

   Requires:                       
       Python 2.7, 3.3 or later
       numpy, matplotlib
"""
import dwf
import time
import matplotlib.pyplot as plt

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device")
dwf_ain = dwf.DwfAnalogIn()

print("Preparing to read sample...")

#set up acquisition
dwf_ain.frequencySet(20e6)
dwf_ain.bufferSizeSet(4000)
dwf_ain.channelEnableSet(0, True)
dwf_ain.channelRangeSet(0, 5.0)

#wait at least 2 seconds for the offset to stabilize
time.sleep(2)

#begin acquisition
dwf_ain.configure(False, True)
print("   waiting to finish")

while True:
    sts = dwf_ain.status(True)
    print("STS VAL: " + str(sts) + " STS DONE: " + str(dwf_ain.STATE_DONE))
    if sts == dwf_ain.STATE_DONE:
        break
    time.sleep(0.1)
print("Acquisition finished")

rgdSamples = dwf_ain.statusData(0, 4000)
dwf_ain.close()

#plot window
dc = sum(rgdSamples) / len(rgdSamples)
print("DC: " + str(dc) + "V")

plt.plot(rgdSamples)
plt.show()

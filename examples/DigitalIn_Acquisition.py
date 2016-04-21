#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 5

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Author:  Digilent, Inc.
   Revision: 10/17/2013

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
dwf_do = dwf.DwfDigitalOut()

print("Preparing to read sample...")

# generate on DIO-0 1Mhz pulse (100MHz/25/(3+1)), 25% duty (3low 1high)
#dwf_do.enableSet(0, True)
#dwf_do.dividerSet(0, 25)
#dwf_do.counterSet(0, 3, 1)
    
# generate counter
for i in range(16):
    dwf_do.enableSet(i, True)
    dwf_do.dividerSet(i, 0x01 << i)
    dwf_do.counterSet(i, 1, 1)

dwf_do.configure(True)

#sample rate = system frequency / divider, 100MHz/1
dwf_di = dwf.DwfDigitalIn(dwf_do)
dwf_di.dividerSet(1)
# 16bit per sample format
dwf_di.sampleFormatSet(16)
# set number of sample to acquire
N_SAMPLES = 1000
dwf_di.bufferSizeSet(N_SAMPLES)

# begin acquisition
dwf_di.configure(False, True)
print("   waiting to finish")

while True:
    sts = dwf_di.status(True)
    print("STS VAL: " + str(sts))
    if sts == dwf_di.STATE_DONE:
        break
    time.sleep(1)
print("Acquisition finished")

# get samples, byte size
rgwSamples = dwf_di.statusData(N_SAMPLES)
dwf_di.close()
dwf_do.close()

plt.plot(rgwSamples)
plt.show()

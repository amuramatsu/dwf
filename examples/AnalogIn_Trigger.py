#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 5

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 10/17/2013

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import time

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device")
dwf_ai = dwf.DwfAnalogIn()

print("Preparing to read sample...")

#set up acquisition
dwf_ai.frequencySet(20e6)
dwf_ai.bufferSizeSet(8192)
dwf_ai.channelEnableSet(0, True)
dwf_ai.channelRangeSet(0, 5.0)

#set up trigger
dwf_ai.triggerAutoTimeoutSet(0.0) #disable auto trigger
dwf_ai.triggerSourceSet(dwf_ai.TRIGSRC.DETECTOR_ANALOG_IN)
dwf_ai.triggerTypeSet(dwf_ai.TRIGTYPE.EDGE)
dwf_ai.triggerChannelSet(0)
dwf_ai.triggerLevelSet(1.5) # 1.5V
dwf_ai.triggerConditionSet(dwf_ai.TRIGCOND.RISING_POSITIVE)

# wait at least 2 seconds with Analog Discovery for the offset to stabilize,
# before the first reading after device open or offset/range change
time.sleep(2)

print("   starting repeated acquisitions")
for iTrigger in range(100):
    #begin acquisition
    dwf_ai.configure(False, True)

    while True:
        if dwf_ai.status(True) == dwf_ai.STATE.DONE:
            break
        time.sleep(0.001)

    rgdSamples = dwf_ai.statusData(0, 8192)
    
    dc = sum(rgdSamples) / len(rgdSamples)
    print("Acquisition #" + str(iTrigger+1) + " average: " + str(dc) + "V")

dwf_ai.close()

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

#declare constant
CHANNEL = 0

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device...")
dwf_ao = dwf.DwfAnalogOut()

print("Generating sine wave...")
dwf_ao.nodeEnableSet(CHANNEL, dwf_ao.NODE_CARRIER, True)
dwf_ao.nodeFunctionSet(CHANNEL, dwf_ao.NODE_CARRIER, dwf_ao.FUNC_SINE)
dwf_ao.nodeFrequencySet(CHANNEL, dwf_ao.NODE_CARRIER, 10e3)
dwf_ao.nodeAmplitudeSet(CHANNEL, dwf_ao.NODE_CARRIER, 1.0)
dwf_ao.nodeOffsetSet(CHANNEL, dwf_ao.NODE_CARRIER, 1.0)

dwf_ao.nodeEnableSet(CHANNEL, dwf_ao.NODE_FM, True)
dwf_ao.nodeFunctionSet(CHANNEL, dwf_ao.NODE_FM, dwf_ao.FUNC_RAMP_UP)
dwf_ao.nodeFrequencySet(CHANNEL, dwf_ao.NODE_FM, 10e3)
dwf_ao.nodeAmplitudeSet(CHANNEL, dwf_ao.NODE_FM, 1.0)
dwf_ao.nodeOffsetSet(CHANNEL, dwf_ao.NODE_FM, 1.0)

print("Play sine wave for 10 seconds...")
dwf_ao.configure(CHANNEL, True)
time.sleep(10)
print("done.")
dwf_ao.close()

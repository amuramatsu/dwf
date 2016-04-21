#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 8/21/2014

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import math
import time
import sys

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device")
dwf_do = dwf.DwfDigitalOut()

hzSys = dwf_do.internalClockInfo()

# 1kHz pulse on IO pin 0
dwf_do.enableSet(0, True)
# prescaler to 2kHz, SystemFrequency/1kHz/2
dwf_do.dividerSet(0, int(hzSys / 1e3 / 2))
# 1 tick low, 1 tick high
dwf_do.counterSet(0, 1, 1)

# 1kHz 25% duty pulse on IO pin 1
dwf_do.enableSet(1, True)
# prescaler to 4kHz SystemFrequency/1kHz/4
dwf_do.dividerSet(1, int(hzSys / 1e3 / 4))
# 3 ticks low, 1 tick high
dwf_do.counterSet(1, 3, 1)

# 2kHz random on IO pin 2
dwf_do.enableSet(2, True)
dwf_do.typeSet(2, dwf_do.TYPE_RANDOM)
dwf_do.dividerSet(2, int(hzSys / 2e3))

rgdSamples = [0x00, 0xAA, 0x66, 0xFF]
# 1kHz sample rate custom on IO pin 3
dwf_do.enableSet(3, 1)
dwf_do.typeSet(3, dwf_do.TYPE_CUSTOM)
dwf_do.dividerSet(3, int(hzSys / 1e3))
dwf_do.dataSet(3, dwf.create_bitdata_stream(rgdSamples, 8))

dwf_do.configure(True)

print("Generating output counter for 10 seconds...")
time.sleep(10)

dwf_do.reset()
dwf_do.close()

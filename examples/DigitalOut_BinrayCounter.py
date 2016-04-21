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
dwf_do = dwf.DwfDigitalOut()

hzSys = dwf_do.internalClockInfo()
print(" internal frequency is " + str(hzSys))

# 100kHz counter rate, SystemFrequency/100kHz
cntFreq = int(hzSys / 1e5)

# generate counter
for i in range(16):
    dwf_do.enableSet(i, True)
    # increase by 2 the period of successive bits
    dwf_do.dividerSet(i, 0x01 << i)
    dwf_do.counterSet(i, cntFreq, cntFreq)

dwf_do.configure(True)

print("Generating binary counter for 10 seconds...")
time.sleep(10)

dwf_do.close()

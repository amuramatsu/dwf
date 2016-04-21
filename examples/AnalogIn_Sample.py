#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 4

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
print("Opening first device...")
dwf_ai = dwf.DwfAnalogIn()

print("Preparing to read sample...")
dwf_ai.channelEnableSet(0, True)
dwf_ai.channelOffsetSet(0, 0.0)
dwf_ai.channelRangeSet(0, 5.0)
dwf_ai.configure(False, False)
time.sleep(2)
dwf_ai.status(False)
voltage = dwf_ai.statusSample(0)
print("Voltage:  " + str(voltage))

dwf_ai.close()

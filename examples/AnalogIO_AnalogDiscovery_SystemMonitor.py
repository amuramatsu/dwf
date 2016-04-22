#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 7

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
dwf_aio = dwf.DwfAnalogIO()

print("Device USB supply voltage, current and device temperature:")
#monitor voltage, current, temperature
#60 times, once per second
for i in range(60):
    # wait between readings; the update rate is approximately 1Hz
    time.sleep(1)
    # fetch analog IO status from device
    dwf_aio.status()
    # get system monitor readings
    deviceVoltage = dwf_aio.channelNodeStatus(2, 0)
    deviceCurrent = dwf_aio.channelNodeStatus(2, 1)
    deviceTemperature = dwf_aio.channelNodeStatus(2, 2)
    print("%.4f V\t%.4f A\t%.4fdegC" % (
        deviceVoltage, deviceCurrent, deviceTemperature))
    
#close the device
dwf_aio.close()

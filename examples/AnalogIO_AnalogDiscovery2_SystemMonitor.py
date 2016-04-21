#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example
   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 12/29/2015

   Requires:                       
       Python 2.7, 3.3 or lator
"""

import dwf
import time

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device")
dwf_aio = dwf.DwfAnalogIO()

print("Device temperature and USB/AUX supply voltage and current")
#monitor voltage, current, temperature
#60 times, once per second
for i in range(60):
    # wait between readings
    time.sleep(1)
    # fetch analog IO status from device
    dwf_aio.status()

    # get system monitor readings
    usbVoltage = dwf_aio.channelNodeStatus(2, 0)
    usbCurrent = dwf_aio.channelNodeStatus(2, 1)
    deviceTemperature = dwf_aio.channelNodeStatus(2, 2)
    auxVoltage = dwf_aio.channelNodeStatus(3, 0)
    auxCurrent = dwf_aio.channelNodeStatus(3, 1)
    print("Temperature: %.2fdegC" % deviceTemperature)
    print("USB:\t%.3fV\t%.3fA" % (usbVoltage, usbCurrent))
    print("AUX:\t%.3fV\t%.3fA" % (auxVoltage, auxCurrent))
    
#close the device
dwf_aio.close()

#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 1

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision:  10/17/2013

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import sys

#check library loading errors, like: Adept Runtime not found
print(dwf.FDwfGetLastErrorMsg())

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#enumerate and print device information
devs = dwf.DwfEnumeration()
print("Number of Devices: " + str(len(devs)))

for i, device in enumerate(devs):
    print("------------------------------")
    print("Device " + str(i) + " : ")
    print("\t" + device.deviceName())
    print( "\t" + device.SN())
    
    if not device.isOpened():
        dwf_ai = dwf.DwfAnalogIn(device)
        channel = dwf_ai.channelCount()
        _, hzFreq = dwf_ai.frequencyInfo()
        print("\tAnalog input channels: " + str(channel))
        print("\tMax freq: " + str(hzFreq))
        dwf_ai.close()

# ensure all devices are closed
dwf.FDwfDeviceCloseAll()

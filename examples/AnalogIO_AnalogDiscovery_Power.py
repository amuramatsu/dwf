#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 6

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

print("Preparing to read sample...")

#set up analog IO channel nodes
# enable positive supply
dwf_aio.channelNodeSet(0, 0, True) 
# enable negative supply
dwf_aio.channelNodeSet(1, 0, True)
# master enable
dwf_aio.enableSet(True)

for i in range(60):
    #wait 1 second between readings
    time.sleep(1)
    #fetch analogIO status from device
    dwf_aio.status()

    #supply monitor
    supplyVoltage = dwf_aio.channelNodeStatus(3, 0)
    supplyCurrent = dwf_aio.channelNodeStatus(3, 1)

    supplyPower = supplyVoltage * supplyCurrent
    print("Total supply power: %fW" % supplyPower)

    supplyLoadPercentage = 100 * (supplyCurrent / 0.2)
    print("Load: %f%%" % supplyLoadPercentage)

    # in case of over-current condition the supplies are disabled
    if not dwf_aio.enableStatus():
        #re-enable supplies
        dwf_aio.enableSet(False)
        dwf_aio.enableSet(True)

#close the device
dwf_aio.close()

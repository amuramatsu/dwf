#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 12/28/2015

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import time

print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device")
dwf_aio = dwf.DwfAnalogIO()

# set up analog IO channel nodes
# enable positive supply
dwf_aio.channelNodeSet(0, 0, True)
# set voltage to 5 V
dwf_aio.channelNodeSet(0, 1, 5.0)
# enable negative supply
dwf_aio.channelNodeSet(1, 0, True)
# set voltage to -5 V
dwf_aio.channelNodeSet(1, 1, -5.0)
# master enable
dwf_aio.enableSet(True)

for i in range(60):
    #wait 1 second between readings
    time.sleep(1)
    #fetch analogIO status from device
    dwf_aio.status()

    #supply monitor
    usbVoltage = dwf_aio.channelNodeStatus(2, 0)
    usbCurrent = dwf_aio.channelNodeStatus(2, 1)
    auxVoltage = dwf_aio.channelNodeStatus(3, 0)
    auxCurrent = dwf_aio.channelNodeStatus(3, 1)
    print("USB: %.3fV\t%.3fA" % (usbVoltage, usbCurrent))
    print("AUX: %.3fV\t%.3fA" % (auxVoltage, auxCurrent))

    # in case of over-current condition the supplies are disabled
    if not dwf_aio.enableStatus():
        #re-enable supplies
        print("Restart")
        dwf_aio.enableSet(False)
        dwf_aio.enableSet(True)

#close the device
dwf_aio.close()

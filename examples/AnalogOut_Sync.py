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

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device...")
dwf_ao = dwf.DwfAnalogOut()

print("Generating sine wave...")
# enable two channels
dwf_ao.nodeEnableSet(0, dwf_ao.NODE.CARRIER, True)
dwf_ao.nodeEnableSet(1, dwf_ao.NODE.CARRIER, True)
# for second channel set master the first channel
dwf_ao.masterSet(1, 0)
# slave channel is controlled by the master channel
# it is enough to set trigger, wait, run and repeat paramters for master channel

# configure enabled channels
dwf_ao.nodeFunctionSet(-1, dwf_ao.NODE.CARRIER, dwf_ao.FUNC.SINE)
dwf_ao.nodeFrequencySet(-1, dwf_ao.NODE.CARRIER, 1000.0)
dwf_ao.nodeAmplitudeSet(-1, dwf_ao.NODE.CARRIER, 1.0)

#set phase for second channel
dwf_ao.nodePhaseSet(1, dwf_ao.NODE.CARRIER, 180.0)

print("Generating sine wave for 10 seconds...")
# start signal generation, 
# the second, slave channel will start too
dwf_ao.configure(0, True)

time.sleep(10)

print("done.")
dwf_ao.close()

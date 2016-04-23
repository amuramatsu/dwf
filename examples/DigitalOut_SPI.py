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
import time

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
dwf_do = dwf.DwfDigitalOut()
hzSys = dwf_do.internalClockInfo()

# SPI parameters
CPOL = 0 # or 1
CPHA = 0 # or 1
hzFreq = 1e6
cBits = 16
rgdData = [0x12, 0x34]

# serialization time length
dwf_do.runSet((cBits + 0.5) / hzFreq)

# DIO 2 Select 
dwf_do.enableSet(2, True)
# output high while DigitalOut not running
dwf_do.idleSet(2, dwf_do.IDLE.HIGH)
# output constant low while running
dwf_do.counterInitSet(2, False, 0)
dwf_do.counterSet(2, 0, 0)

# DIO 1 Clock
dwf_do.enableSet(1, True)
# set prescaler twice of SPI frequency
dwf_do.dividerSet(1, int(hzSys / hzFreq / 2))
# 1 tick low, 1 tick high
dwf_do.counterSet(1, 1, 1)
# start with low or high based on clock polarity
dwf_do.counterInitSet(1, CPOL, 1)
dwf_do.idleSet(1, dwf_do.IDLE.HIGH if CPOL else dwf_do.IDLE.LOW)

# DIO 0 Data
dwf_do.enableSet(0, True)
dwf_do.typeSet(0, dwf_do.TYPE.CUSTOM)
# for high active clock, hold the first bit for 1.5 periods 
dwf_do.dividerInitSet(0, int((1+0.5*CPHA)*hzSys/hzFreq))
# SPI frequency, bit frequency
dwf_do.dividerSet(0, int(hzSys / hzFreq))
# data sent out LSB first
dwf_do.dataSet(0, dwf.create_bitdata_stream(rgdData, 8))

dwf_do.configure(True)
print("Generating SPI signal")
time.sleep(1)

dwf_do.reset()
dwf_do.close()

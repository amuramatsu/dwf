#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 8

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 10/17/2013

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import sys

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device")
dwf_dio = dwf.DwfDigitalIO()

print("Preparing to read Digital IO pins...")

# enable output/mask on 8 LSB IO pins, from DIO 0 to 7
dwf_dio.outputEnableSet(0x00FF)
# set value on enabled IO pins
dwf_dio.outputSet(0x0012)
# fetch digital IO information from the device 
dwf_dio.status()
# read state of all pins, regardless of output enable
dwRead = dwf_dio.inputStatus()

#print dwRead as bitfield (32 digits, removing 0b at the front)
print("Digital IO Pins:  " + bin(dwRead)[2:].zfill(32))

dwf_dio.close()

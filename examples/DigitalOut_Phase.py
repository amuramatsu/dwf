#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 04/20/2015

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import time
import sys

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device")
dwf_do = dwf.DwfDigitalOut()

# 2 pin phase start low and high
for i in range(2):
    dwf_do.enableSet(i, True)
    dwf_do.counterInitSet(i, i == 1, 50)
    dwf_do.counterSet(i, 50, 50) # 100MHz base freq /(50+50) = 1MHz

dwf_do.configure(True)
print("Generating for 10 seconds...")
time.sleep(10)

# 3 pin phase
dwf_do.counterInitSet(0, True, 0)
dwf_do.counterInitSet(1, False, 20)
dwf_do.counterInitSet(2, True, 10)
for i in range(3):
    dwf_do.enableSet(i, True)
    dwf_do.counterSet(i, 30, 30) # 100MHz base freq /(30+30) = 1.67 MHz

dwf_do.configure(True)
print("Generating for 10 seconds...")
time.sleep(10)

# 4 pin phase starting: low & 25, low $ 50, high & 25, high & 50 
for i in range(4):
    dwf_do.enableSet(i, True)
    dwf_do.counterInitSet(i, (i==2) or (i==3), 25 if (i==0 or i==2) else 50)
    dwf_do.counterSet(i, 50, 50)

dwf_do.configure(True)
print("Generating for 10 seconds...")
time.sleep(10)

dwf_do.close()

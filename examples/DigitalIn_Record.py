#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 11/24/2014

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import math

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device")
dwf_di = dwf.DwfDigitalIn()
dwf_do = dwf.DwfDigitalOut(dwf_di)

print("Configuring Digital Out / In...")

# generate counter
for i in range(16):
    dwf_do.enableSet(i, True)
    dwf_do.dividerSet(i, 0x01 << i)
    dwf_do.counterSet(i, 1000, 1000)

dwf_do.configure(True)

# set number of sample to acquire
N_SAMPLES = 100000

# in record mode samples after trigger are acquired only
dwf_di.acquisitionModeSet(dwf_di.ACQMODE_RECORD)
# sample rate = system frequency / divider, 100MHz/1000 = 100kHz
dwf_di.dividerSet(1000)
# 16bit per sample format
dwf_di.sampleFormatSet(16)
# number of samples after trigger
dwf_di.triggerPositionSet(N_SAMPLES)
# trigger when all digital pins are low
dwf_di.triggerSourceSet(dwf_di.TRIGSRC_DETECTOR_DIGITAL_IN)
# trigger detector mask:   low &   high & ( rising | falling )
dwf_di.triggerSet(0xFFFF,  0x0000, 0x0000, 0x0000)

# begin acquisition
dwf_di.configure(False, True)

print("Starting record")

cSamples = 0
rgwSamples = []
fLost = False
fCorrupted = False
while cSamples < N_SAMPLES:
    sts = dwf_di.status(True)
    if cSamples == 0 and sts in (dwf_di.STATE_CONFIG,
                                 dwf_di.STATE_PREFILL,
                                 dwf_di.STATE_ARMED):
        # acquisition not yet started.
        continue
    
    cAvailable, cLost, cCorrupted = dwf_di.statusRecord()
    cSamples += cLost
    
    if cLost > 0:
        fLost = True
    if cCorrupted > 0:
        fCorrupted = True
    if cAvailable == 0:
        continue
    
    if cSamples + cAvailable > N_SAMPLES:
        cAvailable = N_SAMPLES - cSamples
    
    # get samples
    rgwSamples.extend(dwf_di.statusData(cAvailable))
    cSamples += cAvailable

dwf_do.close()
dwf_di.close()

print("Recording finished")
if fLost:
    print("Samples were lost! Reduce sample rate")
if fCorrupted:
    print("Samples could be corrupted! Reduce sample rate")

with open("record.csv", "w") as f:
    for v in rgwSamples:
        f.write("%s\n" % v)

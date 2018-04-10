#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
===========================================
Digilent's DWF library wrapper for python.
===========================================

Copyright notice
================

Copyright (c) 2016 MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php


Supported platforms
===================

* Python 2.6, 2.7 or Python 3.3 or above
* Windows, OSX, or Linux with Digilent's Waveforms 2015 or lator

This code is tested with Waveforms SDK, October 12, 2015 version.
'''

from enum import IntEnum

from . import lowlevel as _l

#################################################################
# Class-based APIs
##################

def _make_set(value, enum):
    result = []
    for e in list(enum):
        if _l.IsBitSet(value, e.value):
            result.append(e)
    return frozenset(result)

# DEVICE MANAGMENT FUNCTIONS
# Enumeration:
class ENUMFILTER(IntEnum):
    ALL = _l.enumfilterAll
    EEXPLORER = _l.enumfilterEExplorer
    DISCOVERY = _l.enumfilterDiscovery

def DwfEnumeration(enumfilter=ENUMFILTER.ALL):
    num = _l.FDwfEnum(enumfilter)
    return tuple([ DwfDevice(i) for i in range(num) ])

class DwfDevice(object):
    class DEVID(IntEnum):
        EEXPLORER = _l.devidEExplorer
        DISCOVERY = _l.devidDiscovery

    class DEVVER(IntEnum):
        EEXPLORER_C = _l.devverEExplorerC
        EEXPLORER_E = _l.devverEExplorerE
        EEXPLORER_F = _l.devverEExplorerF
        DISCOVERY_A = _l.devverDiscoveryA
        DISCOVERY_B = _l.devverDiscoveryB
        DISCOVERY_C = _l.devverDiscoveryC

    class CONFIGINFO(IntEnum):
        ANALOG_IN_CHANNEL_COUNT = _l.DECIAnalogInChannelCount
        ANALOG_OUT_CHANNEL_COUNT = _l.DECIAnalogOutChannelCount
        ANALOG_IO_CHANNEL_COUNT = _l.DECIAnalogIOChannelCount
        DIGITAL_IN_CHANNEL_COUNT = _l.DECIDigitalInChannelCount
        DIGITAL_OUT_CHANNEL_COUNT = _l.DECIDigitalOutChannelCount
        DIGITAL_IO_CHANNEL_COUNT = _l.DECIDigitalIOChannelCount
        ANALOG_IN_BUFFER_SIZE = _l.DECIAnalogInBufferSize
        ANALOG_OUT_BUFFER_SIZE = _l.DECIAnalogOutBufferSize
        DIGITAL_IN_BUFFER_SIZE = _l.DECIDigitalInBufferSize
        DIGITAL_OUT_BUFFER_SIZE = _l.DECIDigitalOutBufferSize
    
    def __init__(self, idxDevice):
        self.idxDevice = idxDevice
    def deviceType(self):
        devid, devver = _l.FDwfEnumDeviceType(self.idxDevice)
        return self.DEVID(devid), self.DEVVER(devver)
    def isOpened(self):
        return bool(_l.FDwfEnumDeviceIsOpened(self.idxDevice))
    def userName(self):
        return _l.FDwfEnumUserName(self.idxDevice)
    def deviceName(self):
        return _l.FDwfEnumDeviceName(self.idxDevice)
    def SN(self):
        return _l.FDwfEnumSN(self.idxDevice)
    def config(self):
        return _l.FDwfEnumConfig(self.idxDevice)
    def configInfo(self, info):
        return _l.FDwfEnumConfigInfo(self.idxDevice, info)
    
    def open(self, config=None):
        return Dwf(self.idxDevice, idxCfg=config)

class _HDwf(object):
    def __init__(self, hdwf):
        self.hdwf = hdwf
    @property
    def _as_parameter_(self):
        return self.hdwf
    def close(self):
        if self.hdwf != _l.hdwfNone:
            _l.FDwfDeviceClose(self.hdwf)
            self.hdwf = _l.hdwfNone
    def __del__(self):
        self.close()

class Dwf(object):
    DEVICE_NONE = _l.hdwfNone

    class TRIGSRC(IntEnum):
        '''trigger source'''
        NONE = _l.trigsrcNone
        PC = _l.trigsrcPC
        DETECTOR_ANALOG_IN = _l.trigsrcDetectorAnalogIn
        DETECTOR_DIGITAL_IN = _l.trigsrcDetectorDigitalIn
        ANALOG_IN = _l.trigsrcAnalogIn
        DIGITAL_IN = _l.trigsrcDigitalIn
        DIGITAL_OUT = _l.trigsrcDigitalOut
        ANALOG_OUT1 = _l.trigsrcAnalogOut1
        ANALOG_OUT2 = _l.trigsrcAnalogOut2
        ANALOG_OUT3 = _l.trigsrcAnalogOut3
        ANALOG_OUT4 = _l.trigsrcAnalogOut4
        EXTERNAL1 = _l.trigsrcExternal1
        EXTERNAL2 = _l.trigsrcExternal2
        EXTERNAL3 = _l.trigsrcExternal3
        EXTERNAL4 = _l.trigsrcExternal4

    class STATE(IntEnum):
        '''instrument states'''
        READY = _l.DwfStateReady
        CONFIG = _l.DwfStateConfig
        PREFILL = _l.DwfStatePrefill
        ARMED = _l.DwfStateArmed
        WAIT = _l.DwfStateWait
        TRIGGERED = _l.DwfStateTriggered
        RUNNING = _l.DwfStateRunning
        DONE = _l.DwfStateDone
    
    def __init__(self, idxDevice=-1, idxCfg=None):
        if isinstance(idxDevice, Dwf):
            raise Exception()
        if isinstance(idxDevice, DwfDevice):
            idxDevice = idxDevice.idxDevice
        if idxCfg is None:
            hdwf = _l.FDwfDeviceOpen(idxDevice)
        else:
            hdwf = _l.FDwfDeviceConfigOpen(idxDevice, idxCfg)
        if hdwf == self.DEVICE_NONE:
            raise RuntimeError("Device is not found")
        self.hdwf = _HDwf(hdwf)
    def close(self):
        self.hdwf.close()
    def autoConfigureSet(self, auto_configure):
        _l.FDwfDeviceAutoConfigureSet(self.hdwf, auto_configure)
    def autoConfigureGet(self):
        return bool(_l.FDwfDeviceAutoConfigureGet(self.hdwf))
    def reset(self):
        _l.FDwfDeviceReset(self.hdwf)
    def enableSet(self, enable):
        _l.FDwfDeviceEnableSet(self.hdwf, enable)
    def triggerInfo(self):
        return _make_set(_l.FDwfDeviceTriggerInfo(self.hdwf), self.TRIGSRC)
    def triggerSet(self, idxPin, trigsrc):
        _l.FDwfDeviceTriggerSet(self.hdwf, idxPin, trigsrc)
    def triggerGet(self, idxPin):
        return self.TRIGSRC(_l.FDwfDeviceTriggerGet(self.hdwf, idxPin))
    def triggerPC(self):
        _l.FDwfDeviceTriggerPC(self.hdwf)

# ANALOG IN INSTRUMENT FUNCTIONS
class DwfAnalogIn(Dwf):
    class ACQMODE(IntEnum):
        '''acquisition modes'''
        SINGLE = _l.acqmodeSingle
        SCAN_SHIFT = _l.acqmodeScanShift
        SCAN_SCREEN = _l.acqmodeScanScreen
        RECORD = _l.acqmodeRecord

    class FILTER(IntEnum):
        '''analog acquisition filter'''
        DECIMATE = _l.filterDecimate
        AVERAGE = _l.filterAverage
        MIN_MAX = _l.filterMinMax

    class TRIGTYPE(IntEnum):
        '''analog in trigger mode'''
        EDGE = _l.trigtypeEdge
        PULSE = _l.trigtypePulse
        TRANSITION = _l.trigtypeTransition

    class TRIGCOND(IntEnum):
        '''analog in trigger condition'''
        RISING_POSITIVE = _l.trigcondRisingPositive
        FALLING_NEGATIVE = _l.trigcondFallingNegative

    class TRIGLEN(IntEnum):
        '''analog in trigger length condition'''
        LESS = _l.triglenLess
        TIMEOUT = _l.triglenTimeout
        MORE = _l.triglenMore
    
# Control and status:
    def __init__(self, idxDevice=-1, idxCfg=None):
        if isinstance(idxDevice, Dwf):
            self.hdwf = idxDevice.hdwf
        else:
            super(DwfAnalogIn, self).__init__(idxDevice, idxCfg)
    def reset(self, parent=False):
        if parent: super(DwfAnalogIn, self).reset()
        _l.FDwfAnalogInReset(self.hdwf)
    def configure(self, reconfigure, start):
        _l.FDwfAnalogInConfigure(self.hdwf, reconfigure, start)
    def status(self, read_data):
        return self.STATE(_l.FDwfAnalogInStatus(self.hdwf, read_data))
    def statusSamplesLeft(self):
        return _l.FDwfAnalogInStatusSamplesLeft(self.hdwf)
    def statusSamplesValid(self):
        return _l.FDwfAnalogInStatusSamplesValid(self.hdwf)
    def statusIndexWrite(self):
        return _l.FDwfAnalogInStatusIndexWrite(self.hdwf)
    def statusAutotriggered(self):
        return bool(_l.FDwfAnalogInStatusAutoTriggered(self.hdwf))
    def statusData(self, idxChannel, data_num):
        return _l.FDwfAnalogInStatusData(self.hdwf, idxChannel, data_num)
    def statusNoise(self, idxChannel, data_num):
        return _l.FDwfAnalogInStatusNoise(self.hdwf, idxChannel, data_num)
    def statusSample(self, idxChannel):
        return _l.FDwfAnalogInStatusSample(self.hdwf, idxChannel)
    def statusRecord(self):
        return _l.FDwfAnalogInStatusRecord(self.hdwf)
    def recordLengthSet(self, length):
        _l.FDwfAnalogInRecordLengthSet(self.hdwf, length)
    def recordLengthGet(self):
        return _l.FDwfAnalogInRecordLengthGet(self.hdwf)

# Acquisition configuration:
    def frequencyInfo(self):
        return _l.FDwfAnalogInFrequencyInfo(self.hdwf)
    def frequencySet(self, hzFrequency):
        _l.FDwfAnalogInFrequencySet(self.hdwf, hzFrequency)
    def frequencyGet(self):
        return _l.FDwfAnalogInFrequencyGet(self.hdwf)
    def bitsInfo(self):
        '''Returns the number of ADC bits'''
        return _l.FDwfAnalogInBitsInfo(self.hdwf)

    def bufferSizeInfo(self):
        return _l.FDwfAnalogInBufferSizeInfo(self.hdwf)
    def bufferSizeSet(self, size):
        _l.FDwfAnalogInBufferSizeSet(self.hdwf, size)
    def bufferSizeGet(self):
        return _l.FDwfAnalogInBufferSizeGet(self.hdwf)

    def noiseSizeInfo(self):
        return _l.FDwfAnalogInNoiseSizeInfo(self.hdwf)
    def noiseSizeGet(self):
        return _l.FDwfAnalogInNoiseSizeGet(self.hdwf)

    def acquisitionModeInfo(self):
        return _make_set(
            _l.FDwfAnalogInAcquisitionModeInfo(self.hdwf), self.ACQMODE)
    def acquisitionModeSet(self, acqmode):
        _l.FDwfAnalogInAcquisitionModeSet(self.hdwf, acqmode)
    def acquisitionModeGet(self):
        return self.ACQMODE(_l.FDwfAnalogInAcquisitionModeGet(self.hdwf))

# Channel configuration:
    def channelCount(self):
        return _l.FDwfAnalogInChannelCount(self.hdwf)
    def channelEnableSet(self, idxChannel, enable):
        _l.FDwfAnalogInChannelEnableSet(self.hdwf, idxChannel, enable)
    def channelEnableGet(self, idxChannel):
        return bool(_l.FDwfAnalogInChannelEnableGet(self.hdwf, idxChannel))
    def channelFilterInfo(self):
        return _make_set(
            _l.FDwfAnalogInChannelFilterInfo(self.hdwf), self.FILTER)
    def channelFilterSet(self, idxChannel, filter_):
        _l.FDwfAnalogInChannelFilterSet(self.hdwf, idxChannel, filter_)
    def channelFilterGet(self, idxChannel):
        return self.FILTER(_l.FDwfAnalogInChannelFilterGet(
            self.hdwf, idxChannel))
    def channelRangeInfo(self):
        return _l.FDwfAnalogInChannelRangeInfo(self.hdwf)
    def channelRangeSteps(self):
        return _l.FDwfAnalogInChannelRangeSteps(self.hdwf)
    def channelRangeSet(self, idxChannel, voltsRange):
        _l.FDwfAnalogInChannelRangeSet(self.hdwf, idxChannel, voltsRange)
    def channelRangeGet(self, idxChannel):
        return _l.FDwfAnalogInChannelRangeGet(self.hdwf, idxChannel)
    def channelOffsetInfo(self):
        return _l.FDwfAnalogInChannelOffsetInfo(self.hdwf)
    def channelOffsetSet(self, idxChannel, voltOffset):
        _l.FDwfAnalogInChannelOffsetSet(self.hdwf, idxChannel, voltOffset)
    def channelOffsetGet(self, idxChannel):
        return _l.FDwfAnalogInChannelOffsetGet(self.hdwf, idxChannel)
    def channelAttenuationSet(self, idxChannel, attenuation):
        _l.FDwfAnalogInChannelAttenuationSet(self.hdwf, idxChannel, attenuation)
    def channelAttenuationGet(self, idxChannel):
        return _l.FDwfAnalogInChannelAttenuationGet(self.hdwf, idxChannel)

# Trigger configuration:
    def triggerSourceInfo(self):
        return _make_set(
            _l.FDwfAnalogInTriggerSourceInfo(self.hdwf), self.TRIGSRC)
    def triggerSourceSet(self, trigsrc):
        _l.FDwfAnalogInTriggerSourceSet(self.hdwf, trigsrc)
    def triggerSourceGet(self):
        return self.TRIGSRC(_l.FDwfAnalogInTriggerSourceGet(self.hdwf))

    def triggerPositionInfo(self):
        return _l.FDwfAnalogInTriggerPositionInfo(self.hdwf)
    def triggerPositionSet(self, secPosition):
        _l.FDwfAnalogInTriggerPositionSet(self.hdwf, secPosition)
    def triggerPositionGet(self):
        return _l.FDwfAnalogInTriggerPositionGet(self.hdwf)
    def triggerPositionStatus(self):
        return _l.FDwfAnalogInTriggerPositionStatus(self.hdwf)

    def triggerAutoTimeoutInfo(self):
        return _l.FDwfAnalogInTriggerAutoTimeoutInfo(self.hdwf)
    def triggerAutoTimeoutSet(self, secTimeout):
        _l.FDwfAnalogInTriggerAutoTimeoutSet(self.hdwf, secTimeout)
    def triggerAutoTimeoutGet(self):
        return _l.FDwfAnalogInTriggerAutoTimeoutGet(self.hdwf)

    def triggerHoldOffInfo(self):
        return _l.FDwfAnalogInTriggerHoldOffInfo(self.hdwf)
    def triggerHoldOffSet(self, secHoldOff):
        _l.FDwfAnalogInTriggerHoldOffSet(self.hdwf, secHoldOff)
    def triggerHoldOffGet(self):
        return _l.FDwfAnalogInTriggerHoldOffGet(self.hdwf)

    def triggerTypeInfo(self):
        return _make_set(
            _l.FDwfAnalogInTriggerTypeInfo(self.hdwf), self.TRIGTYPE)
    def triggerTypeSet(self, trigtype):
        _l.FDwfAnalogInTriggerTypeSet(self.hdwf, trigtype)
    def triggerTypeGet(self):
        return self.TRIGTYPE(_l.FDwfAnalogInTriggerTypeGet(self.hdwf))

    def triggerChannelInfo(self):
        return _l.FDwfAnalogInTriggerChannelInfo(self.hdwf)
    def triggerChannelSet(self, idxChannel):
        _l.FDwfAnalogInTriggerChannelSet(self.hdwf, idxChannel)
    def triggerChannelGet(self):
        return _l.FDwfAnalogInTriggerChannelGet(self.hdwf)

    def triggerFilterInfo(self):
        return _make_set(
            _l.FDwfAnalogInTriggerFilterInfo(self.hdwf), self.FILTER)
    def triggerFilterSet(self, filter_):
        _l.FDwfAnalogInTriggerFilterSet(self.hdwf, filter_)
    def triggerFilterGet(self):
        return self.FILTER(_l.FDwfAnalogInTriggerFilterGet(self.hdwf))

    def triggerLevelInfo(self):
        return _l.FDwfAnalogInTriggerLevelInfo(self.hdwf)
    def triggerLevelSet(self, voltsLevel):
        _l.FDwfAnalogInTriggerLevelSet(self.hdwf, voltsLevel)
    def triggerLevelGet(self):
        return _l.FDwfAnalogInTriggerLevelGet(self.hdwf)

    def triggerHysteresisInfo(self):
        return _l.FDwfAnalogInTriggerHysteresisInfo(self.hdwf)
    def triggerHysteresisSet(self, voltsLevel):
        _l.FDwfAnalogInTriggerHysteresisSet(self.hdwf, voltsLevel)
    def triggerHysteresisGet(self):
        return _l.FDwfAnalogInTriggerHysteresisGet(self.hdwf)

    def triggerConditionInfo(self):
        return _make_set(
            _l.FDwfAnalogInTriggerConditionInfo(self.hdwf), self.TRIGCOND)
    def triggerConditionSet(self, trigcond):
        _l.FDwfAnalogInTriggerConditionSet(self.hdwf, trigcond)
    def triggerConditionGet(self):
        return self.TRIGCOND(_l.FDwfAnalogInTriggerConditionGet(self.hdwf))

    def triggerLengthInfo(self):
        return _l.FDwfAnalogInTriggerLengthInfo(self.hdwf)
    def triggerLengthSet(self, secLength):
        _l.FDwfAnalogInTriggerLengthSet(self.hdwf, secLength)
    def triggerLengthGet(self):
        return _l.FDwfAnalogInTriggerLengthGet(self.hdwf)

    def triggerLengthConditionInfo(self):
        return _make_set(
            _l.FDwfAnalogInTriggerLengthConditionInfo(self.hdwf), self.TRIGLEN)
    def triggerLengthConditionSet(self, triglen):
        _l.FDwfAnalogInTriggerLengthConditionSet(self.hdwf, triglen)
    def triggerLengthConditionGet(self):
        return self.TRIGLEN(_l.FDwfAnalogInTriggerLengthConditionGet(self.hdwf))


# ANALOG OUT INSTRUMENT FUNCTIONS
class DwfAnalogOut(Dwf):
    class FUNC(IntEnum):
        '''analog out signal types'''
        DC = _l.funcDC
        SINE = _l.funcSine
        SQUARE = _l.funcSquare
        TRIANGLE = _l.funcTriangle
        RAMP_UP = _l.funcRampUp
        RAMP_DOWN = _l.funcRampDown
        NOISE = _l.funcNoise
        CUSTOM = _l.funcCustom
        PLAY = _l.funcPlay

    class NODE(IntEnum):
        CARRIER = _l.AnalogOutNodeCarrier
        FM = _l.AnalogOutNodeFM
        AM = _l.AnalogOutNodeAM

    class MODE(IntEnum):
        VOLTAGE = _l.DwfAnalogOutModeVoltage
        CURRENT = _l.DwfAnalogOutModeCurrent

    class IDLE(IntEnum):
        DISABLE = _l.DwfAnalogOutIdleDisable
        OFFSET = _l.DwfAnalogOutIdleOffset
        INITIAL = _l.DwfAnalogOutIdleInitial
    
# Configuration:
    def channelCount(self): # changed names
        return _l.FDwfAnalogOutCount(self.hdwf)

    def masterSet(self, idxChannel, idxMaster):
        _l.FDwfAnalogOutMasterSet(self.hdwf, idxChannel, idxMaster)
    def masterGet(self, idxChannel):
        return _l.FDwfAnalogOutMasterGet(self.hdwf, idxChannel)

    def triggerSourceInfo(self, idxChannel):
        return _make_set(
            _l.FDwfAnalogOutTriggerSourceInfo(self.hdwf, idxChannel),
            self.TRIGSRC)
    def triggerSourceSet(self, idxChannel, trigsrc):
        _l.FDwfAnalogOutTriggerSourceSet(self.hdwf, idxChannel, trigsrc)
    def triggerSourceGet(self, idxChannel):
        return self.TRIGSRC(
            _l.FDwfAnalogOutTriggerSourceGet(self.hdwf, idxChannel))

    def runInfo(self, idxChannel):
        return _l.FDwfAnalogOutRunInfo(self.hdwf, idxChannel)
    def runSet(self, idxChannel, secRun):
        _l.FDwfAnalogOutRunSet(self.hdwf, idxChannel, secRun)
    def runGet(self, idxChannel):
        return _l.FDwfAnalogOutRunGet(self.hdwf, idxChannel)
    def runStatus(self, idxChannel):
        return _l.FDwfAnalogOutRunStatus(self.hdwf, idxChannel)

    def waitInfo(self, idxChannel):
        return _l.FDwfAnalogOutWaitInfo(self.hdwf, idxChannel)
    def waitSet(self, idxChannel, secWait):
        _l.FDwfAnalogOutWaitSet(self.hdwf, idxChannel, secWait)
    def waitGet(self, idxChannel):
        return _l.FDwfAnalogOutWaitGet(self, idxChannel)

    def repeatInfo(self, idxChannel):
        return _l.FDwfAnalogOutRepeatInfo(self.hdwf, idxChannel)
    def repeatSet(self, idxChannel, repeat):
        _l.FDwfAnalogOutRepeatSet(self.hdwf, idxChannel, repeat)
    def repeatGet(self, idxChannel):
        return _l.FDwfAnalogOutRepeatGet(self.hdwf, idxChannel)
    def repeatStatus(self, idxChannel):
        return _l.FDwfAnalogOutRepeatStatus(self.hdwf, idxChannel)

    def repeatTriggerSet(self, idxChannel, repeat_trigger):
        _l.FDwfAnalogOutRepeatTriggerSet(self.hdwf, idxChannel, repeat_trigger)
    def repeatTriggerGet(self, idxChannel):
        return bool(_l.FDwfAnalogOutRepeatTriggerGet(self.hdwf, idxChannel))

    # EExplorer channel 3&4 current/voltage limitation
    def limitationInfo(self, idxChannel):
        return _l.FDwfAnalogOutLimitationInfo(self.hdwf, idxChannel)
    def limitationSet(self, idxChannel, limit):
        _l.FDwfAnalogOutLimitationSet(self.hdwf, idxChannel, limit)
    def limitationGet(self, idxChannel):
        return _l.FDwfAnalogOutLimitationGet(self.hdwf, idxChannel)

    def modeSet(self, idxChannel, mode):
        _l.FDwfAnalogOutModeSet(self.hdwf, idxChannel, mode)
    def modeGet(self, idxChannel):
        return self.MODE(_l.FDwfAnalogOutModeGet(self.hdwf, idxChannel))

    def idleInfo(self, idxChannel):
        return _make_set(
            _l.FDwfAnalogOutIdleInfo(self.hdwf, idxChannel), self.IDLE)
    def idleSet(self, idxChannel, idle):
        _l.FDwfAnalogOutIdleSet(self.hdwf, idxChannel, idle)
    def idleGet(self, idxChannel):
        return self.IDLE(_l.FDwfAnalogOutIdleGet(self.hdwf, idxChannel))

    def nodeInfo(self, idxChannel):
        '''use IsBitSet'''
        return _make_set(
            _l.FDwfAnalogOutNodeInfo(self.hdwf, idxChannel), self.NODE)

    def nodeEnableSet(self, idxChannel, node, enable):
        _l.FDwfAnalogOutNodeEnableSet(self.hdwf, idxChannel, node, enable)
    def nodeEnableGet(self, idxChannel, node):
        return bool(_l.FDwfAnalogOutNodeEnableGet(self.hdwf, idxChannel, node))

    def nodeFunctionInfo(self, idxChannel, node):
        return _make_set(
            _l.FDwfAnalogOutNodeFunctionInfo(self.hdwf, idxChannel, node),
            self.FUNC)
    def nodeFunctionSet(self, idxChannel, node, func):
        _l.FDwfAnalogOutNodeFunctionSet(self.hdwf, idxChannel, node, func)
    def nodeFunctionGet(self, idxChannel, node):
        return self.FUNC(
            _l.FDwfAnalogOutNodeFunctionGet(self.hdwf, idxChannel, node))

    def nodeFrequencyInfo(self, idxChannel, node):
        return _l.FDwfAnalogOutNodeFrequencyInfo(self.hdwf, idxChannel, node)
    def nodeFrequencySet(self, idxChannel, node, hzFrequency):
        _l.FDwfAnalogOutNodeFrequencySet(
            self.hdwf, idxChannel, node, hzFrequency)
    def nodeFrequencyGet(self, idxChannel, node):
        return _l.FDwfAnalogOutNodeFrequencySet(self.hdwf, idxChannel, node)

# Carrier Amplitude or Modulation Index 
    def nodeAmplitudeInfo(self, idxChannel, node):
        return _l.FDwfAnalogOutNodeAmplitudeInfo(self, idxChannel, node)
    def nodeAmplitudeSet(self, idxChannel, node, amplitude):
        _l.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, idxChannel, node, amplitude)
    def nodeAmplitudeGet(self, idxChannel, node):
        return _l.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, idxChannel, node)

    def nodeModulationInfo(self, idxChannel, node):
        return _l.FDwfAnalogOutNodeAmplitudeInfo(self, idxChannel, node)
    def nodeModulationSet(self, idxChannel, node, modulation):
        _l.FDwfAnalogOutNodeAmplitudeSet(
            self.hdwf, idxChannel, node, modulation)
    def nodeModulationGet(self, idxChannel, node):
        return _l.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, idxChannel, node)

    def nodeOffsetInfo(self, idxChannel, node):
        return _l.FDwfAnalogOutNodeOffsetInfo(self.hdwf, idxChannel, node)
    def nodeOffsetSet(self, idxChannel, node, offset):
        _l.FDwfAnalogOutNodeOffsetSet(self.hdwf, idxChannel, node, offset)
    def nodeOffsetGet(self, idxChannel, node):
        return _l.FDwfAnalogOutNodeOffsetGet(self.hdwf, idxChannel, node)

    def nodeSymmetryInfo(self, idxChannel, node):
        return _l.FDwfAnalogOutNodeSymmetryInfo(self.hdwf, idxChannel, node)
    def nodeSymmetrySet(self,  idxChannel, node, percentageSymmetry):
        _l.FDwfAnalogOutNodeSymmetrySet(
            self.hdwf, idxChannel, node, percentageSymmetry)
    def nodeSymmetryGet(self,  idxChannel, node):
        return _l.FDwfAnalogOutNodeSymmetryGet(self.hdwf, idxChannel, node)

    def nodePhaseInfo(self, idxChannel, node):
        return _l.FDwfAnalogOutNodePhaseInfo(self.hdwf, idxChannel, node)
    def nodePhaseSet(self, idxChannel, node, degreePhase):
        _l.FDwfAnalogOutNodePhaseSet(self.hdwf, idxChannel, node, degreePhase)
    def nodePhaseGet(self, idxChannel, node):
        return _l.FDwfAnalogOutNodePhaseGet(self.hdwf, idxChannel, node)

    def nodeDataInfo(self, idxChannel, node):
        return _l.FDwfAnalogOutNodeDataInfo(self.hdwf, idxChannel, node)
    def nodeDataSet(self, idxChannel, node, rgdData):
        _l.FDwfAnalogOutNodeDataSet(self.hdwf, idxChannel, node, rgdData)

# needed for EExplorer, don't care for ADiscovery
    def customAMFMEnableSet(self, idxChannel, enable):
        _l.FDwfAnalogOutCustomAMFMEnableSet(self.hdwf, idxChannel, enable)
    def customAMFMEnableGet(self, idxChannel):
        return bool(_l.FDwfAnalogOutCustomAMFMEnableGet(self.hdwf, idxChannel))

# Control:
    def __init__(self, idxDevice=-1, idxCfg=None):
        if isinstance(idxDevice, Dwf):
            self.hdwf = idxDevice.hdwf
        else:
            super(DwfAnalogOut, self).__init__(idxDevice, idxCfg)
    def reset(self, idxChannel=-1, parent=False):
        if parent: super(DwfAnalogIn, self).reset()
        _l.FDwfAnalogOutReset(self.hdwf, idxChannel)
    def configure(self, idxChannel, start):
        _l.FDwfAnalogOutConfigure(self.hdwf, idxChannel, start)
    def status(self, idxChannel):
        return self.STATE(_l.FDwfAnalogOutStatus(self.hdwf, idxChannel))
    def nodePlayStatus(self, idxChannel, node):
        return _l.FDwfAnalogOutNodePlayStatus(self.hdwf, idxChannel, node)
    def nodePlayData(self, idxChannel, node, rgdData):
        _l.FDwfAnalogOutNodePlayData(self.hdwf, idxChannel, node, rgdData)

# ANALOG IO INSTRUMENT FUNCTIONS
class DwfAnalogIO(Dwf):
    class TYPE(IntEnum):
        '''analog io channel node types'''
        ENABLE = _l.analogioEnable
        VOLTAGE = _l.analogioVoltage
        CURRENT = _l.analogioCurrent
        POWER = _l.analogioPower
        TEMPERATURE = _l.analogioTemperature

# Control:
    def __init__(self, idxDevice=-1, idxCfg=None):
        if isinstance(idxDevice, Dwf):
            self.hdwf = idxDevice.hdwf
        else:
            super(DwfAnalogIO, self).__init__(idxDevice, idxCfg)
    def reset(self, parent=False):
        if parent: super(DwfAnalogIO, self).reset()
        _l.FDwfAnalogIOReset(self.hdwf)
    def configure(self):
        return _l.FDwfAnalogIOConfigure(self.hdwf)
    def status(self):
        _l.FDwfAnalogIOStatus(self.hdwf)

# Configure:
    def enableInfo(self):
        return bool(_l.FDwfAnalogIOEnableInfo(self.hdwf))
    def enableSet(self, master_enable):
        _l.FDwfAnalogIOEnableSet(self.hdwf, master_enable)
    def enableGet(self):
        return bool(_l.FDwfAnalogIOEnableGet(self.hdwf))
    def enableStatus(self):
        return bool(_l.FDwfAnalogIOEnableStatus(self.hdwf))
    
    def channelCount(self):
        return _l.FDwfAnalogIOChannelCount(self.hdwf)
    def channelName(self, idxChannel):
        return _l.FDwfAnalogIOChannelName(self.hdwf, idxChannel)
    def channelInfo(self, idxChannel):
        return _l.FDwfAnalogIOChannelInfo(self.hdwf, idxChannel)

    def channelNodeName(self, idxChannel, idxNode):
        return _l.FDwfAnalogIOChannelNodeName(self.hdwf, idxChannel, idxNode)
    def channelNodeInfo(self, idxChannel, idxNode):
        result = _l.FDwfAnalogIOChannelNodeInfo(self.hdwf, idxChannel, idxNode)
        if result == 0:
            return None
        return self.TYPE(result)
    def channelNodeSetInfo(self, idxChannel, idxNode):
        return _l.FDwfAnalogIOChannelNodeSetInfo(self.hdwf, idxChannel, idxNode)
    def channelNodeSet(self, idxChannel, idxNode, value):
        _l.FDwfAnalogIOChannelNodeSet(self.hdwf, idxChannel, idxNode, value)
    def channelNodeGet(self, idxChannel, idxNode):
        return _l.FDwfAnalogIOChannelNodeGet(self.hdwf, idxChannel, idxNode)
    def channelNodeStatusInfo(self, idxChannel, idxNode):
        return _l.FDwfAnalogIOChannelNodeStatusInfo(
            self.hdwf, idxChannel, idxNode)
    def channelNodeStatus(self, idxChannel, idxNode):
        return _l.FDwfAnalogIOChannelNodeStatus(self.hdwf, idxChannel, idxNode)

# DIGITAL IO INSTRUMENT FUNCTIONS
class DwfDigitalIO(Dwf):
# Control:
    def __init__(self, idxDevice=-1, idxCfg=None):
        if isinstance(idxDevice, Dwf):
            self.hdwf = idxDevice.hdwf
        else:
            super(DwfDigitalIO, self).__init__(idxDevice, idxCfg)
    def reset(self, parent=False):
        if parent: super(DwfDigitalIO, self).reset()
        _l.FDwfDigitalIOReset(sef_l.hdwf)
    def configure(self):
        return _l.FDwfDigitalIOConfigure(self.hdwf)
    def status(self):
        _l.FDwfDigitalIOStatus(self.hdwf)

# Configure:
    def outputEnableInfo(self):
        return _l.FDwfDigitalIOOutputEnableInfo(self)
    def outputEnableSet(self, output_enable):
        _l.FDwfDigitalIOOutputEnableSet(self.hdwf, output_enable)
    def outputEnableGet(self):
        return _l.FDwfDigitalIOOutputEnableGet(self.hdwf)
    
    def outputInfo(self):
        return _l.FDwfDigitalIOOutputInfo(self.hdwf)
    def outputSet(self, output):
        _l.FDwfDigitalIOOutputSet(self.hdwf, output)
    def outputGet(self):
        return _l.FDwfDigitalIOOutputSet(self.hdwf)

    def inputInfo(self):
        return _l.FDwfDigitalIOInputInfo(self.hdwf)
    def inputStatus(self):
        return _l.FDwfDigitalIOInputStatus(self.hdwf)

# DIGITAL IN INSTRUMENT FUNCTIONS
class DwfDigitalIn(Dwf):
    class ACQMODE(IntEnum):
        '''acquisition modes'''
        SINGLE = _l.acqmodeSingle
        SCAN_SHIFT = _l.acqmodeScanShift
        SCAN_SCREEN = _l.acqmodeScanScreen
        RECORD = _l.acqmodeRecord

    class CLOCKSOURCE(IntEnum):
        INTERNAL = _l.DwfDigitalInClockSourceInternal
        EXTERNAL = _l.DwfDigitalInClockSourceExternal

    class SAMPLEMODE(IntEnum):
        SIMPLE = _l.DwfDigitalInSampleModeSimple
        # alternate samples: noise|sample|noise|sample|... 
        # where noise is more than 1 transition between 2 samples
        NOISE = _l.DwfDigitalInSampleModeNoise
    
# Control and status:
    def __init__(self, idxDevice=-1, idxCfg=None):
        if isinstance(idxDevice, Dwf):
            self.hdwf = idxDevice.hdwf
        else:
            super(DwfDigitalIn, self).__init__(idxDevice, idxCfg)
    def reset(self, parent=False):
        if parent: super(DwfDigitalIn, self).reset()
        _l.FDwfDigitalInReset(self.hdwf)
    def configure(self, reconfigure, start):
        return _l.FDwfDigitalInConfigure(self.hdwf, reconfigure, start)
    def status(self, read_data):
        return self.STATE(_l.FDwfDigitalInStatus(self.hdwf, read_data))
    def statusSamplesLeft(self):
        return _l.FDwfDigitalInStatusSamplesLeft(self.hdwf)
    def statusSamplesValid(self):
        return _l.FDwfDigitalInStatusSamplesValid(self.hdwf)
    def statusIndexWrite(self):
        return _l.FDwfDigitalInStatusIndexWrite(self.hdwf)
    def statusAutoTriggered(self):
        return bool(_l.FDwfDigitalInStatusAutoTriggered(self.hdwf))
    def statusData(self, count):
        bit_width = self.sampleFormatGet()
        countOfDataBytes = count * (bit_width // 8)
        data = _l.FDwfDigitalInStatusData(self.hdwf, countOfDataBytes)
        if bit_width == 16:
            data = [ (data[2*i+1] & 0xff) << 8 | (data[2*i] & 0xff)
                     for i in range(len(data) // 2) ]
        elif bit_width == 32:
            data = [ (data[4*i+3] & 0xff) << 24 | ((data[4*i+2] & 0xff) << 16) |
                     ((data[4*i+1] & 0xff) << 8) | (data[4*i] & 0xff)
                     for i in range(len(data) // 4) ]
        return data
    def statusRecord(self):
        return _l.FDwfDigitalInStatusRecord(self.hdwf)

# Acquistion configuration:
    def internalClockInfo(self):
        return _l.FDwfDigitalInInternalClockInfo(self.hdwf)

    def clockSourceInfo(self):
        return _make_set(
            _l.FDwfDigitalInClockSourceInfo(self.hdwf), self.CLOCKSOURCE)
    def clockSourceSet(self, clock_source):
        _l.FDwfDigitalInClockSourceSet(self.hdwf, clock_source)
    def clockSourceGet(self, clock_source):
        return self.CLOCKSOURCE(_l.FDwfDigitalInClockSourceGet(self.hdwf))

    def dividerInfo(self):
        return _l.FDwfDigitalInDividerInfo(self.hdwf)
    def dividerSet(self, div):
        _l.FDwfDigitalInDividerSet(self.hdwf, div)
    def dividerGet(self, div):
        return _l.FDwfDigitalInDividerGet(self.hdwf)

    def bitsInfo(self):
        '''Returns the number of Digital In bits'''
        return _l.FDwfDigitalInBitsInfo(self.hdwf)
    def sampleFormatSet(self, bits):
        '''valid options 8/16/32'''
        _l.FDwfDigitalInSampleFormatSet(self.hdwf, bits)
    def sampleFormatGet(self):
        return _l.FDwfDigitalInSampleFormatGet(self.hdwf)

    def bufferSizeInfo(self):
        return _l.FDwfDigitalInBufferSizeInfo(self.hdwf)
    def bufferSizeSet(self, size):
        _l.FDwfDigitalInBufferSizeSet(self.hdwf, size)
    def bufferSizeGet(self, size):
        return _l.FDwfDigitalInBufferSizeGet(self.hdwf)

    def sampleModeInfo(self):
        return _make_set(
            _l.FDwfDigitalInSampleModeInfo(self.hdwf), self.SAMPLEMODE)
    def sampleModeSet(self, sample_mode):
        _l.FDwfDigitalInSampleModeSet(self.hdwf, sample_mode)
    def sampleModeGet(self):
        return self.SAMPLEMODE(_l.FDwfDigitalInSampleModeGet(self.hdwf))

    def acquisitionModeInfo(self):
        return _make_set(
            _l.FDwfDigitalInAcquisitionModeInfo(self.hdwf), self.ACQMODE)
    def acquisitionModeSet(self, acqmode):
        _l.FDwfDigitalInAcquisitionModeSet(self.hdwf, acqmode)
    def acquisitionModeGet(self):
        return self.ACQMODE(_l.FDwfDigitalInAcquisitionModeGet(self.hdwf))

# Trigger configuration:
    def triggerSourceInfo(self):
        '''use IsBitSet'''
        return _make_set(
            _l.FDwfDigitalInTriggerSourceInfo(self.hdwf), self.TRIGSRC)
    def triggerSourceSet(self, trigsrc):
        _l.FDwfDigitalInTriggerSourceSet(self.hdwf, trigsrc)
    def triggerSourceGet(self):
        return self.TRIGSRC(_l.FDwfDigitalInTriggerSourceGet(self.hdwf))

    def triggerPositionInfo(self):
        return _l.FDwfDigitalInTriggerPositionInfo(self.hdwf)
    def triggerPositionSet(self, samples_after_trigger):
        _l.FDwfDigitalInTriggerPositionSet(self.hdwf, samples_after_trigger)
    def triggerPositionGet(self):
        return _l.FDwfDigitalInTriggerPositionGet(self.hdwf)

    def triggerAutoTimeoutInfo(self):
        return _l.FDwfDigitalInTriggerAutoTimeoutInfo(self.hdwf)
    def triggerAutoTimeoutSet(self, secTimeout):
        _l.FDwfDigitalInTriggerAutoTimeoutSet(self.hdwf, secTimeout)
    def triggerAutoTimeoutGet(self):
        return _l.FDwfDigitalInTriggerAutoTimeoutGet(self.hdwf)

    def triggerInfo(self):
        return _l.FDwfDigitalInTriggerInfo(self.hdwf)
    # the logic for trigger bits: Low and High and (Rise or Fall)
    # bits set in Rise and Fall means any edge
    def triggerSet(self, level_low, level_high, edge_rise, edge_fall):
        _l.FDwfDigitalInTriggerSet(
            self.hdwf, level_low, level_high, edge_rise, edge_fall)
    def triggerGet(self):
        return _l.FDwfDigitalInTriggerGet(self.hdwf)

# DIGITAL OUT INSTRUMENT FUNCTIONS
class DwfDigitalOut(Dwf):

    class OUTPUT(IntEnum):
        PUSH_PULL = _l.DwfDigitalOutOutputPushPull
        OPEN_DRAIN = _l.DwfDigitalOutOutputOpenDrain
        OPEN_SOURCE = _l.DwfDigitalOutOutputOpenSource
        TRISTATE = _l.DwfDigitalOutOutputThreeState # for custom and random

    class TYPE(IntEnum):
        PULSE = _l.DwfDigitalOutTypePulse
        CUSTOM = _l.DwfDigitalOutTypeCustom
        RANDOM = _l.DwfDigitalOutTypeRandom

    class IDLE(IntEnum):
        INIT = _l.DwfDigitalOutIdleInit
        LOW = _l.DwfDigitalOutIdleLow
        HIGH = _l.DwfDigitalOutIdleHigh
        HiZ = _l.DwfDigitalOutIdleZet

# Control:
    def __init__(self, idxDevice=-1, idxCfg=None):
        if isinstance(idxDevice, Dwf):
            self.hdwf = idxDevice.hdwf
        else:
            super(DwfDigitalOut, self).__init__(idxDevice, idxCfg)
    def reset(self, parent=False):
        if parent: super(DwfDigitalOut, self).reset()
        return _l.FDwfDigitalOutReset(self.hdwf)
    def configure(self, start):
        _l.FDwfDigitalOutConfigure(self.hdwf, start)
    def status(self):
        return self.STATE(_l.FDwfDigitalOutStatus(self.hdwf))

# Configuration:
    def internalClockInfo(self):
        return _l.FDwfDigitalOutInternalClockInfo(self.hdwf)

    def triggerSourceInfo(self):
        return _make_set(
            _l.FDwfDigitalOutTriggerSourceInfo(self.hdwf), self.TRIGSRC)
    def triggerSourceSet(self, trigsrc):
        _l.FDwfDigitalOutTriggerSourceSet(self.hdwf, trigsrc)
    def triggerSourceGet(self, trigsrc):
        return self.TRIGSRC(_l.FDwfDigitalOutTriggerSourceGet(self.hdwf))

    def runInfo(self):
        return _l.FDwfDigitalOutRunInfo(self.hdwf)
    def runSet(self, secRun):
        _l.FDwfDigitalOutRunSet(self.hdwf, secRun)
    def runGet(self):
        return _l.FDwfDigitalOutRunGet(self.hdwf)
    def runStatus(self):
        return _l.FDwfDigitalOutRunStatus(self.hdwf)

    def waitInfo(self):
        return _l.FDwfDigitalOutWaitInfo(self.hdwf)
    def waitSet(self, secWait):
        _l.FDwfDigitalOutWaitSet(self.hdwf, secWait)
    def waitGet(self):
        return _l.FDwfDigitalOutWaitGet(self.hdwf)

    def repeatInfo(self):
        return _l.FDwfDigitalOutRepeatInfo(self.hdwf)
    def repeatSet(self, repeat):
        _l.FDwfDigitalOutRepeatSet(self.hdwf, repeat)
    def repeatGet(self):
        return _l.FDwfDigitalOutRepeatGet(self.hdwf)
    def repeatStatus(self):
        return _l.FDwfDigitalOutRepeatStatus(self.hdwf)

    def repeatTriggerSet(self, repeat_trigger):
        _l.FDwfDigitalOutRepeatTriggerSet(self.hdwf, repeat_trigger)
    def repeatTriggerGet(self):
        return _l.FDwfDigitalOutRepeatTriggerGet(self.hdwf)

    def channelCount(self): #renamed
        return _l.FDwfDigitalOutCount(self.hdwf)
    def enableSet(self, idxChannel, enable):
        _l.FDwfDigitalOutEnableSet(self.hdwf, idxChannel, enable)
    def enableGet(self, idxChannel):
        return bool(_l.FDwfDigitalOutEnableGet(self.hdwf, idxChannel))

    def outputInfo(self, idxChannel):
        return _make_set(
            _l.FDwfDigitalOutOutputInfo(self.hdwf, idxChannel), self.OUTPUT)
    def outputSet(self, idxChannel, output_mode):
        _l.FDwfDigitalOutOutputSet(self.hdwf, idxChannel, output_mode)
    def outputGet(self, idxChannel):
        return self.OUTPUT(_l.FDwfDigitalOutOutputGet(self.hdwf, idxChannel))

    def typeInfo(self, idxChannel):
        return _make_set(
            _l.FDwfDigitalOutTypeInfo(sef.hdwf, idxChannel), self.TYPE)
    def typeSet(self, idxChannel, output_type):
        _l.FDwfDigitalOutTypeSet(self.hdwf, idxChannel, output_type)
    def typeGet(self, idxChannel):
        return self.TYPE(_l.FDwfDigitalOutTypeGet(self.hdwf, idxChannel))

    def idleInfo(self, idxChannel):
        return _make_set(
            _l.FDwfDigitalOutIdleInfo(self.hdwf, idxChannel), self.IDLE)
    def idleSet(self, idxChannel, idle_mode):
        _l.FDwfDigitalOutIdleSet(self.hdwf, idxChannel, idle_mode)
    def idleGet(self, idxChannel):
        return self.IDLE(_l.FDwfDigitalOutIdleGet(self.hdwf, idxChannel))

    def dividerInfo(self, idxChannel):
        return _l.FDwfDigitalOutDividerInfo(self.hdwf, idxChannel)
    def dividerInitSet(self, idxChannel, init):
        _l.FDwfDigitalOutDividerInitSet(self.hdwf, idxChannel, init)
    def dividerInitGet(self, idxChannel):
        return _l.FDwfDigitalOutDividerInitGet(self.hdwf, idxChannel)
    def dividerSet(self, idxChannel, value):
        _l.FDwfDigitalOutDividerSet(self.hdwf, idxChannel, value)
    def dividerGet(self, idxChannel):
        return _l.FDwfDigitalOutDividerGet(self.hdwf, idxChannel)

    def counterInfo(self, idxChannel):
        return _l.FDwfDigitalOutCounterInfo(self.hdwf, idxChannel)
    def counterInitSet(self, idxChannel, start_high, init):
        _l.FDwfDigitalOutCounterInitSet(self.hdwf, idxChannel, start_high, init)
    def counterInitGet(self, idxChannel):
        return _l.FDwfDigitalOutCounterInitGet(self.hdwf, idxChannel)
    def counterSet(self, idxChannel, low, high):
        _l.FDwfDigitalOutCounterSet(self.hdwf, idxChannel, low, high)
    def counterGet(self, idxChannel):
        return _l.FDwfDigitalOutCounterGet(self.hdwf, idxChannel)

    def dataInfo(self, idxChannel):
        return _l.FDwfDigitalOutDataInfo(self.hdwf, idxChannel)
    def dataSet(self, idxChannel, rgBits):
        _l.FDwfDigitalOutDataSet(self.hdwf, idxChannel, rgBits)

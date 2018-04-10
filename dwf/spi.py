#! /usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum
import time

from . import api as _api

class SPIMode(IntEnum):
    MODE_0 = 0
    MODE_1 = 1
    MODE_2 = 2
    MODE_3 = 3

    POL_POS = 0x00
    POL_NEG = 0x02
    PHA_LATCH = 0x00
    PHA_SHIFT = 0x01

class SPIMaster(object):
    
    def __init__(self, mode, freq, SCLK, MISO=None, MOSI=None, SS=None,
                 lsb_first=False, idxDevice=-1, idxCfg=None):
        if MISO is None and MOSI is None:
            raise Exception("Please set MISO and/or MOSI pin number")
        
        if isinstance(idxDevice, _api.DwfDigitalIO):
            self._dev = idxDeivce
        else:
            self._dev = _api.DwfDigitalIO(idxDevice, idxCfg)
        self.mode = mode
        self.freq = freq
        self.lsb_first = lsb_first
        self.SCLK_bit = 1 << SCLK
        if SS is None:
            self.SS_bit = None
        else:
            self.SS_bit = 1 << SS
        self.MOSI_bit = None
        self.MISO_bit = None
        
        self.read = self._unsupported
        self.write = self._unsupported
        self.readwrite = self._unsupported
        if MISO is not None:
            self.MISO_bit = 1 << MISO
            self._bit_readwrite = _bit_readwrite_ronly
            if self.lsb_first:
                self.read = self._read_lsbfirst
            else:
                self.read = self._read_msbfirst
            if MOSI is not None:
                self.MOSI_bit = 1 << MOSI
                self._bit_readwrite = _bit_readwrite_both
                if self.lsb_first:
                    self.write = self._write_lsbfirst
                    self.readwrite = self._readwrite_lsbfirst
                else:
                    self.write = self._write_msbfirst
                    self.readwrite = self._readwrite_msbfirst
        elif MOSI is not None:
            self.MOSI_bit = 1 << MOSI
            self._bit_readwrite = _bit_readwrite_wonly
            if self.lsb_first:
                self.write = self._write_lsbfirst
            else:
                self.write = self._write_msbfirst

        output = self.SCLK_bit
        if self.SS_bit is not None:
            output |= self.SS_bit
        if self.MOSI_bit is not None:
            output |= self.MOSI_bit
        input = 0x00
        if self.MISO_bit is not None:
            input |= self.MISO_bit
        
        enable = self._dev.outputEnableGet()
        self._dev.outputEnableSet((enable & ~input) | output)
        
        self._set_mode(self.mode)
        
        self.end()

    def _set_mode(self, mode):
        if mode & SPIMode.POL_NEG != 0:
            self._sclk_assert = self._sclk_neg
            self._sclk_negate = self._sclk_pos
        else:
            self._sclk_assert = self._sclk_pos
            self._sclk_negate = self._sclk_neg
        if mode & SPIMode.PHA_SHIFT != 0:
            self._rw_onebit = self._rw_onebit_shift
        else:
            self._rw_onebit = self._rw_onebit_latch

    def _bit_readwrite_ronly(self, bit):
        return (self._buf & self.MISO_bit) != 0
            
    def _bit_readwrite_wonly(self, bit):
        if bit:
            self._buf |= self.MOSI_bit
        else:
            self._buf &= ~self.MOSI_bit
            
    def _bit_readwrite_both(self, bit):
        if bit:
            self._buf |= self.MOSI_bit
        else:
            self._buf &= ~self.MOSI_bit
        return (self._buf & self.MISO_bit) != 0
            
    def _rw_onbit_shift(self, bit):
        self._buf = self._dev.outputGet()
        self._sclk_assert()
        self._dev.outputSet(self._buf)
        self._wait()
        
        self._buf = self._dev.outputGet()
        out = self._bit_readwrite(bit)
        self._sclk_negate()
        self._dev.outputSet(self._buf)
        self._wait()
        
        return out
    
    def _rw_onbit_latch(self, bit):
        self._buf = self._dev.outputGet()
        out = self._bit_readwrite(bit)
        self._sclk_assert()
        self._dev.outputSet(self._buf)
        self._wait()
        
        self._buf = self._dev.outputGet()
        self._sclk_negate()
        self._dev.outputSet(self._buf)
        self._wait()
        return out

    def _sclk_pos(self):
        self._buf |= self.SCLK_bit
    
    def _sclk_neg(self):
        self._buf &= ~self.SCLK_bit
            
    def _read_msbfirst(self, wordsize, datalen):
        results = []
        for l in range(datalen):
            value = 0
            mask = 0x01 << (wordsize-1)
            for i in range(wordsize):
                if self._rw_onebit(0):
                    value |= mask
                mask >>= 1
            results.append(value)
        return value
    
    def _read_lsbfirst(self, wordsize, datalen):
        results = []
        for l in range(datalen):
            value = 0
            mask = 0x01
            for i in range(wordsize):
                if self._rw_onebit(0):
                    value |= mask
                mask <<= 1
            results.append(value)
        return value

    def _write_msbfirst(self, wordsize, data):
        for v in data:
            mask = 0x01 << (wordsize -1)
            for i in range(wordsize):
                self._rw_onebit(v & mask != 0)
                mask >>= 1

    def _write_lsbfirst(self, wordsize, data):
        for v in data:
            mask = 0x01
            for i in range(wordsize):
                self._rw_onebit(v & mask != 0)
                mask <<= 1

    def _readwrite_msbfirst(self, wordsize, data):
        results = []
        for v in data:
            value = 0
            mask = 0x01 << (wordsize -1)
            for i in range(wordsize):
                if self._rw_onebit(v & mask != 0):
                    value |= mask
                mask >>= 1
            results.append(value)
        return results

    def _readwrite_lsbfirst(self, wordsize, data):
        results = []
        for v in data:
            value = 0
            mask = 0x01
            for i in range(wordsize):
                if self._rw_onebit(v & mask != 0):
                    value |= mask
                mask <<= 1
            results.append(value)
        return results

    def _unsupported(self, *args, **kwargs):
        raise NotImpelemented()

    def _wait(self):
        time.sleep(0.5/self.freq)
    
    def begin(self):
        self._buf = self._dev.outputGet()
        if self.SS_bit:
            self._buf |= self.SS_bit
        self._dev.outputSet(self._buf)

    def end(self):
        self._buf = self._dev.outputGet()
        if self.SS_bit:
            self._buf &= ~self.SS_bit
        self._sclk_negate()
        self._dev.outputSet(self._buf)
        

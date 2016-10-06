#! /usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
import time

from . import api as _api

class _I2C_IO(_api.DwfDigitalIO):
    _BIT_NONE = 0x00
    _BIT_SCL = 0x01
    _BIT_SDA = 0x02
    _BIT_BOTH = 0x03

    def __init__(self, SCL, SDA, idxDevice=-1, idxCfg=None):
        if isinstance(idxDevice, _api.DwfDigitalIO):
            self._dev = idxDeivce
        else:
            self._dev = _api.DwfDigitalIO(idxDevice, idxCfg)
        self.scl_bit = 0x01 << SCL
        self.sda_bit = 0x01 << SDA
        self._set_scl(True)
        self._set_sda(True)

    def _get_both(self):
        result = 0
        st = self._dev.inputStatus()
        if (st & self.scl_bit) != 0:
            result |= self._BIT_SCL
        if (st & self.sda_bit) != 0:
            result |= self._BIT_SDA
        return result
    
    def _get_scl(self):
        return (self._dev.inputStatus() & self.scl_bit) != 0
    
    def _get_sda(self):
        return (self._dev.inputStatus() & self.sda_bit) != 0
    
    def _set_scl(self, hiz):
        value = self._dev.outputEnableGet()
        if hiz:
            value &= ~self.scl_bit
        else:
            value |= self.scl_bit
        self._dev.outputEnableSet(value)
        
    def _set_sda(self, hiz):
        value = self._dev.outputEnableGet()
        if hiz:
            value &= ~self.sda_bit
        else:
            value |= self.sda_bit
        self._dev.outputEnableSet(value)
        

class I2CMaster(_I2C_IO):
    
    def __init__(self, *args, **kwargs):
        super(I2CMaseter, self).__init__(*args, **kwargs):
    
    def _wait(self):
        # for 100kbps (half of bps)
        time.sleep(5e-6)
    
    def make_start_condition(self):
        self._set_scl(True)
        self._wait()
        self._set_sda(False)
        self._wait()
        self._set_scl(False)
    
    def make_stop_condition(self):
        self._set_scl(False)
        self._wait()
        self._set_sda(True)
        self._wait()
        self._set_scl(True)
        
    def make_restart_condition(self):
        self.stop_condition()
        self.start_condition()

    def make_send_addr(self, addr, write=False, force_14bit=False):
        if addr >= 0x80 or force_14bit:
            data1 = 0xf0 | ((addr >> 7) & 0x06)
            if write:
                data1 |= 0x01
            ack = self.make_send_data(data)
            return self.make_send_data(addr & 0xff) and ack
        else:
            data = (addr << 1) & 0xFe
            if write:
                data |= 0x01
            return self.make_send_data(data)
    
    def send_byte(self, data):
        mask = 0x80
        while mask != 0:
            self._set_sda((data & mask) != 0)
            self._wait()
            self._set_scl(True)
            while not self._get_scl():
                pass
            self._wait()
            self._set_scl(False)
            mask >>= 1

        # check ack
        self._set_sda(False)
        self._wait()
        self._set_scl(True)
        while not self._get_scl():
            pass
        ack = self._get_sda()
        self._wait()
        self._set_scl(False)
        return ack
    
    def recv_byte(self, cont=False):
        mask = 0x80
        data = 0
        while mask != 0:
            self._wait()
            self._set_scl(True)
            while not self._get_scl():
                pass
            if self._get_sda():
                data |= mask
            self._wait()
            self._set_scl(False)
            mask >>= 1

        # send ack
        self._set_sda(cont)
        self._wait()
        self._set_scl(True)
        while not self._get_scl():
            pass
        self._wait()
        self._set_scl(False)
        return data
    
    def send_data(self, addr, data):
        self.make_start_condition()
        self.send_addr(addr, write=True)
        for d in data:
            self.send_byte(d)
        self.make_stop_condition()

    def recv_data(self, addr, num=1):
        result = []
        self.make_start_condition()
        self.send_addr(addr, write=False)
        for i in range(num-1):
            result.append(self.recv_byte(cont=True))
        result.append(self.recv_data(cont=False))
        self.make_stop_condition()
        return result

class I2CSlave(_I2C_IO):
    
    def __init__(self, *args, **kwargs):
        super(I2CMaseter, self).__init__(*args, **kwargs):
        self.slave_address = 0x00
        self.terminate = False
        self._send_data_handler = None
        self._recv_data_handler = None
    
    def _wait(self):
        # for 100kbps (half of bps)
        time.sleep(5e-6)
    
    def wait_start_condition(self):
        while True:
            while self._get_both() != self._BIT_BOTH:
                self._wait()
            while True:
                s = self._get_both()
                if s != self._BIT_BOTH:
                    break
                self._wait()
            if s == self._SCL:
                return
    
    def is_stop_condition(self):
        while True:
            s = self._get_both()
            if s != self._BIT_SCL:
                break
            self._wait()
        return s == self._BIT_BOTH
    
    def receive_byte(self, check_address=False):
        bits = [ None ] * 8
        for i in range(8):
            while self._get_scl() == True:
                self._wait()
            self._set_scl(False)
            bits[i] = self._get_sda()
            self._set_scl(True)
            while self._get_scl() == False:
                self._wait()
        if check_address:
            pass
        
        while self._get_scl() == True:
            self._wait()
        self._set_scl(False)
        self._set_sda(False)
        self._set_scl(True)
        while self._get_scl() == False:
            self._wait()
        self._set_sda(True)
        return bits

    def send_byte(self, data):
        mask = 0x80
        for i in range(8):
            while self._get_scl() == True:
                self._wait()
            self._set_scl(False)
            self._set_sda((data & mask) != 0)
            self._set_scl(True)
            while self._get_scl() == False:
                self._wait()
        
        while self._get_scl() == True:
            self._wait()
        self._set_scl(False)
        cont = self._get_sda()
        self._set_scl(True)
        while self._get_scl() != True:
            self._wait()
        return cont
    
    def set_send_data_handler(self, handler):
        old = self._send_data_handler
        self._send_data_handler = handler
        return old

    def set_recv_data_handler(self, handler):
        old = self._recv_data_handler
        self._recv_data_handler = handler
        return old

    def send_data_handler(self, addr, finish=False):
        if self._send_data_handler is not None:
            self._send_data_handler(addr)
        return 0
    
    def recv_data_handler(self, addr, data):
        if self._recv_data_handler is not None:
            self._recv_data_handler(addr, data)
        # NOP
    
    def do_loop(self):
        self.terminate = False
        while not self.terminate:
            self.wait_start_condition()
            addr = self.receive_byte(check_address=True)
            if (addr >> 1) != self.slave_address:
                continue
            if (addr & 0x01) == 0: # write
                data = []
                while self.is_stop_condition():
                    data.append(self.receive_byte())
                self.recv_data_handler(addr, data)
            else: # read
                cont = True
                while cont:
                    data = self.send_data_handler(addr)
                    cont = self.send_byte(data)
                self.send_data_handler(addr, finish=True)
    
    def do_end(self):
        self.terminate = True

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
        value = self._dev.outputGet()
        self._dev.outputSet(value | self.scl_bit | self.sda_bit)
        self._set_both(scl=1, sda=1)

    def _get_both(self):
        result = 0
        st = self._dev.inputStatus()
        if (st & self.scl_bit) != 0:
            result |= self._BIT_SCL
        if (st & self.sda_bit) != 0:
            result |= self._BIT_SDA
        return result

    def _set_both(self, scl=-1, sda=-1):
        value = self._dev.outputEnableGet()
        if scl == 0:
            value &= ~self.scl_bit
        elif scl > 0:
            value |= self.scl_bit
        if sda == 0:
            value &= ~self.sda_bit
        elif sda > 0:
            value |= self.sda_bit
        self._dev.outputEnableSet(value)
    
class I2CMaster(_I2C_IO):
    
    def __init__(self, *args, **kwargs):
        super(I2CMaster, self).__init__(*args, **kwargs)
    
    def make_start_condition(self):
        self._set_both(scl=1, sda=1)
        self.wait_data()
        self._set_both(sda=0)
    
    def make_stop_condition(self):
        self._set_both(scl=1, sda=0)
        self.wait_data()
        self._set_both(sda=1)
    
    def make_restart_condition(self):
        self.make_start_condition()

    def send_addr(self, addr, write=False, force_14bit=False):
        if addr >= 0x80 or force_14bit:
            data = 0xf0 | ((addr >> 7) & 0x06)
            if write:
                data |= 0x01
            ack = self.send_byte(data)
            return ack and self.send_byte(addr & 0xff)
        else:
            data = (addr << 1) & 0xfe
            if write:
                data |= 0x01
            return self.send_byte(data)

    def wait_data(self):
        while True:
            s = self._get_both()
            if (s & self._BIT_SCL) != 0:
                return (s & self._BIT_SDA) != 0

    def send_byte(self, data):
        # send 8 bits
        for i in range(8):
            self._set_both(scl=0, sda=((data & (0x80 >> i)) != 0))
            self._set_both(scl=1)
            self.wait_data()
        
        # check ack
        self._set_both(sda=0, scl=0)
        self._set_both(scl=1)
        return self.wait_data()
    
    def recv_byte(self, cont=False):
        data = 0
        for i in range(8):
            self._set_both(scl=1)
            if self.wait_data():
                data |= 0x80 >> 1
            self._set_both(scl=0)

        # send ack
        self._set_both(sda=cont)
        self._set_both(scl=1)
        self.wait_data()
        return data
    
    def send_data(self, addr, data, check=True):
        self.make_start_condition()
        if self.send_addr(addr, write=True) and check:
            raise Excption("I2C addr {:x04} is not found".format(addr))
        for d in data:
            if self.send_byte(d) and check:
                raise Excption("I2C send_data {:x02} is failed".format(d))
        self.make_stop_condition()
        
    def recv_data(self, addr, num=1):
        result = []
        self.make_start_condition()
        if self.send_addr(addr, write=False) and check:
            raise Excption("I2C addr {:x04} is not found".format(addr))
        for i in range(num-1):
            result.append(self.recv_byte(cont=True))
        result.append(self.recv_byte(cont=False))
        self.make_stop_condition()
        return result

class I2CSlave(_I2C_IO):
    
    def __init__(self, *args, **kwargs):
        super(I2CMaseter, self).__init__(*args, **kwargs)
        self.slave_address = 0x00
        self.terminate = False
        self._send_data_handler = None
        self._recv_data_handler = None
    
    def wait_start_condition(self):
        while True:
            while True:
                if self.terminate: return False
                if self._get_both() != self._BIT_BOTH:
                    break
            while True:
                if self.terminate: return False
                s = self._get_both()
                if s != self._BIT_SCL:
                    return True
                if s != self._BIT_BOTH:
                    break
    
    def is_stop_condition(self):
        while True:
            s = self._get_both()
            if s != self._BIT_SCL:
                break
        return s == self._BIT_BOTH
    
    def wait_clk(self, scl):
        while (self._get_both() & self._BIT_SCL) == scl:
            return (self._get_both() & self._BIT_SDA) != 0

    def receive_byte(self, check_address=False):
        data = 0
        self.wait_clk(scl=0)
        for i in range(8):
            if self.wait_clk(scl=1):
                data |= 0x80 >> i
            self.wait_clk(scl=0)
        if check_address and self.slave_address != (data >> 1):
            return None
        
        self._set_both(sda=0)
        self.wait_clk(scl=1)
        self._set_both(sda=1)
        return bits

    def send_byte(self, data):
        for i in range(8):
            self.wait_clk(scl=0)
            self._set_both(sda=(data & (0x80 >> i)) != 0)
            self.wait_clk(scl=1)

        self._set_both(sda=0)
        cont = (self._get_both() & self._SDA_BIT) != 0
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
            if not self.wait_start_condition():
                break
            addr = self.receive_byte(check_address=True)
            if addr is None:
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

#
#
#

from threading import Thread
from dwf.i2c import I2CSlave

I2C_ADDRESS = 0x33

class I2CSlaveThread(Thread):
    def __init__(self):
        self.i2c = I2CSlave(SCL=0, SDA=1)
        self.i2c.slave_address = I2C_ADDRESS
        self.i2c.set_send_data_handler(self.send_data_handler)
        self.i2c.set_recv_data_handler(self.recv_data_handler)
        self.reg_data = [0] * 256
        self.regaddr_ptr = 0

    def __del__(self):
        if self.i2c is not None:
            self.stop()
    
    def run(self):
        self.i2c.do_loop()
    
    def stop(self):
        self.i2c.terminate()
        while self.i2c.is_alive():
            pass
        self.i2c = None

    def send_data_handler(self, addr, finish=False):
        if not finish:
            data = self.reg_data[self.regaddr_ptr]
            self.regaddr_ptr += 1
            if self.regaddr_ptr >= len(self.reg_data):
                self.regadr_ptr = 0
            return data
    
    def recv_data_handler(self, addr, data):
        self.regaddr_ptr = data[0]
        for d in data[1:]:
            self.reg_data[self.regaddr_ptr] = d
            self.regaddr_ptr += 1
            if self.regaddr_ptr >= len(self.reg_data):
                self.regadr_ptr = 0

th = I2CSlaveThread()
th.start()


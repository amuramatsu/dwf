#
#
#

from dwf.i2c import I2CMaster

I2C_ADDRESS = 0x33

i2c = I2CMaster(SCL=0, SDA=1)
i2c.send_data(I2C_ADDRESS, [0x33, 0x00, 0x22])

i2c.send_data(I2C_ADDRESS, [0x00])
data = i2c.recv_data(I2C_ADDRESS, 6)

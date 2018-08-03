#
#
#

from dwf.spi import SPIMaster, SPIMode
import time


spi = SPIMaster(SPIMode.MODE_0, freq=100e3, SCLK=0, MISO=1, MOSI=2, SS=3)
time.sleep(2)
spi.begin()
result = spi.readwrite(8, [0x33, 0x10])
spi.end()
print(result)

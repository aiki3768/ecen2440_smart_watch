import machine
from machine import I2C
from machine import Pin

i2c = I2C(-1,scl=Pin(21),sda=Pin(22))

print(i2c.scan())


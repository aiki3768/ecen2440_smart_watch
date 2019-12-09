import machine
import clock
import interrupt
import time
import ssd1306
import imu20948
import scipy
from machine import Pin, RTC, I2C
from time import sleep
from imu20948 import ICM20948

button = False

def handle_interrupt(p19):
    global button
    button = True

def print_time():
    currenttime = rtc.datetime()# gets the time
    oled.fill(0)
    oled.text('time:',40,0)
    oled.text(str(currenttime[4]),35,10)
    oled.text(':', 50, 10)
    oled.text(str(currenttime[5]),58,10)
    oled.text(':', 75, 10)
    oled.text(str(currenttime[6]),81,10) # puts time in string form and prints
    
def sdelay(time):
    initial = rtc.datetime()
    seconds = (initial[6])
    while True:
        print_time()
        print_Gyro()
        oled.show()
        now = rtc.datetime()
        now_sec = (now[6])
        if (now_sec - seconds >= time):
            break
        
def print_Gyro():
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
    oled.text('Gyroscope:', 25, 35)
    oled.text(str(gx), 25, 45)
    return gx

p19 = Pin(19, Pin.IN)
p18 = Pin(18, Pin.OUT)
p19.irq(trigger = Pin.IRQ_RISING, handler = handle_interrupt)

i2c = I2C(-1, scl=Pin(21), sda=Pin(22)) #sets I2C bus at pins 22 and 21
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c) #oled object of class SSD1306
rtc = RTC()
rtc.datetime((2019,1,1,0,11,20,0,0)) #2019 January first zero hours zero seconds ect
        
imu = ICM20948()

while True:
    if button:
        print('interrupt')
        p18.on()
        sdelay(3)
        p18.off()
        button = False
    print_time()
    gx = print_Gyro()
    oled.show()
    
#!/usr/bin/python

import time
import serial
import aqi

ser = serial.Serial(
    port = '/dev/ttyAMA0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1,
)
print(ser.name)


def calcAQI(u):
    if u > 0.0 and u <= 12.0:
        AQIu = 50.0 *u / 12.0
    elif u <= 35.4:
        AQIu = 50 + (50.0*(u-12.0)/23.5)
    elif u <= 55.4:
        AQIu = 100 + (50.0 * (u-35.4) / 20.0)
    elif u <= 150.4:
        AQIu = 150 + (50.0 * (u-55.4) / 95.0)
    elif u <= 250.4:
        AQIu = 200 + (u-150.4)
    elif u <= 350.4:
        AQIu = 300 + (u-250.4)
    elif u <= 500:
        AQIu = 400 + (100.0*(u-350.4)/149.6)
    else:
        AQIu = -1

    return AQIu
    

def processPacket(packet):

    print ord(packet[11])
    pm01 = ord(packet[8])<<8|ord(packet[9])
    pm2_5 = ord(packet[10])<<8|ord(packet[11])
    pm10 = ord(packet[12])<<8|ord(packet[13])

    print pm01
    print pm2_5
    print pm10
    print "PM2.5 AQI %d\n" % (calcAQI(pm2_5))

    
while 1:
    x = ser.read()
    if ord(x) == 0x42:
        x = ser.read()
        if ord(x) == 0x4d:
            x = ser.read(30)
            processPacket(x)
            

#!/usr/bin/python3

import time
import serial
import sys
import RPi.GPIO as GPIO
import threading
import urllib.request
import urllib.parse

redPin = 11
greenPin = 13
bluePin = 15

host = "http://192.168.1.201:8000"

aqi_buffer = {}
aqi_buffer['aqi01']=0
aqi_buffer['aqi25']=0
aqi_buffer['aqi10']=0
aqi_buffer['voc']=0

def turnonLED(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)

def turnoffLED(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)

def allOff():
    turnoffLED(redPin)
    turnoffLED(greenPin)
    turnoffLED(bluePin)

def redOn():
    turnonLED(redPin)

def greenOn():
    turnonLED(greenPin)

def blueOn():
    turnonLED(bluePin)

def yellowOn():
    turnonLED(redPin)
    turnonLED(greenPin)

def cyanOn():
    turnonLED(greenPin)
    turnonLED(bluePin)

def magentaOn():
    turnonLED(redPin)
    turnonLED(bluePin)

def whiteOn():
    turnonLED(redPin)
    turnonLED(greenPin)
    turnonLED(bluePin)


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

    pm01 = ord(packet[8])<<8|ord(packet[9])
    pm2_5 = ord(packet[10])<<8|ord(packet[11])
    pm10 = ord(packet[12])<<8|ord(packet[13])
    voc = ord(packet[26])<<8|ord(packet[28])

    print("PM1.0 %d /  PM2.5 %d /  PM10 %d / VOC %d mg/M" % ( pm01, pm2_5, pm10, voc ))
    aqi = calcAQI(pm2_5)

    print("PM2.5 AQI %d\n" % (aqi))

    aqi_buffer['aqi01'] = pm01
    aqi_buffer['aqi25'] = pm2_5
    aqi_buffer['aqi10'] = pm10
    aqi_buffer['voc'] = voc
    
    allOff()
    
    if aqi > 0 and aqi <= 50:
        greenOn()
    elif aqi > 50 and aqi <=100:
        yellowOn()
    elif aqi > 100 and aqi <= 150:
        redOn()
    elif aqi > 150 and aqi <= 200:
        magentaOn()
    elif aqi > 200:
        blueOn()
        
def verify_checksum(packet):
    checksum = ord(packet[28])<<8 | ord(packet[29])
    datasum = 0
    
    for i in range(28):
        datasum += ord(packet[i])

    datasum += 0x42
    datasum += 0x4d

    if checksum == datasum:
        return True
    else:
        return False

def log_aqi(delay,run_event):
    while run_event.is_set():
        time.sleep(delay)
        log_server_http()

def log_server_http():
    uri = "/polls/logaqi?aqi01=%s&aqi25=%s&aqi10=%s&voc=%s" % ( aqi_buffer['aqi01'], aqi_buffer['aqi25'],aqi_buffer['aqi10'], aqi_buffer['voc'])

    try:
        f = urllib.request.urlopen(host+uri)
    except urllib.request.URLError as e:
        print(e.reason)
        return

    print("Successfully logged to %s" % (host+uri))
    f.close()

def main():

    run_event = threading.Event()
    run_event.set()

    log_thread = threading.Thread(target=log_aqi,args = (10,run_event))
    log_thread.start()
    
    try:
        ser = serial.Serial(
            port = '/dev/ttyAMA0',
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 1,
        )
    except serial.SerialException:
        print("Port open failed")
    try:
        while 1:
            x = ser.read()
            print(type(x))
            if ord(x) == 0x42:
                x = ser.read()
            if ord(x) == 0x4d:
                x = ser.read(30) 
            if verify_checksum(x):
                processPacket(x)
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught")
        run_event.clear()
        log_thread.join()
        print("exiting.... ")

if __name__ == "__main__":
    main()


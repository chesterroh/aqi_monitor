#!/usr/bin/python

import time
import serial
import sys
import RPi.GPIO as GPIO

redPin = 11
greenPin = 13
bluePin = 15

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


allOff()
yellowOn()




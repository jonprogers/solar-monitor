#! /usr/bin/env python

#Library to use Custard PI2 interface board
#J Rogers. 04/2013

import RPi.GPIO as GPIO
import time
import datetime
import sys

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) # set to board addressing

    #set generic GPIO pins
    GPIO.setup(23,GPIO.OUT) #Clock
    GPIO.setup(19,GPIO.OUT) #Data out
    
    #set pins specific for analogue input
    GPIO.setup(21,GPIO.IN) #Data in
    GPIO.setup(24,GPIO.OUT) #Chip enable

    #set pins for analogue output
    GPIO.setup(26,GPIO.OUT) #Chip enable

    #set pins for digital output
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(12,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(15,GPIO.OUT)
    
    #initialise output pin states
    #analogue channels
    GPIO.output(26,True)
    GPIO.output(24,True)
    GPIO.output(23,False)
    GPIO.output(19,True)
    #digital channels
    GPIO.output(11,False)
    GPIO.output(12,False)
    GPIO.output(13,False)
    GPIO.output(15,False)
    
def close():
    GPIO.cleanup()

def dig_out(pin,state):
    if pin in (11,12,13,15):
        if state in (True,False):
            GPIO.output(pin,state)

def ana_in(channel):
    word1=[1,1,channel,1,1]

    GPIO.output(24,False)
    anip=0
    sl=0.002

    for x in range(0,5):
        GPIO.output(19,word1[x])
        time.sleep(sl)
        GPIO.output(23,True)
        time.sleep(sl)
        GPIO.output(23,False)

    for x in range(0,12):
        GPIO.output(23,True)
        time.sleep(sl)
        bit=GPIO.input(21)
        time.sleep(sl)
        GPIO.output(23,False)
        value=bit*2**(12-x-1)
        anip=anip+value
        #print x, bit, value, anip

    GPIO.output(24,True)

    volt=anip*3.3/4096
#    instant=datetime.datetime.now()
#    outstr = str(instant) + ' ' + str(volt)
#    print outstr
    return volt

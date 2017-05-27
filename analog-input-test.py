#! /usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BOARD)

GPIO.setup(24,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(21,GPIO.IN)

GPIO.output(24,True)
GPIO.output(23,False)
GPIO.output(19,True)

word1=[1,1,0,1,1]

lp=0
while lp<1000:
    lp=lp+1
    
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
    outstr = str(lp) + ' ' + str(volt)
    print outstr

GPIO.cleanup()
sys.exit()


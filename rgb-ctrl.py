#! /usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(12,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    GPIO.output(11,True)
    GPIO.output(12,True)
    GPIO.output(13,True)

def ptime():
    localtime = time.localtime()
    timestring = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    return timestring

def test_sequence():
    GPIO.output(11,False)
    time.sleep(0.1)
    GPIO.output(11,True)
    GPIO.output(12,False)
    time.sleep(0.1)
    GPIO.output(12,True)
    GPIO.output(13,False)
    time.sleep(0.1)
    GPIO.output(13,True)

def test_white():
    currenttime = ptime()
    print(currenttime)
    
    y = 5
    while y<40:
        x = 0
        y = y+1
        delay = 0.001
        pause = delay * y
        print pause
        while x < (1000 / y):
            x=x+1
            GPIO.output(11,False)
            time.sleep(pause)
            GPIO.output(11,True)
            GPIO.output(12,False)
            time.sleep(pause)
            GPIO.output(12,True)
            GPIO.output(13,False)
            time.sleep(pause)
            GPIO.output(13,True)

        currenttime = ptime()
        print(currenttime)

def rgb(r,g,b,secs,freq):
    delay = float(1) / freq
    #delay = 0.1
    zero = 0,0,0,0,0,0,0,0,0,0
    one  = 1,0,0,0,0,0,0,0,0,0
    two  = 1,0,0,0,0,1,0,0,0,0
    thr  = 1,0,0,1,0,0,1,0,0,0
    four = 1,0,0,1,0,1,0,0,1,0
    five = 1,0,1,0,1,0,1,0,1,0
    six  = 1,0,1,0,1,1,0,1,0,1
    sev  = 1,0,1,1,0,1,1,0,1,1
    eigh = 1,1,1,1,0,1,1,1,1,0
    nine = 1,1,1,1,0,1,1,1,1,1
    ten  = 1,1,1,1,1,1,1,1,1,1
    pwm = zero, one, two, thr, four, five, six, sev, eigh, nine, ten

    cycles = secs * freq /30
    #cycles = 2
    x = 0
    red = pwm[r]
    #print 'red ' + str(red)
    gre = pwm[g]
    #print 'gre ' + str(gre)
    blu = pwm[b]
    #print 'blu ' + str(blu)
    while x < cycles:
        x=x+1
        for i in range(10):
            #print 'red' + str(red[i]) 
            if red[i] == 1:
                GPIO.output(11,False)

            time.sleep(delay)
            GPIO.output(11,True)
            #print 'gre' + str(gre[i]) 
            if gre[i] == 1:
                GPIO.output(12,False)

            time.sleep(delay)
            GPIO.output(12,True)
            #print 'blu' + str(blu[i]) 
            if blu[i] == 1:
                GPIO.output(13,False)

            time.sleep(delay)
            GPIO.output(13,True)
            
def closedown():
    GPIO.cleanup()

if __name__ == "__main__":
    init()
    test_sequence()
    cycle = (10,9,8,7,6,5,4,3,2,1,0,1,2,3,4,5,6,7,8,9)
    for r in range(0,10,2):
        for g in cycle:
            for b in cycle:
                rgb(r,g,b,0.01,800)

    rgb(10,10,10,5,400)
    closedown()

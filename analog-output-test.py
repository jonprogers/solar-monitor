#! /use/bin/env python

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(26,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)

GPIO.output(26,True)
GPIO.output(23,False)
GPIO.output(19,True)

count=0

word1=[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
word2=[0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1]
word0=[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0]

while count<5:

    GPIO.output(26,False)

    for x in range(0,16):
        GPIO.output(19,word1[x])
        print word1[x]
        time.sleep(0.01)
        GPIO.output(23,True)
        time.sleep(0.01)
        GPIO.output(23,False)

    GPIO.output(26,True)
    time.sleep(5)
    GPIO.output(26,False)

    for x in range(0,16):
        GPIO.output(19,word2[x])
        print word2[x]
        time.sleep(0.01)
        GPIO.output(23,True)
        time.sleep(0.01)
        GPIO.output(23,False)

    GPIO.output(26,True)
    print count
    count=count+1
    time.sleep(5)

GPIO.output(26,False)

for x in range(0,16):
    GPIO.output(19,word0[x])
    print word0[x]
    time.sleep(0.01)
    GPIO.output(23,True)
    time.sleep(0.01)
    GPIO.output(23,False)

GPIO.output(26,True)

GPIO.cleanup()
import sys
sys.exit()

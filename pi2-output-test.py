#! /usr/bin/env python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)

for x in range (0,20):
    GPIO.output(11,True)
    time.sleep(0.2)
    GPIO.output(11,False)
    time.sleep(0.2)

GPIO.cleanup()

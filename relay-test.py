#! /usr/bin/env python
import RPi.GPIO as GPIO
import time
import sys
import MySQLdb as mdb

def ptime():
    localtime = time.localtime()
    timestring = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    return timestring
    
def relay_ctrl(n):
    GPIO.output(11,True)
    GPIO.output(13,True)
    x=0
    while x<n:
        GPIO.output(11,False)
        xf=float(x)
        wait=xf/10
        time.sleep(wait)
        GPIO.output(13,False)
        time.sleep(wait)
        GPIO.output(11,True)
        time.sleep(wait)
        GPIO.output(13,True)
        time.sleep(wait)
        x=x+1
        

if __name__ == "__main__":
    has_run=False
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    relay_ctrl(15)

    GPIO.cleanup()
        

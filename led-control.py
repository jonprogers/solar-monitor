#! /usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys

def ptime():
    localtime = time.localtime()
    timestring = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    return timestring
    
def led_ctrl(n):
    currenttime = ""
    GPIO.setup(11,GPIO.OUT)
    currenttime = ptime()
    print(currenttime)
    x=1
    rev=False
    while x != 0:
        GPIO.output(11,GPIO.HIGH)
        time.sleep(x/100)
        GPIO.output(11,GPIO.LOW)
        time.sleep(x/100)
    #    print (x)
        if x>n:
            rev=True
            print('Turning round')
            
        if rev:
            x=x-1
        else:
            x=x+1

    timeString  = ptime()
    print(timeString)

def edge_detect():
    print('switch pressed')
    led_ctrl(int(sys.argv[1]))

if __name__ == "__main__":
    has_run=False
    GPIO.setmode(GPIO.BOARD)
    #led_ctrl(int(sys.argv[1]))
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(12, GPIO.FALLING)
#    print(has_run)
    GPIO.add_event_detect(13, GPIO.RISING)
#    GPIO.add_event_callback(13, edge_detect)
#    print(has_run)
    while not has_run:
        if GPIO.event_detected(13):
            print('Rising edge has occurred!')
            edge_detect()
            
        if GPIO.event_detected(12):
            has_run=True
            print('end event detected, terminating...')
            
        time.sleep(0.1)

    GPIO.cleanup()


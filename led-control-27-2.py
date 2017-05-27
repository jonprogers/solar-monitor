#! /usr/bin/env python
import RPi.GPIO as GPIO
import time
import sys
import MySQLdb as mdb

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
        xnew=float(x)
        wait = xnew/50
#        print(wait)
        time.sleep(wait)
        GPIO.output(11,GPIO.LOW)
        time.sleep(wait)
#        print (x)
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
    led_ctrl(15)

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

    con = None

#    try:
        
#        con = mdb.connect('localhost', 'jon', 'dbpwd', 'jondb');

#        with con:

#            cur = con.cursor()
#            cur.execute("CREATE TABLE IF NOT EXISTS \
#                Events(Id INT PRIMARY KEY AUTO_INCREMENT,Type VARCHAR(25), Time DATETIME)");
                
    while not has_run:
        if GPIO.event_detected(13):
            currtime = ptime()
            #print(currtime)
            try:
                con = mdb.connect('localhost', 'jon', 'dbpwd', 'jondb');
                with con:
                    cur = con.cursor()
                    add_event = ("INSERT INTO Events(Type,Time) VALUES(%s, %s)")
                    data1 = ('But press', currtime)
                    print(data1)
                    cur.execute(add_event, data1)
                    #con.commit() # can commit data without doing con.close()
                
            finally:        
                if con:    
                    con.close()
                    con = None
                    
            print('Rising edge has occurred!')
            edge_detect()
            
        if GPIO.event_detected(12):
            has_run=True
            currtime = ptime()
            #print(currtime)
            try:
                con = mdb.connect('localhost', 'jon', 'dbpwd', 'jondb');
                with con:
                    cur = con.cursor()
                    add_event = ("INSERT INTO Events(Type,Time) VALUES(%s, %s)")
                    data1 = ('Terminate', currtime)
                    print(data1)
                    cur.execute(add_event, data1)
                    
            finally:        
                if con:    
                    con.close()
                    con = None
                    
            print('end event detected, terminating...')
            
        time.sleep(0.1)
        
    GPIO.cleanup()

#    finally:        
#        if con:    
#            con.close()
#            con = None
            

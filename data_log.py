#!/usr/bin/python
# -*- coding: utf-8 -*-

import cp2
import sys
import time
import datetime
import smtplib
import string

def Email_results(Current, Maxpower, Daygen, Dayuse):
    HOST = "relay.plus.net"
    SUBJECT = "Solar update, generated " + time.strftime("%Y-%m-%d %H:%M", time.localtime())
    TO = "jon.rogers@onodo.co.uk"
    FROM = "pi@onodo.co.uk"
    BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        "Update generated: %s" % time.strftime("%Y-%m-%d %H:%M", time.localtime()),
        "Currently generating : %s W" % Current,
        "Peak so far today    : %s W" % Maxpower,
        "Generation today     : %s Wh" % Daygen,
        "Useage today         : %s Wh" % Dayuse,
        ), "\r\n")
    server = smtplib.SMTP(HOST)
    server.sendmail(FROM, [TO], BODY)
    server.quit()
        

def CloseSession(*args):
    cp2.close()
    sys.exit(0)


class DataLog:

    def __init__(self):
        self.data={"info":"Solar Data Logger main data dictionary"}
        self.data[time]=self.data[timel]=time.time()


    def read_vals(self):


    def read_switching_params(self):


    def switch(self, channel, switch_to):

    
    def eval_switching(self):


    def 



#main program

cp2.init()

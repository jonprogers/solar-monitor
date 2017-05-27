#! /usr/bin/env python

#analog-reading testing

import cp2
import datetime
import time

cp2.init()
n=0
Umax=0
Smax=0
while n<200:
    n=n+1
    ch0=cp2.ana_in(0)
    ch0=ch0*4683
    if Umax<ch0:
        Umax=ch0
        
    ch1=cp2.ana_in(1)
    ch1=ch1*1412
    if Smax<ch1:
        Smax=ch1
        
    tch0=str(ch0)
    rch0=tch0[:6]
    tch1=str(ch1)
    rch1=tch1[:6]
    now=datetime.datetime.now()
    outstr=time.strftime('%H:%M:%S',time.localtime()) + ' : Usage - ' + rch0 + 'W :Solar - ' + rch1 +'W :Umax ' + str(Umax)[:5] + ' Smax ' + str(Smax)[:5]
    print outstr
    time.sleep(10)
    
cp2.close()

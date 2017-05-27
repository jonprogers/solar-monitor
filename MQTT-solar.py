#! /usr/bin/env python


from Tkinter import *
import ttk
import cp2
import sys
import time
import datetime
import smtplib
import string
import paho.mqtt.client as paho

auxmargin = 800

def on_publish(client, userdata, mid):
    print("MQTT: "+str(mid))

def Email_results(Current, Maxpower, Daygen, Dayuse):
    HOST = "relay.plus.net"
    SUBJECT = "Solar update, generated " + time.strftime("%Y-%m-%d %H:%M", time.localtime())
    TO = "jon.rogers@onodo.co.uk"
    FROM = "jonprogers@jonprogers.plus.com"
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
    try:
        server = smtplib.SMTP(HOST)
        server.sendmail(FROM, [TO], BODY)
        server.quit()
    
    except:
        print "Email error occured"
        

def CloseSession(*args):
    cp2.close()
    client.loop_stop()
    sys.exit(0)

def reread():
    global vSlast, vSnow, vSmaxhr, vSmaxday, vSmaxrun, vSEhr, vSEday, vSErun
    global vUlast, vUnow, vUmaxhr, vUmaxday, vUmaxrun, vUEhr, vUEday, vUErun
    global lasttime, nowtime
    global Sinst, Uinst, Smaxhr, Umaxhr, Smaxday, Umaxday, Smaxrun, Umaxrun
    global SEhr, UEhr, SEday, UEday, SErun, UErun, fan, genmargin, auxrun, auxruntxt
    global lasthr, lastday, lastmin
    curtime.set(time.strftime("%H:%M:%S",time.localtime()))
    vSlast=vSnow
    vUlast=vUnow
    lasttime=nowtime
    nowtime=time.time()
    vSnow=cp2.ana_in(1)
    vUnow=cp2.ana_in(0)
    #vSnow=vSnow*1414
    vSnow=vSnow*1437
    #vUnow=vUnow*4683
    vUnow=vUnow*4690
    
    vSnow=vSnow - 62
    if vSnow<40:
        vSnow=0


    d=datetime.datetime.now()
    t=d.timetuple()
    rSnow=int(vSnow)

    fanon=False
    if rSnow>1000:
        if rSnow > vUnow:
            fanon=True


    if fanon:
        cp2.dig_out(15,True)
        fan.set("True")
    else:
        cp2.dig_out(15,False)
        fan.set("False")

    margin=vSnow-vUnow
    genmargin.set(str(int(margin)))
    if auxrun and margin < -50:
        cp2.dig_out(11,False)
        auxrun = False

    if not(auxrun) and margin > auxmargin:
        cp2.dig_out(11,True)
        auxrun = True
        
    if auxrun:
        auxruntxt.set("True")
    else:
        auxruntxt.set("False")

    if t[3] != lasthr:
        Email_results(str(rSnow), str(int(vSmaxday)), str(int(vSEday)), str(int(vUEday)))
        vSmaxhr=0
        vUmaxhr=0
        vSEhr=0
        vUEhr=0
        lasthr=t[3]

    if t[2] != lastday:
        vSmaxday=0
        vUmaxday=0
        vSEday=0
        vUEday=0
        lastday=t[2]

    if t[4] != lastmin:
        (rc, mid) = client.publish('status/solar/inst', str(int(vSnow)), qos=1)
        (rc, mid) = client.publish('status/power/inst', str(int(vUnow)), qos=1)
        (rc, mid) = client.publish('status/solar/day', str(vSEday), qos=1)
        (rc, mid) = client.publish('status/power/day', str(vUEday), qos=1)
        lastmin=t[4]
        
    if rSnow > vSmaxhr:
        vSmaxhr = vSnow
        Smaxhr.set(str(rSnow))
        
    rUnow=int(vUnow)
    if rUnow > vUmaxhr:
        vUmaxhr = vUnow
        Umaxhr.set(str(rUnow))
        
    if rSnow > vSmaxday:
        vSmaxday = vSnow
        Smaxday.set(str(rSnow))
        
    if rUnow > vUmaxday:
        vUmaxday = vUnow
        Umaxday.set(str(rUnow))

    if rSnow > vSmaxrun:
        vSmaxrun = vSnow
        Smaxrun.set(str(rSnow))
        
    if rUnow > vUmaxrun:
        vUmaxrun = vUnow
        Umaxrun.set(str(rUnow))

    if vSnow<(2 * vSlast):
        if vSnow>(0.75 * vSlast):            
            vSEd=((vSnow+vSlast)/2)*(nowtime-lasttime)/3600
            vSEhr=vSEhr+vSEd
            vSEday=vSEday+vSEd
            vSErun=vSErun+vSEd

            
    vUEd=((vUnow+vUlast)/2)*(nowtime-lasttime)/3600
    vUEhr=vUEhr+vUEd
    vUEday=vUEday+vUEd
    vUErun=vUErun+vUEd

    SEhr.set(str(int(vSEhr)))
    SEday.set(str(int(vSEday)))
    SErun.set(str(int(vSErun)))
    UEhr.set(str(int(vUEhr)))
    UEday.set(str(int(vUEday)))
    UErun.set(str(int(vUErun)))

    Sinst.set(str(rSnow))
    Uinst.set(str(rUnow))
    
    root.after(1000, reread)
    
root = Tk()
root.title("Realtime Solar Monitor with MQTT")

frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(N, W, E, S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

curtime = StringVar()
Sinst = StringVar()
Smaxhr = StringVar()
Smaxday = StringVar()
Smaxrun = StringVar()
SEhr = StringVar()
SEday = StringVar()
SErun = StringVar()
Uinst = StringVar()
Umaxhr = StringVar()
Umaxday = StringVar()
Umaxrun = StringVar()
UEhr = StringVar()
UEday = StringVar()
UErun = StringVar()
fan = StringVar()
genmargin = StringVar()
auxruntxt = StringVar()

curtime.set(time.strftime("%H:%M:%S",time.localtime()))
vSnow=0
vSlast=0
vUnow=0
vUlast=0
vSmaxhr=0
vSmaxday=0
vSmaxrun=0
vUmaxhr=0
vUmaxday=0
vUmaxrun=0
vSEhr=0
vSEday=0
vSErun=0
vUEhr=0
vUEday=0
vUErun=0
lasthr=0
lastday=0
lastmin=0
auxrun=False

ttk.Button(frame, text="Stop", command=CloseSession).grid(column=5, row=1, sticky=W)
ttk.Label(frame, text="Sample Time").grid(column=1, row=2, sticky=W)
ttk.Label(frame, text="SOLAR").grid(column=2, row=3, sticky=E)
ttk.Label(frame, text="USAGE").grid(column=4, row=3, sticky=E)
ttk.Label(frame, text="Instantaneous").grid(column=1, row=4, sticky=W)
ttk.Label(frame, text="Max this hour").grid(column=1, row=5, sticky=W)
ttk.Label(frame, text="Max this day").grid(column=1, row=6, sticky=W)
ttk.Label(frame, text="Max this run").grid(column=1, row=7, sticky=W)
ttk.Label(frame, text="This hour").grid(column=1, row=8, sticky=W)
ttk.Label(frame, text="This day").grid(column=1, row=9, sticky=W)
ttk.Label(frame, text="This run").grid(column=1, row=10, sticky=W)
ttk.Label(frame, text="Fan run").grid(column=1, row=11, sticky=W)
ttk.Label(frame, text="Gen margin").grid(column=1, row=12, sticky=W)
ttk.Label(frame, text="Aux run").grid(column=1, row=13, sticky=W)
ttk.Label(frame, text="W").grid(column=3, row=4, sticky=W)
ttk.Label(frame, text="W").grid(column=3, row=5, sticky=W)
ttk.Label(frame, text="W").grid(column=3, row=6, sticky=W)
ttk.Label(frame, text="W").grid(column=3, row=7, sticky=W)
ttk.Label(frame, text="Wh").grid(column=3, row=8, sticky=W)
ttk.Label(frame, text="Wh").grid(column=3, row=9, sticky=W)
ttk.Label(frame, text="Wh").grid(column=3, row=10, sticky=W)
ttk.Label(frame, text="W").grid(column=5, row=4, sticky=W)
ttk.Label(frame, text="W").grid(column=5, row=5, sticky=W)
ttk.Label(frame, text="W").grid(column=5, row=6, sticky=W)
ttk.Label(frame, text="W").grid(column=5, row=7, sticky=W)
ttk.Label(frame, text="Wh").grid(column=5, row=8, sticky=W)
ttk.Label(frame, text="Wh").grid(column=5, row=9, sticky=W)
ttk.Label(frame, text="Wh").grid(column=5, row=10, sticky=W)
ttk.Label(frame, text="W").grid(column=3, row=12, sticky=W)

ttk.Label(frame, textvariable=curtime).grid(column=2, row=2, sticky=E)
ttk.Label(frame, textvariable=Sinst).grid(column=2, row=4, sticky=E)
ttk.Label(frame, textvariable=Smaxhr).grid(column=2, row=5, sticky=E)
ttk.Label(frame, textvariable=Smaxday).grid(column=2, row=6, sticky=E)
ttk.Label(frame, textvariable=Smaxrun).grid(column=2, row=7, sticky=E)
ttk.Label(frame, textvariable=SEhr).grid(column=2, row=8, sticky=E)
ttk.Label(frame, textvariable=SEday).grid(column=2, row=9, sticky=E)
ttk.Label(frame, textvariable=SErun).grid(column=2, row=10, sticky=E)
ttk.Label(frame, textvariable=Uinst).grid(column=4, row=4, sticky=E)
ttk.Label(frame, textvariable=Umaxhr).grid(column=4, row=5, sticky=E)
ttk.Label(frame, textvariable=Umaxday).grid(column=4, row=6, sticky=E)
ttk.Label(frame, textvariable=Umaxrun).grid(column=4, row=7, sticky=E)
ttk.Label(frame, textvariable=UEhr).grid(column=4, row=8, sticky=E)
ttk.Label(frame, textvariable=UEday).grid(column=4, row=9, sticky=E)
ttk.Label(frame, textvariable=UErun).grid(column=4, row=10, sticky=E)
ttk.Label(frame, textvariable=fan).grid(column=2, row=11, sticky=E)
ttk.Label(frame, textvariable=genmargin).grid(column=2, row=12, sticky=E)
ttk.Label(frame, textvariable=auxruntxt).grid(column=2, row=13, sticky=E)

root.bind('<Return>', CloseSession)
for child in frame.winfo_children(): child.grid_configure(padx=2, pady=5)

##Setup MQTT connection
client = paho.Client()
client.on_publish = on_publish
client.connect('aclosehas.onodo.co.uk', 1883)
client.loop_start()

cp2.init()
lasttime = nowtime = time.time()


reread()
root.mainloop()

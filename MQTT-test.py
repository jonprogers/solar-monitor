import paho.mqtt.client as paho
import time
 
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
client.connect('aclosehas.onodo.co.uk', 1883)
client.loop_start()
temperature = 1
 
while True:
    
    (rc, mid) = client.publish('encyclopedia/temperature', str(temperature), qos=1)
    time.sleep(30)
    temperature = temperature +1

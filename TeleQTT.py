#!/usr/bin/env python
import mosquitto
import os
import teleinfo
from serial import SerialException

broker = "localhost"
port = 1883

def on_connect(mosq, obj, rc):
    if rc == 0:
    #rc 0 successful connect
        print "Connected"
    else:
        raise Exception
 
def on_publish(mosq, obj, mid):
    print("Message "+str(mid)+" published.")
 
def on_disconnect(mosq, obj, rc):
    if rc != 0:
        print("Unexpected disconnection.")

 
#called on exit
#close serial, disconnect MQTT
 
def cleanup():
    print "Ending and cleaning up"
    mqttc.disconnect()

try:
    print "Connecting... "
    #connect to serial port
    ti = teleinfo.Teleinfo("/dev/teleinfo")
except:
    print "Failed to connect serial"
    #unable to continue with no serial input
    raise SystemExit

try:
    mypid = os.getpid()
    client_uniq = "RB_EDF"
    mqttc = mosquitto.Mosquitto(client_uniq)

#attach MQTT callbacks
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_disconnect = on_disconnect

#connect to broker
    mqttc.connect(broker, port, 60, True)
 
    while mqttc.loop() == 0:
        line = ti.read()
        if line is not None:
            for serEtiquette, serValue in line.items():
                mqttc.publish("EDF/"+serEtiquette, serValue)
except (SerialException):
    print "Serial Exception"
#    pass
except (IndexError):
    print "No data received within serial timeout period"
    cleanup()
# handle app closure
except (KeyboardInterrupt):
    print "Interrupt received"
    cleanup()
except (RuntimeError):
    print "uh-oh! time to die"
    cleanup()

#!/usr/bin/env python

# Handle the new paho naming for Mosquitto lib
try:
    import mosquitto
    mqtt_version = "mosquitto"
except:
    import paho.mqtt.client as paho
    mqtt_version = "paho"

import os
import teleinfo
from serial import SerialException
import optparse

parser = optparse.OptionParser(description="Serial to MQTT teleinfo interface")
parser.add_option("-b", "--mqtt-broker-host", help=u"Host name/address for MQTT broker, default = localhost", dest="mqtt_host", default="localhost")
parser.add_option("-p", "--mqtt-broker-port", help=u"Port for MQTT broker, default = 1883",  dest="mqtt_port", default=1883)
parser.add_option("-t", "--mqtt-base-topic", help=u"Base toic for published messages, default = EDF/",  dest="mqtt_base_topic", default="EDF/")
(options, args) = parser.parse_args()

def on_connect(mosq, obj, flags, rc):
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
    try:
        mqttc = mosquitto.Mosquitto(client_uniq)
    except:
        mqttc = paho.Client(client_uniq)

#attach MQTT callbacks
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_disconnect = on_disconnect

#connect to broker
    if mqtt_version == "mosquitto":
        mqttc.connect(options.mqtt_host, options.mqtt_port, 60, True)
    elif mqtt_version == "paho":
        mqttc.connect(options.mqtt_host, options.mqtt_port, 60)
    else:
        raise RuntimeError("Unknown MQTT lib")
 
    while mqttc.loop() == 0:
        line = ti.read()
        if line is not None:
            for serEtiquette, serValue in line.items():
                mqttc.publish(options.mqtt_base_topic+serEtiquette, serValue)
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

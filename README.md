TeleQTT
=======

This easy script publish to MQTT the value from a serial teleinfo modem located at /dev/teleinfo.
The labels are pushed to the EDF/<label> at local MQTT server.

Imports
=======
The mosquitto library used for the MQTT client may not be available on your default installation.  It can be installed with pip like this:
`pip install mosquitto`

If you are running on a Raspberry Pi and need to install pip, you can do it with this:
`sudo apt-get install python-setuptools && sudo easy_install pip`

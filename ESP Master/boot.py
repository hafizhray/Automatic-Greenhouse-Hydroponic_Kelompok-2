import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
import dht

try:
  import usocket as socket
except:
  import socket

esp.osdebug(None)
import gc
gc.collect()


ssid = 'RouterRoom6'
password = 'indra123'
mqtt_server = 'broker.mqttdashboard.com'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'hydro/monitor'
topic_pub = b'hydro/control'

last_message = 0
message_interval = 0.5

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


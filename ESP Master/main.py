import machine
from machine import Pin, SoftI2C
from time import sleep
from endecode import EnDecode
from base64 import decode
from lcd_api import LcdApi
from i2c_lcd import I2cLcd


# Initializing LCD
lcd_count = 0

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32

lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

global data_rcv
data_rcv = [0,0,0,0,0,0,0,0]

def sub_cb(topic, msg):
  global data_rcv
  data_rcv = EnDecode().dec_data(msg)
  print(data_rcv)

  
def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
  except OSError as e:
    restart_and_reconnect()

  print("Suhu:", data_rcv[1], "Kelembaban:", data_rcv[2], "Intensitas (Lux):", data_rcv[4], "Ketinggian air:", data_rcv[6])
  if lcd_count == 0:
    lcd_row1 ="Temp: "+str(data_rcv[1])+" C"
    lcd_row2 ="Hum:  "+str(round(data_rcv[2], 1))+" %"
    lcd_count = 1
  else:
    lcd_row1 ="Lux: "+str(int(data_rcv[4]))
    lcd_row2 ="Air: "+str(round(data_rcv[6],1))+" cm"
    lcd_count = 0
  lcd.putstr(lcd_row1+" "*(16-len(lcd_row1))+lcd_row2+" "*(16-len(lcd_row2)))
  sleep(1)

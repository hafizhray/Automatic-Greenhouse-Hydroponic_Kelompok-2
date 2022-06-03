from machine import Pin, Timer
import machine
import time
from time import sleep
import umqttsimple
from umqttsimple import MQTTClient
from ldr import LDR
from led import LED
from mov_avg import Mov_Avg
import dht
from water_sens import Water_Sens
from endecode import EnDecode


# Variable to be sent
auto = 1
branch = 1
temp = 0
hum = 0
servo = 0
lux = 0
led = 0
water_lvl = 0
pump = 0

# Autoatic indicator
auto_pin = Pin(19, Pin.OUT)
auto_pin.off()

# Servo
p2 = machine.Pin(27)
pwm2 = machine.PWM(p2)
# set the PWM frequency as 50Hz
pwm2.freq(50)
# mengubah duty jadi angular
def dty (ang):
  d = 18+(97/180)*ang
  # d = ang/180
  return int(d)
# memutar servo 0 derajat lalu 180 derajat
def semprot():
  pwm2.duty(dty(0))
  time.sleep(0.5)
  pwm2.duty(dty(180))
  time.sleep(0.5)


# initialize a pump
pump_pin = Pin(25, Pin.OUT)
pump_pin.on()

# initialize a LDR
ldr_pin = LDR(32)
ldr_mov = Mov_Avg(5)

# initialize Water Sensor
water_pin = Water_Sens(34, 21)
water_mov = Mov_Avg(5)

# Initialize LED
led_pin = LED(5, 10)

led_pin.start()

# Initialize DHT
dht_sens = dht.DHT22(Pin(15))

temp = hum = 0

def read_dht():
  global temp, hum
  try:
    dht_sens.measure()
    temp = dht_sens.temperature()
    hum = dht_sens.humidity()
    if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
      msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))
      hum = round(hum, 2)
      return(msg)
    else:
      return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')


def sub_cb(topic, msg):
  print(msg)
  global auto, pump, servo, led

  # Respon terhadap pesan yang diterima
  if msg[:1] == b'0':
    auto = 0
  elif msg[:1] == b'1':
    auto = 1
  if msg[1:] == b'0':
    pump = 0
  if msg[1:] == b'1':
    pump = 1
  if msg[1:] == b'2':
    servo = 0
  if msg[1:] == b'3':
    servo = 1
  if msg[1:] == b'4':
    led = 0
  if msg[1:] == b'5':
    led = 1

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
  # DHT and Servo
  try:
    read_dht()
  except:
    temp = temp
    hum = hum

  
  # LDR and LED
  lux = ldr_mov.filter(ldr_pin.lux())

  # Water LVL
  water_lvl = water_mov.filter(water_pin.read()*4/100)

  # Debug
  print("Illumination %:", lux, "temp :", temp, "hum :", hum, "water lvl :", water_lvl, "water raw", water_pin.raw())


  # Control
  if auto == 0:
    auto_pin.on()
    # Pump
    if pump == 0:
      pump_pin.on()
    elif pump == 1:
      pump_pin.off()
      
    # LED
    if led == 0:
      led_pin.update_lux(999999)
    elif led == 1:
      led_pin.update_lux(0)

    # Servo
    if servo == 1:
      semprot()
  
  else:
    auto_pin.off()
    # Servo
    if hum < 80:
      semprot()

    # Led
    led_pin.update_lux(lux)

    # Pump
    if water_lvl < 0.5 and pump_pin.value() == 1:
      pump_pin.off()
    if water_lvl > 3.5 and pump_pin.value() == 0:
      pump_pin.on()


  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = EnDecode().enc_data([branch, 0, 2, temp, 1, 3, hum, 1, 3, servo, 0, 1, lux, 0, 6, led, 0, 1, water_lvl, 1, 3, pump, 0, 1])
      client.publish(topic_pub, msg)
      client.publish(b'hydro/temp', str(temp))
      client.publish(b'hydro/hum', str(hum))
      client.publish(b'hydro/lux', str(lux))
      client.publish(b'hydro/water', str(round(water_lvl,1)))
      last_message = time.time()
  except OSError as e:
    restart_and_reconnect()

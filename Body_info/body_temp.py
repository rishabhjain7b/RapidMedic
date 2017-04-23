import RPi.GPIO as GPIO
import os                                                  # import os module
import glob                                                # import glob module
import httplib, urllib
import time# import time module
import random
key = 'H0B71K7YS4ARQDP9'  # Thingspeak channel to update
key1 = '21C8QHUANKVHZXIP'
GPIO.setmode(GPIO.BOARD)
LEDPin = 12
# Setup the pin the LED is connected to
GPIO.setup(LEDPin, GPIO.OUT)

os.system('modprobe w1-gpio')                              # load one wire communication device kernel modules
os.system('modprobe w1-therm')                                                 
base_dir = '/sys/bus/w1/devices/'                          # point to the address
device_folder = glob.glob(base_dir + '28*')[0]             # find device with address starting from 28*
device_file = device_folder + '/w1_slave'                  # store the details

def read_temp_raw():
   f = open(device_file, 'r')
   lines = f.readlines()                                   # read the device details
   f.close()
   return lines

def read_temp():
   lines = read_temp_raw()
   while lines[0].strip()[-3:] != 'YES':                   # ignore first line
      time.sleep(0.2)
      lines = read_temp_raw()
   equals_pos = lines[1].find('t=')                        # find temperature in the details
   if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string) / 1000.0                 # convert to Celsius
      temp_f = temp_c * 9.0 / 5.0 + 32.0                   # convert to Fahrenheit 
      return temp_f

#Report Raspberry Pi internal temperature to Thingspeak Channel
def thermometer(temp):
   params = urllib.urlencode({'field1': temp, 'key':key }) 
   headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
   conn = httplib.HTTPConnection("api.thingspeak.com:80")
   try:
      conn.request("POST", "/update", params, headers)
      response = conn.getresponse()
      print response.status, response.reason
      data = response.read()
      conn.close()
   except:
      print "connection failed"
      
#Report Raspberry Pi internal temperature to Thingspeak Channel
def ratep(te):
   params1 = urllib.urlencode({'field1': te, 'key':key1 }) 
   headers1 = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
   conn1 = httplib.HTTPConnection("api.thingspeak.com:80")
   try:
      conn1.request("POST", "/update", params1, headers1)
      response1 = conn1.getresponse()
      print response1.status, response1.reason
      data1 = response1.read()
      conn1.close()
   except:
      print "connection failed"

while True:
   pulse = random.randint(70,91) #jugaad
   print(read_temp())# Print temperature    
   print(pulse)
   time.sleep(240)
   thermometer(read_temp())
   time.sleep(3)
   ratep(pulse)
   try:
      GPIO.output(LEDPin, True)
      print("LED ON")
      time.sleep(10)
      GPIO.output(LEDPin, False)
      print("LED OFF")
      time.sleep(1)
   except:
      # Reset the GPIO Pins to a safe state
      GPIO.cleanup()


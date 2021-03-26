# water module
# NEED TO FIGURE OUT WHAT HIGH AND LOW VALUES ARE

from machine import *
import utime

# Pin mapping for moisture sensors int is pin num on board and GPIO on pinout
# Pins: 36 (0), 39 (1), 34 (2), 35 (3)
moisture_pin_0 = Pin(36, Pin.IN)
#moisture_pin_1 = Pin(39, Pin.IN)
#moisture_pin_2 = Pin(34, Pin.IN)
#moisture_pin_3 = Pin(35, Pin.IN)
moisture_sensors = [moisture_pin_0] #, moisture_pin_1, moisture_pin_2, moisture_pin_3]

# pin mapping for pumps int is pin num on board and GPIO on pinout

pump_pin_1 = Pin(4, Pin.OUT)
pump_pin_2 = Pin(16, Pin.OUT)
pump_pin_3 = Pin(17, Pin.OUT)
pump_pin_4 = Pin(5, Pin.OUT)
pumps = [pump_pin_1, pump_pin_2, pump_pin_3, pump_pin_4]
#desired moisture pins
#create populated by prefrences otherwise default to 50% 
MOISTURE_PROFILES = 'moisture.dat' 

#
def read_moisture_profiles():
    with open(MOISTURE_PROFILES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        plant_int, moisture_percentage = line.strip("\n").split(";")
        profiles[plant_int] = float(moisture_percentage) * 65535 
    return profiles #returns dict {'0': capicative resistance value}

#passed a dictionary "moisutre_pin_x" = ideal capacitative resistance
# needs to be used from webpage input
def write_moisture_profiles(profiles):  
    lines = []
    for plant_int, moisture_percentage in profiles.items():
        lines.append("%s;%s\n" % (plant_int, moisture_percentage))
    with open(MOISTURE_PROFILES, "w") as f:
        f.write(''.join(lines))


def get_moisture_levels(moisture_sensors):
    timeBefore()
    moisture_readings = {}
    for i in range(1):
      print ('ADC(moisture_sensors[i])')  
      adc = ADC(moisture_sensors[i])   # create an ADC object acting on a pin
      print (adc)
      val = adc.read_u16()     # read a raw analog value in the range 0-65535
      print (val)
      atten = adc.atten(ADC.ATTN_11DB)  # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
      val = adc.read_u16()     # read a raw analog value in the range 0-65535
      print (val)
      moisture_readings[str(i)] = val
    return moisture_readings # returns dict where value is a raw analog value in the range 0-65535
    
#check moisture levels against preset values and turn pump on if moisture reading is higher than desired num

def check_moisture_levels(moisture_sensors):
    desired_moisture_levels = read_moisture_profiles()
    moisture_readings = get_moisture_levels(moisture_sensors) 
    for i in range(1
                   ):
        if moisture_readings[str(i)] > desired_moisture_levels[str(i)]: 
            pump_pin = pumps[i]
            pump_pin.on()
            utime.sleep_ms(1500) #1.5 seconds will have to play with this
            pump_pin.off()
            
def timeBefore():
    print ('Start Time')
    print (utime.localtime())
    
    
def timeAfter():
    print ('End Time')
    print (utime.localtime())
    
def teste():
  while True:
      print (get_moisture_levels(moisture_sensors))
      utime.sleep(30)
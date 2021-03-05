# water module


import machine
import utime

# Pin mapping for moisture sensors int is pin num on board and GPIO on pinout

moisture_pin_1 = Pin(12, Pin.IN)
moisture_pin_2 = Pin(14, Pin.IN)
moisture_pin_3 = Pin(27, Pin.IN)
moisture_pin_4 = Pin(26, Pin.IN)
moisture_sensors = [moisture_pin_1, moisture_pin_2, moisture_pin_3, moisture_pin_4]

# pin mapping for pumps int is pin num on board and GPIO on pinout

pump_pin_1 = Pin(4, Pin.OUT)
pump_pin_2 = Pin(16, Pin.OUT)
pump_pin_3 = Pin(17, Pin.OUT)
pump_pin_4 = Pin(5, Pin.OUT)
pumps = [pump_pin_1, pump_pin_2, pump_pin_3, pump_pin_4]
pump_mapping = {moisture_pin_1 = pump_pin_1, moisture_pin_2 = pump_pin_2, moisture_pin_3 = pump_pin_3, moisture_pin_4 = pump_pin_4}
#desired moisture pins
#create populated by prefrences otherwise default to 50%
MOISTURE_PROFILES = 'moisture.dat' #moisture profiles 

def read_moisture_profiles():
    with open(MOISTURE_PROFILES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        moisture_sensor_pin, moisture_level = line.strip("\n").split(";")
        profiles[moisture_sensor_pin] = moisture_level
    return profiles

#passed a dictionary moisutre_pin_x = ideal capacitative resistance
# needs to be used from webpage input
def write_moisture_profiles(profiles):  
    lines = []
    for moisture_sensor_pin, moisture_level in profiles.items():
        lines.append("%s;%s\n" % (moisture_sensor_pin, moisture_level))
    with open(MOISTURE_PROFILES, "w") as f:
        f.write(''.join(lines))




def get_moisture_levels(moisture_sensors):
    moisture_readings = {}
    for i in moisture_sensors:
      adc = machine.ADC(i)   # create an ADC object acting on a pin
      val = adc.read_u16()     # read a raw analog value in the range 0-65535
      moisture_readings[i] = val
    return moisture_readings # returns dictionary where key is moisture_pin_x and value is a raw analog value in the range 0-65535
    
    
#check moisture levels against preset values and turn pump on if moisture reading is higher than desired num

def check_moisture_levels(moisture_sensors):
    desired_moisture_levels = read_moisture_profiles()
    moisture_readings = get_moisture_levels(moisture_sensors)
    for i in moisture_sensors:
        if moisture_readings[i] > desired_mositure_levels[i]: 
            pump_pin = pump_mapping[i]
            pump_pin.on()
            utime.sleep_ms(1500) #1.5 seconds will have to play with this
            pump_pin.off()
            
    
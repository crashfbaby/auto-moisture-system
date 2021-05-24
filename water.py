from machine import *

moisture_pin_0 = Pin(39, Pin.IN)
moisture_pin_1 = Pin(35, Pin.IN)
moisture_pin_2 = Pin(33, Pin.IN)
moisture_pin_3 = Pin(34, Pin.IN)
#moisture_pins = [moisture_pin_0 , moisture_pin_1, moisture_pin_2, moisture_pin_3]
moisture_pins = {'0': moisture_pin_0, '1': moisture_pin_1, '2': moisture_pin_2, '3': moisture_pin_3}

pump_pin_0 = Pin(32, Pin.OUT)
pump_pin_1 = Pin(4, Pin.OUT)
pump_pin_2 = Pin(0, Pin.OUT)
pump_pin_3 = Pin(2, Pin.OUT)
#pump_pins = [pump_pin_0, pump_pin_1, pump_pin_2, pump_pin_3]
pump_pins = {'0': pump_pin_0, '1': pump_pin_1, '2': pump_pin_2, '3': pump_pin_3}
PLANT_PROFLIES = 'plants.dat'


#save plant info to 'plant.dat'     
def write_plant_profiles():  
    lines = []
    for idx, plant in PLANTS.items(): # PLANTS needs to be global list of plant objects so it writes entire plant profile for each plant. Use create_plant_objects() to make list
        lines.append("%s;%s,%s,%s,%s,%s,%s\n" % (idx, plant.moisture_pin, plant.pump_pin, plant.desired_moisture_percent, plant.moisture_min, plant.moisture_max, plant.name))
    with open(PLANT_PROFLIES, "w") as f:
        f.write(''.join(lines))
    

#returns dictionary {'0': {plant.moisture_pin:X plant.pump_pin:X, plant.desired_moisture_percent:X, plant.moisture_min:X, plant.moisture_max:X, plant.name:X]
        #might need to throw an exception handler to retrun none to make create_create_plant_objects() work 
def read_plant_profiles():
    with open(PLANT_PROFLIES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        plant_info_dict = {}
        plant_int, plant_info = line.strip("\n").split(";")
        plant_info_list = plant_info.split(',')
        plant_info_dict['moisture_pin'] = plant_info_list[0]
        plant_info_dict['pump_pin'] = plant_info_list[1]
        plant_info_dict['desired_moisture_percent'] = float(plant_info_list[2])
        plant_info_dict['moisture_min'] = float(plant_info_list[3])
        plant_info_dict['moisture_max'] = float(plant_info_list[4])
        plant_info_dict['name'] = plant_info_list[5]
        profiles[plant_int] = plant_info_dict        
    return profiles 


class Plant :
    #plant class constructor
    def __init__(self, idx, moisture_pin, pump_pin) :
        self.id = idx
        self.moisture_pin = moisture_pin
        self.pump_pin = pump_pin
        self.desired_moisture_percent = 0.5    
        self.moisture_min = 0       #theoretical min calibration function will fix making it an instance variable allows for variation between sensors WET
        self.moisture_max = 65535   #theoretical Max calibration function will fix making it an instance variable allows for variation between sensors DRY
        self.name = 'Mysterious Plant'
        
    #call to update sensor reading
    def check_moisture_sensor(self):
        adc = ADC(self.moisture_pin)   # create an ADC object acting on a pin
        atten = adc.atten(ADC.ATTN_11DB)  # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        val = adc.read_u16()     # read a raw analog value in the range 0-65535
        return val
    
    #convert float that represents moisture level as a percent to an analog value comparable to the val returned by check_moisture_sensor
    def prefered_moisture_analog(self):
        sensor_range = self.moisture_max - self.moisture_min
        return (sensor_range * self.desired_moisture_percent) + self.moisture_min

    def update_name(self, new_name):
        self.name = new_name
        write_plant_profiles()
        
    def update_desired_moisture_percent(self, new_percent):
        self.desired_moisture_percent = new_percent
        write_plant_profiles()

    #should be called with sensor in open air higher resistance = less water  DRY
    def update_max(self):
        new_max = self.check_moisture_sensor()
        if new_max == 0:
            new_max += 1
        self.moisture_max = new_max
        write_plant_profiles()
        
    #should be called with sensor in water lower resistance = more water  WET
    def update_min(self):
        new_min = self.check_moisture_sensor()
        self.moisture_min = new_min
        write_plant_profiles()
        
    #compares moisture reading to desired and turns pump on if necessary then sleeps and turns off 
    def compare_moisture_levels(self):
        if self.check_moisture_sensor() > self.preferd_moisture_analog(): 
            self.pump_pin.on()
            utime.sleep_ms(1500) #1.5 seconds will have to play with this
            self.pump_pin.off()
            
    
#creates a disctionary of plant objects from plants.dat or from supplied pin list if that dosent exist
def create_plant_objects():
    plant_profiles = read_plant_profiles()
    plants = {}
    if plant_profiles == {}:  #create new plants if no plant.dat file exists
        for i in range(len(pump_pins)):
            new_plant = Plant(str(i), moisture_pins[str(i)], pump_pins[str(i)])
            plants[str(i)] = new_plant
    else:  #creat plant objects based on plant.dat file
        for i in range(len(plant_profiles)): 
            plant_info = plant_profiles[str(i)]
            existing_plant = Plant(str(i), moisture_pins[str(i)], pump_pins[str(i)])
            existing_plant.desired_moisture_percent = float(plant_info['desired_moisture_percent'])    
            existing_plant.moisture_min = float(plant_info['moisture_min'])      
            existing_plant.moisture_max = float(plant_info['moisture_max'])   
            existing_plant.name = plant_info['name']
            plants[str(i)] = existing_plant
    return plants


PLANTS = create_plant_objects()
write_plant_profiles()

def get_plant_objects():
    return PLANTS

# plant_list = create_plant_objects() runs thru plants and checks water levels should run every 30 min?
def water_loop(plants_list):
    for plant in plant_list:
        plant.comapre_moisture_levels()
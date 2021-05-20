#web_portal

import water
from MicroWebSrv2 import *

@WebRoute(GET, '/plants', name='plants_get')
def RequestTestPost(microWebSrv2, request) :
    wetness = water.read_moisture_profiles()
    plant_0 = (wetness['0'] / 65535)*100
    plant_1 = (wetness['1'] / 65535)*100
    plant_2 = (wetness['2'] / 65535)*100
    plant_3 = (wetness['3'] / 65535)*100
    content = """\
  <!DOCTYPE html>
    <html>
        <head>
            <title>Wetness</title>
        </head>
        <body>
            <h2>How Wet do you want it?</h2>
            
            <form action="/home" method="post">
                Plant 1: Wet <input type="range" min="1" max="100" value="{plant_0}" class="slider" id="moisture_pin_1"> Dry <br /> 
                Plant 2: Wet <input type="range" min="1" max="100" value="{plant_1}" class="slider" id="moisture_pin_2"> Dry <br />
                Plant 3: Wet <input type="range" min="1" max="100" value="{plant_2}" class="slider" id="moisture_pin_3"> Dry <br />
                Plant 4: Wet <input type="range" min="1" max="100" value="{plant_3}" class="slider" id="moisture_pin_4"> Dry <br />
                <input type="submit" value="Update Wetness">
            </form>
        </body>
    </html>
    """.format(plant_0=plant_0, plant_1=plant_1, plant_2=plant_2, plant_3=plant_3)
    request.Response.ReturnOk(content)

# ------------------------------------------------------------------------

@WebRoute(POST, '/plants', name='plants_post')
def RequestTestPost(microWebSrv2, request) :
    data = request.GetPostedURLEncodedForm()
    try :
        profiles = {}
        profiles['0'] = data['moisture_pin_1']
        profiles['1'] = data['moisture_pin_2']
        profiles['2'] = data['moisture_pin_3']
        profiles['3'] = data['moisture_pin_4']
        print(profiles)
        water.write_water_profiles(profiles)
    except :
        request.Response.ReturnBadRequest()
        return
    wetness = water.read_moisture_profiles()
    plant_0 = (wetness['0'] / 65535)*100
    plant_1 = (wetness['1'] / 65535)*100
    plant_2 = (wetness['2'] / 65535)*100
    plant_3 = (wetness['3'] / 65535)*100
    
    content = """\
    <!DOCTYPE html>
      <html>
        <head>
            <title>Wetness</title>
        </head>
        <body>
            <h2>How Wet do you want it?</h2>
            
            <form action="/home" method="post">
                Plant 1: Wet <input type="range" min="1" max="100" value="{plant_0}" class="slider" id="moisture_pin_1"> Dry <br /> 
                Plant 2: Wet <input type="range" min="1" max="100" value="{plant_1}" class="slider" id="moisture_pin_2"> Dry <br />
                Plant 3: Wet <input type="range" min="1" max="100" value="{plant_2}" class="slider" id="moisture_pin_3"> Dry <br />
                Plant 4: Wet <input type="range" min="1" max="100" value="{plant_3}" class="slider" id="moisture_pin_4"> Dry <br />
                <input type="submit" value="Update Wetness">
            </form>
        </body>
      </html>
    """.format(plant_0=plant_0, plant_1=plant_1, plant_2=plant_2, plant_3=plant_3)
    request.Response.ReturnOk(content)
  

pyhtmlMod = MicroWebSrv2.LoadModule('PyhtmlTemplate')
pyhtmlMod.ShowDebug = True
pyhtmlMod.SetGlobalVar('TestVar', 12345)

# Loads the WebSockets module globally and configure it,
wsMod = MicroWebSrv2.LoadModule('WebSockets')
#wsMod.OnWebSocketAccepted = OnWebSocketAccepted

# Instanciates the MicroWebSrv2 class,
mws2 = MicroWebSrv2()


# SSL is not correctly supported on MicroPython.
# But you can uncomment the following for standard Python.
# mws2.EnableSSL( certFile = 'SSL-Cert/openhc2.crt',
#                 keyFile  = 'SSL-Cert/openhc2.key' )

# For embedded MicroPython, use a very light configuration,
mws2.SetEmbeddedConfig()
mws2.BufferSlotsCount = 4 #default is 16 too much ram

# All pages not found will be redirected to the home '/',
mws2.NotFoundURL = '/plants'

# Starts the server as easily as possible in managed mode,
mws2.StartManaged()

# Main program loop until keyboard interrupt,
try :
    while mws2.IsRunning :
        sleep(1)
except KeyboardInterrupt :
    pass

# End,
print()
mws2.Stop()
print('Bye')
print()


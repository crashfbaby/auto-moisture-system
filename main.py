import water
import wifimgr
from MicroWebSrv2  import *
from time          import sleep
from _thread       import allocate_lock



# Wifi manager loop
wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D



# ============================================================================
# ============================================================================
# ============================================================================

@WebRoute(GET, '/', name='home')
def RequestHomePage(microWebSrv2, request) :
    plants = water.get_plant_objects()
    current_moisture_percent = {}
    for idx, plant in plants.items():
        reading = plant.check_moisture_sensor()
        current_moisture_percent[idx] = str(((reading - plant.moisture_min) / (plant.moisture_max - plant.moisture_min)) * 100)

    content = """\
     <!DOCTYPE html>
    <html>
        <head>
            <title>Plants</title>
        </head>
        <body>
            <h2>Plants</h2>
            
            <p>
              <ul>
                  <li>
                      <h3> %s </h3>
                          <li> Pump and Sensor ID: %s </li>
                          <li> Current Moisture Reading: %s </li>
                  </li>
                  <li>
                      <h3> %s </h3>
                          <li> Pump and Sensor ID: %s </li>
                          <li> Current Moisture Reading: %s </li>
                  </li>
                  <li>
                      <h3> %s </h3>
                          <li> Pump and Sensor ID: %s </li>
                          <li> Current Moisture Reading: %s </li>
                  </li>
                  <li>
                      <h3> %s </h3>
                          <li> Pump and Sensor ID: %s </li>
                          <li> Current Moisture Reading: %s </li>
                  </li>  
                          
              </ul>
            </p>
            <form action="/edit">
                <input type="submit" value="Edit" />
            </form>
        </body>
    </html>
    """ % (plants['0'].name, '0', current_moisture_percent['0'],
           plants['1'].name, '1', current_moisture_percent['1'],
           plants['2'].name, '2', current_moisture_percent['2'],
           plants['3'].name, '3', current_moisture_percent['3'])
    
    
    request.Response.ReturnOk(content)


@WebRoute(GET, '/edit', name='edit1/2')
def RequestPlantPage(microWebSrv2, request) :
    plants = water.get_plant_objects()
    content =  """\
     <!DOCTYPE html>
    <html>
        <head>
            <title>Edit Plants</title>
        </head>
        <body>
            <h2>Edit Plants</h2>
               <form action="/edit" method="post">
                   <input type="submit" value="Update Plants">
                   <h3> Plant 0 </h3>
                       <label for="plant_0_name">Plant Name</label><br>
                       <input type="text" id="plant_0_name" name="plant_0_name" value=%s><br>
                       <label for="moisture_percent_0">Plant Desired Moisture</label><br>
                       Wet <input type="range" min="1" max="100" value=%s class="slider" name="moisture_percent_0" id="moisture_percent_0"> Dry <br />
                       <br>
                   <h3> Plant 1 </h3>
                       <label for="plant_1_name">Plant Name</label><br>
                       <input type="text" id="plant_1_name" name="plant_1_name" value=%s><br>
                       <label for="moisture_percent_1">Plant Desired Moisture</label><br>
                       Wet <input type="range" min="1" max="100" value=%s class="slider" name="moisture_percent_1" id="moisture_percent_1"> Dry <br />
                       <br>
                   <h3> Plant 2 </h3>
                       <label for="plant_2_name">Plant Name</label><br>
                       <input type="text" id="plant_2_name" name="plant_2_name" value=%s><br>
                       <label for="moisture_percent_2">Plant Desired Moisture</label><br>
                       Wet <input type="range" min="1" max="100" value=%s class="slider" name="moisture_percent_2" id="moisture_percent_2"> Dry <br />
                       <br>
                   <h3> Plant 3 </h3>
                       <label for="plant_3_name">Plant Name</label><br>
                       <input type="text" id="plant_3_name" name="plant_3_name" value=%s><br>
                       <label for="moisture_percent_3">Plant Desired Moisture</label><br>
                       Wet <input type="range" min="1" max="100" value=%s class="slider" name="moisture_percent_3" id="moisture_percent_3"> Dry <br />
                       <br>
                       
               </form>
               
               <form action="/calibrate">
                  <input type="submit" value="Calibrate Sensors" />
               </form
            
        </body>
    </html>
    """ % (MicroWebSrv2.HTMLEscape(plants['0'].name), plants['0'].desired_moisture_percent * 100,
           MicroWebSrv2.HTMLEscape(plants['1'].name), plants['1'].desired_moisture_percent * 100,
           MicroWebSrv2.HTMLEscape(plants['2'].name), plants['2'].desired_moisture_percent * 100,
           MicroWebSrv2.HTMLEscape(plants['3'].name), plants['3'].desired_moisture_percent * 100)
    #figure out ohow to get full name 
    request.Response.ReturnOk(content)
    
    

@WebRoute(POST, '/edit', name='edit2/2')
def RequestTestPost(microWebSrv2, request) :
    data = request.GetPostedURLEncodedForm()
    plants = water.get_plant_objects()
    try:
        moisture_percent_0 = float(data['moisture_percent_0']) / 100
        moisture_percent_1 = float(data['moisture_percent_1']) / 100
        moisture_percent_2 = float(data['moisture_percent_2']) / 100
        moisture_percent_3 = float(data['moisture_percent_3']) / 100
        plants['0'].update_desired_moisture_percent(moisture_percent_0)
        plants['1'].update_desired_moisture_percent(moisture_percent_1)
        plants['2'].update_desired_moisture_percent(moisture_percent_2)
        plants['3'].update_desired_moisture_percent(moisture_percent_3)
        plants['0'].update_name(data['plant_0_name'])
        plants['1'].update_name(data['plant_1_name'])
        plants['2'].update_name(data['plant_2_name'])
        plants['3'].update_name(data['plant_3_name'])
        water.write_plant_profiles()
    except :
        request.Response.ReturnBadRequest()
        return
    request.Response.ReturnRedirect('/saved') 
    
@WebRoute(GET, '/saved', name='saved')
def RequestTestPost(microWebSrv2, request) :    
    content = """\
     <!DOCTYPE html>
    <html>
        <head>
            <title>Plants</title>
        </head>
        <body>
            <h2>Changes Saved!</h2>
            
            <form action="/">
                <input type="submit" value="Home" />
            </form>
            
            <form action="/edit">
                <input type="submit" value="Edit Plants" />
            </form>
            
            <form action="/calibrate">
                <input type="submit" value="Calibrate Sensors" />
            </form
        </body>
    </html>
    """   
    
    request.Response.ReturnOk(content)

@WebRoute(POST, '/saved', name='saved')
def RequestTestPost(microWebSrv2, request) :    
    content = """\
     <!DOCTYPE html>
    <html>
        <head>
            <title>Plants</title>
        </head>
        <body>
            <h2>Changes Saved!</h2>
            
            <form action="/">
                <input type="submit" value="Home" />
            </form>
            
            <form action="/edit">
                <input type="submit" value="Edit Plants" />
            </form>
            
            <form action="/calibrate">
                <input type="submit" value="Calibrate Sensors" />
            </form
        </body>
    </html>
    """   
    
    request.Response.ReturnOk(content)
    
@WebRoute(GET, '/calibrate', name='calibrate1/2')
def RequestTestPost(microWebSrv2, request) :
    plants = water.get_plant_objects()
    content = """\
     <!DOCTYPE html>
    <html>
        <head>
            <title>Plants</title>
        </head>
        
        <form action="/">
                <input type="submit" value="Home" />
            </form>
        <form action="/edit">
                <input type="submit" value="Edit Plants" />
            </form>
            
        <body>
            <h2>Calibrate The Sensors</h2>
                <p> You need a cup of water for this.
                    Be careful changes can not be reversed
                </p>
                
                <ul>
                  <li>
                      <h3>Plant 0, Name: %s </h3>
                          <p> Make sure sensor is completley dry and refresh the page </p>
                          <p> Current Sensor Reading: %s </p>
                          <p> Current Sensor Max: %s </p>
                          
                          <form action="/plant_0_max">
                            <input type="submit" value="Calibrate Max Sensor Value" name="plant_0_max" />
                          </form>
                          
                          <p> Place sensor in a cup of water and refresh the page </p>
                          <p> Current Sensor Min: %s </p>
                          
                          <form action="/plant_0_min">
                            <input type="submit" value="Calibrate Min Sensor Value" name=plant_0_min />
                          </form>                          
                  </li>
                  <li>
                      <h3>Plant 1, Name: %s </h3>
                          <p> Make sure sensor is completley dry and refresh the page </p>
                          <p> Current Sensor Reading: %s </p>
                          <p> Current Sensor Max: %s </p>
                          
                          <form action="/plant_1_max">
                            <input type="submit" value="Calibrate Max Sensor Value" name="plant_1_max" />
                          </form>
                          
                          <p> Place sensor in a cup of water and refresh the page </p>
                          <p> Current Sensor Min: %s </p>
                          
                          <form action="/plant_1_min">
                            <input type="submit" value="Calibrate Min Sensor Value" name=plant_1_min />
                          </form>
                          
                  </li>
                  <li>
                      <h3>Plant 2, Name: %s </h3>
                          <p> Make sure sensor is completley dry and refresh the page </p>
                          <p> Current Sensor Reading: %s </p>
                          <p> Current Sensor Max: %s </p>
                          
                          <form action="/plant_2_max">
                            <input type="submit" value="Calibrate Max Sensor Value" name="plant_2_max" />
                          </form>
                          
                          <p> Place sensor in a cup of water and refresh the page </p>
                          <p> Current Sensor Min: %s </p>
                          
                          <form action="/plant_2_min">
                            <input type="submit" value="Calibrate Min Sensor Value" name=plant_2_min />
                          </form>   
                  </li>
                  <li>
                      <h3>Plant 3, Name: %s </h3>
                          <p> Make sure sensor is completley dry and refresh the page </p>
                          <p> Current Sensor Reading: %s </p>
                          <p> Current Sensor Max: %s </p>
                          
                          <form action="/plant_3_max">
                            <input type="submit" value="Calibrate Max Sensor Value" name="plant_3_max" />
                          </form>
                          
                          <p> Place sensor in a cup of water and refresh the page </p>
                          <p> Current Sensor Min: %s </p>
                          
                          <form action="/plant_3_min">
                            <input type="submit" value="Calibrate Min Sensor Value" name=plant_3_min />
                          </form>   
                  </li>
                </ul>
        </body>
        
    </html>
    """ % (plants['0'].name, plants['0'].check_moisture_sensor(), plants['0'].moisture_max, plants['0'].moisture_min,
           plants['1'].name, plants['1'].check_moisture_sensor(), plants['1'].moisture_max, plants['1'].moisture_min,
           plants['2'].name, plants['2'].check_moisture_sensor(), plants['2'].moisture_max, plants['2'].moisture_min,
           plants['3'].name, plants['3'].check_moisture_sensor(), plants['3'].moisture_max, plants['3'].moisture_min,
           )

    
    
    request.Response.ReturnOk(content)
    
@WebRoute(GET, '/plant_0_max', name='plant_0_max')
def PlantMax(microWebSrv2, request) :
    try:
        plants = water.get_plant_objects()
        plant = plants['0']
        plant.update_max()
        water.write_plant_profiles()
    except :
        request.Response.ReturnBadRequest()
        return
    request.Response.ReturnRedirect('/saved')
    
@WebRoute(GET, '/plant_1_max', name='plant_1_max')
def PlantMax(microWebSrv2, request) :
    try:
        plants = water.get_plant_objects()
        plant = plants['1']
        plant.update_max()
        water.write_plant_profiles()
    except :
        request.Response.ReturnBadRequest()
        return
    request.Response.ReturnRedirect('/saved')
    
@WebRoute(GET, '/plant_2_max', name='plant_2_max')
def PlantMax(microWebSrv2, request) :
    try:
        plants = water.get_plant_objects()
        plant = plants['2']
        plant.update_max()
        water.write_plant_profiles()
    except :
        request.Response.ReturnBadRequest()
        return
    request.Response.ReturnRedirect('/saved')
    
@WebRoute(GET, '/plant_3_max', name='plant_3_max')
def PlantMax(microWebSrv2, request) :
    try:
        plants = water.get_plant_objects()
        plant = plants['3']
        plant.update_max()
        water.write_plant_profiles()
    except :
        request.Response.ReturnBadRequest()
        return
    request.Response.ReturnRedirect('/saved')
        
@WebRoute(GET, '/plant_0_min', name='plant_0_min')
def PlantMin(microWebSrv2, request) :
    try:
        plants = water.get_plant_objects()
        plant = plants['0']
        plant.update_min()
        water.write_plant_profiles()
    except :
        request.Response.ReturnBadRequest()
        return
    request.Response.ReturnRedirect('/saved')
    
@WebRoute(GET, '/plant_1_min', name='plant_1_min')
def PlantMin(microWebSrv2, request) :
    try:
        plants = water.get_plant_objects()
        plant = plants['1']
        plant.update_min()
        water.write_plant_profiles()
    except :
        request.Response.ReturnBadRequest()
        return
    request.Response.ReturnRedirect('/saved')
    
@WebRoute(GET, '/plant_2_min', name='plant_2_min')
def PlantMin(microWebSrv2, request) :
    try:
        plants = water.get_plant_objects()
        plant = plants['2']
        plant.update_min()
        water.write_plant_profiles()
    except :
        request.Response.ReturnBadRequest()
        return
    request.Response.ReturnRedirect('/saved')
    
@WebRoute(GET, '/plant_3_min', name='plant_3_min')
def PlantMin(microWebSrv2, request) :
    try:
        plants = water.get_plant_objects()
        plant = plants['3']
        plant.update_min()
        water.write_plant_profiles()
    except :
        request.Response.ReturnBadRequest()
        return
    request.Response.ReturnRedirect('/saved')
    
    
    

# ============================================================================
# ============================================================================
# ============================================================================

def OnWebSocketAccepted(microWebSrv2, webSocket) :
    print('Example WebSocket accepted:')
    print('   - User   : %s:%s' % webSocket.Request.UserAddress)
    print('   - Path   : %s'    % webSocket.Request.Path)
    print('   - Origin : %s'    % webSocket.Request.Origin)
    if webSocket.Request.Path.lower() == '/wschat' :
        WSJoinChat(webSocket)
    else :
        webSocket.OnTextMessage   = OnWebSocketTextMsg
        webSocket.OnBinaryMessage = OnWebSocketBinaryMsg
        webSocket.OnClosed        = OnWebSocketClosed

# ============================================================================
# ============================================================================
# ============================================================================

def OnWebSocketTextMsg(webSocket, msg) :
    print('WebSocket text message: %s' % msg)
    webSocket.SendTextMessage('Received "%s"' % msg)

# ------------------------------------------------------------------------

def OnWebSocketBinaryMsg(webSocket, msg) :
    print('WebSocket binary message: %s' % msg)

# ------------------------------------------------------------------------

def OnWebSocketClosed(webSocket) :
    print('WebSocket %s:%s closed' % webSocket.Request.UserAddress)

# ============================================================================
# ============================================================================
# ============================================================================


# ============================================================================
# ============================================================================
# ============================================================================

print()

# Loads the PyhtmlTemplate module globally and configure it,
try:
    pyhtmlMod = MicroWebSrv2.LoadModule('PyhtmlTemplate')
    pyhtmlMod.ShowDebug = True
    pyhtmlMod.SetGlobalVar('TestVar', 12345)
except:
    pass

# Loads the WebSockets module globally and configure it,
try:
    wsMod = MicroWebSrv2.LoadModule('WebSockets')
    wsMod.OnWebSocketAccepted = OnWebSocketAccepted
except: pass
# Instanciates the MicroWebSrv2 class,
mws2 = MicroWebSrv2()

# SSL is not correctly supported on MicroPython.
# But you can uncomment the following for standard Python.
# mws2.EnableSSL( certFile = 'SSL-Cert/openhc2.crt',
#                 keyFile  = 'SSL-Cert/openhc2.key' )

# For embedded MicroPython, use a very light configuration,
mws2.SetEmbeddedConfig()

# All pages not found will be redirected to the home '/',
mws2.NotFoundURL = '/'

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

# ============================================================================
# ============================================================================
# ============================================================================

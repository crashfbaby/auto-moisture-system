import water
import wifimgr
from time import sleep
import machine
import gc

try:
  import usocket as socket
except:
  import socket

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D



def web_page():
    wetness = water.read_moisture_profiles()
    plant_1 = (wetness['0'] / 65535)*100
    plant_2 = (wetness['1'] / 65535)*100
    plant_3 = (wetness['2'] / 65535)*100
    plant_4 = (wetness['3'] / 65535)*100
    
    content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Wetness</title>
        </head>
        <body>
            <h2>How Wet do you want it?</h2>
            
            <form action="/home" method="post">
                Plant 1: Wet <input type="range" min="1" max="100" value="%(plant_1)" class="slider" id="moisture_pin_1"> Dry <br /> 
                Plant 2: Wet <input type="range" min="1" max="100" value="50" class="slider" id="moisture_pin_2"> Dry <br />
                Plant 3: Wet <input type="range" min="1" max="100" value="50" class="slider" id="moisture_pin_3"> Dry <br />
                Plant 4: Wet <input type="range" min="1" max="100" value="50" class="slider" id="moisture_pin_4"> Dry <br />
                <input type="submit" value="OK">
            </form>
        </body>
    </html>
    """ %int(plant_1)
    return content
try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', 80))
  s.listen(5)
except OSError as e:
  machine.reset()

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')
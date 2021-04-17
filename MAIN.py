import water
import usocket as socket
import gc

def web_page():
    wetness = water.read_moisture_profiles()
    content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Wetness</title>
        </head>
        <body>
            <h2>How Wet do you want it?</h2>
            
            <form action="/home" method="post">
                Plant 1:  <input type="range" min="1" max="100" value={} class="slider" id="moisture_pin_1"><br />
                Plant 2:  <input type="range" min="1" max="100" value={} class="slider" id="moisture_pin_2"><br />
                Plant 3:  <input type="range" min="1" max="100" value={} class="slider" id="moisture_pin_3"><br />
                Plant 4:  <input type="range" min="1" max="100" value={}  class="slider" id="moisture_pin_4"><br />
                <input type="submit" value="OK">
            </form>
        </body>
    </html>
    """.format(wetness['0'], wetness['1'], wetness['2'], wetness['3']) 
    return content

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

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
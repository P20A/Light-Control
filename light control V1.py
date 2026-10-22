import network
import socket
from machine import Pin

in1 = Pin(12,Pin.OUT)
in2 = Pin(13,Pin.OUT)
in1.value(1)
in2.value(1)

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="LightControl", password="14426Parsa@",authmode=network.AUTH_WPA_WPA2_PSK)
ip = ap.ifconfig()[0]
print("ESP32 IP:", ip)

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
def web_page():
    html = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Parsa's web controler</title>
        <style>
            button{width: 100px;height: 50px;margin: 10px;}
            a{text-decoration: none;color: black;}
            .flexer{display: flex;justify-content: center;align-items: center;margin-top: 50px;flex-direction: column;}
            .rowflex{flex-direction: row;}
            .width200{width: 200px;height: 70px;}
        </style>
    </head>
    <body class="flexer">
        <div class="flexer rowflex"><div class="flexer"><a href="/?key_one_on"><button>Lamp 1 on</button></a>
        <a href="/?key_one_off"><button>Lamp 1 off</button></a></div>
        <div class="flexer"><a href="/?key_two_on"><button>Lamp 2 on</button></a>
        <a href="/?key_two_off"><button>Lamp 2 off</button></a></div></div>   
        <a href="/?both_on"><button class="width200">Both lamps on</button></a>
        <a href="/?both_off"><button class="width200">Both lamps off</button></a>
    </body>
    </html>"""
    return html
    
while True:
    client, addr = s.accept()
    request = client.recv(1024).decode()

    if "/?key_one_on" in request:
        in1.value(0)
        response = "KeyOneOn"
    elif "/?key_one_off" in request:
        in1.value(1)
        response = "KeyOneOff"
    elif "/?key_two_on" in request:
        in2.value(0)
        response = "KeyTwoOn"
    elif "/?key_two_off" in request:
        in2.value(1)
        response = "KeyTwoOff"
    elif "/?both_on" in request:
        in1.value(0)
        in2.value(0)
        response = "BothOn"
    elif "/?both_off" in request:
        in1.value(1)
        in2.value(1)
        response = "BothOff"
    else:
        response = "ESP32 OK"

    response = web_page()
    client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    client.sendall(response)
    client.close()




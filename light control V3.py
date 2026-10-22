import network
import socket
from machine import Pin

in1 = Pin(12,Pin.OUT)
in2 = Pin(13,Pin.OUT)

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
        button {
            width: 200px;
            height: 70px;
            margin: 10px;
        }
        a {
            text-decoration: none;
            color: black;
        }
        .flexer {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 50px;
            flex-direction: column;
        }
        .rowflex {
            flex-direction: row;
        }
        #lamp1,#lamp2,#both{
            background-color: red;
        }
    </style>
</head>

<body class="flexer">
    <div class="flexer rowflex">
        <button id="lamp1" onclick="toggleLampOne()">Lamp 1</button>
        <button id="lamp2" onclick="toggleLampTwo()">Lamp 2</button>

    </div>
        <button id="both" onclick="toggleBoth()">Both</button>
</body>
<script>
    const lamp1 = document.getElementById("lamp1");
    const lamp2 = document.getElementById("lamp2");
    const both = document.getElementById("both");
    function toggleLampOne() {
        fetch('/keyone').then(res => res.text()).then(state => {
        
        if(lamp1.style.backgroundColor == "green"){
            lamp1.style.backgroundColor = "red";
        }
        else{
            lamp1.style.backgroundColor = "green";
        }
        });
    }
    function toggleLampTwo() {
        fetch('/keytwo').then(res => res.text()).then(state => {
        
        if(lamp2.style.backgroundColor == "green"){
            lamp2.style.backgroundColor = "red";
        }
        else{
            lamp2.style.backgroundColor = "green";
        }
        });
    }
    function toggleBoth() {
        fetch('/both').then(res => res.text()).then(state => {
        
        if(both.style.backgroundColor == "green"){
            both.style.backgroundColor = "red";
            lamp1.style.backgroundColor = "red";
            lamp2.style.backgroundColor = "red";
        }
        else{
            both.style.backgroundColor = "green";
            lamp1.style.backgroundColor = "green";
            lamp2.style.backgroundColor = "green";
        }
        });
    }
</script>
</html>"""
    return html
L1 = False
L2 = False
while True:
    client, addr = s.accept()
    request = client.recv(1024).decode()

    if "/keyone" in request:
        if L1:
            in1.value(1)
            L1 = False
        else:
            in1.value(0)
            L1 = True
        response = "one"
    elif "/keytwo" in request:
        if L2:
            in2.value(1)
            L2 = False
        else:
            in2.value(0)
            L2 = True
        response = "two"
    elif "/both" in request:
        if L1 or L2:
            in1.value(1)
            in2.value(1)
            L1 = False
            L2 = False
        else:
            in1.value(0)
            in2.value(0)
            L1 = True
            L2 = True
        response = "both"
    else:
        in1.value(1)
        in2.value(1)
        response = web_page()
    client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    client.sendall(response)
    client.close()
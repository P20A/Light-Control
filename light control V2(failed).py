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
    </style>
</head>

<body class="flexer">
    <div class="flexer rowflex">
        <a href=""><button class="" onclick="toggleLampOne()">Lamp 1</button></a>
        <a href=""><button class="" onclick="toggleLampTwo()">Lamp 2</button></a>
    </div>
    <a href=""><button class="" onclick="toggleBoth()">Both lamps</button></a>
</body>
<script>
    var L1 = false;
    var L2 = false;
    function toggleLampOne() {
        if (L1) {
            fetch('/keyoneoff').then(response => response.text()).then(data => { console.log(data) });
            L1 = false;
        }
        else {
            fetch('/keyoneon').then(response => response.text()).then(data => { console.log(data) });
            L1 = true;
        }
    }
    function toggleLampTwo() {
        if (L2) {
            fetch('/keytwooff').then(response => response.text()).then(data => { console.log(data) });
            L2 = false;
        }
        else {
            fetch('/keytwoon').then(response => response.text()).then(data => { console.log(data) });
            L2 = true;
        }
    }
    function toggleBoth() {
        if (L1 | L2) {
            fetch('/bothoff').then(response => response.text()).then(data => { console.log(data) });
            L1 = false;
            L2 = false;
        }
        else {
            fetch('/bothon').then(response => response.text()).then(data => { console.log(data) });
            L1 = true;
            L2 = true;
        }
    }
</script>
</html>"""
    return html

while True:
    client, addr = s.accept()
    request = client.recv(1024).decode()

    if "/keyoneoff" in request:
        in1.value(1)
    elif "/keyoneon" in request:
        in1.value(0)
    elif "/keytwooff" in request:
        in2.value(1)
    elif "/keytwoon" in request:
        in2.value(0)
    elif "/bothoff" in request:
        in1.value(1)
        in2.value(1)
    elif "/bothon" in request:
        in1.value(0)
        in2.value(0)
    else:
        response = web_page()
        client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        client.sendall(response)
        client.close()
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
    var L1 = false;
    var L2 = false;
    function toggleLampOne() {
        if(L1){
            fetch('/keyoneoff').then(res => res.text());
            L1 = false;
        }
        else{
            fetch('/keyoneon').then(res => res.text());
            L1 = true;
        }
        colors();
    }
    function toggleLampTwo() {
        if(L2){
            fetch('/keytwooff').then(res => res.text());
            L2 = false;
        }
        else{
            fetch('/keytwoon').then(res => res.text());
            L2 = true;
        }
        colors();
    }
    function toggleBoth() {
        if(L1 || L2){
            fetch('/bothoff').then(res => res.text());
            L1 = false;
            L2 = false;
        }
        else{
            fetch('/bothon').then(res => res.text());
            L1 = true;
            L2 = true;
        }
        colors();
    }
    function colors(){
        if(L1 && L2){
            both.style.backgroundColor = "green";
        }
        else{
            both.style.backgroundColor = "red";
        }
        if(L1){
            lamp1.style.backgroundColor = "green";
        }
        else{
            lamp1.style.backgroundColor = "red";
        }
        if(L2){
            lamp2.style.backgroundColor = "green";
        }
        else{
            lamp2.style.backgroundColor = "red";
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
        response = "keyoneoff"
    elif "/keyoneon" in request:
        in1.value(0)
        response = "keyoneon"
    elif "/keytwooff" in request:
        in2.value(1)
        response = "keytwoon"
    elif "/keytwoon" in request:
        in2.value(0)
        response = "keytwoon"
    elif "/bothoff" in request:
        in1.value(1)
        in2.value(1)
        response = "bothoff"

    elif "/bothon" in request:
        in1.value(0)
        in2.value(0)
        response = "bothon"
    else:
        in1.value(1)
        in2.value(1)
        response = web_page()
    client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    client.sendall(response)
    client.close()
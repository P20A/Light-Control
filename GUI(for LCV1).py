from tkinter import Tk,Button,Label,Entry
import requests
ESP32_IP = "192.168.4.1"
window = Tk()
window.title('Light Control           made by: P20A')
def KeyOneOn():
    requests.get(f"http://{ESP32_IP}/?key_one_on")  
def KeyOneOff():
    requests.get(f"http://{ESP32_IP}/?key_one_off")  
def KeyTwoOn():
    requests.get(f"http://{ESP32_IP}/?key_two_on")  
def KeyTwoOff():
    requests.get(f"http://{ESP32_IP}/?key_two_off")  
def BothOn():
    requests.get(f"http://{ESP32_IP}/?both_on")  
def BothOff():
    requests.get(f"http://{ESP32_IP}/?both_off")  
upBtn = Button(window,text= 'Lamp 1 on',command=KeyOneOn)
upBtn.pack()
downBtn = Button(window,text= 'Lamp 1 off',command=KeyOneOff)
downBtn.pack()
leftBtn = Button(window,text= 'Lamp 2 on',command=KeyTwoOn)
leftBtn.pack()
rightBtn = Button(window,text= 'Lamp 2 off',command=KeyTwoOff)
rightBtn.pack()
stopBtn = Button(window,text= 'Both lamps on',command=BothOn)
stopBtn.pack()
checkWifiBtn = Button(window,text= 'Both lamps off',command=BothOff)
checkWifiBtn.pack()

window.geometry('400x300')
window.mainloop()
import network
import socket
import ssd1306
from time import sleep
import machine
import json
from umqtt.simple import MQTTClient



# Network
ssid = "KME662"
pwd = "######"


# Display
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Buttons
SW0 = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)

# Leds
D1 = machine.PWM(machine.Pin(22, machine.Pin.OUT))
D2 = machine.PWM(machine.Pin(21, machine.Pin.OUT))
D3 = machine.PWM(machine.Pin(20, machine.Pin.OUT))

# JSON msg
msg = '{"topic":"josiaPico","msg":"message from Pico"}'

# Global
ip = ''

# Const
PWM_VALUE = 65535


# Connect to class wlan
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, pwd)
    while wlan.isconnected() == False:
        print("Waiting...")
        sleep(1)
    print("Connected")
    global ip
    ip = wlan.ifconfig()[0]
    displayIP(ip)
    
    
def displayIP(ipAdd):
    display.text("IP:", 0, 1)
    display.text(str(ipAdd), 0, 10)
    display.show()
    
def displayLEDS():
    display.fill(0)
    displayIP(ip)
    d1Val = D1.duty_u16() / PWM_VALUE * 100
    d2Val = D2.duty_u16() / PWM_VALUE * 100
    d3Val = D3.duty_u16() / PWM_VALUE * 100
    display.text("D1:", 0, 25)
    display.text("D2:", 0, 35)
    display.text("D3:", 0, 45)
    display.text(str(int(d1Val + 1)), 25, 25)
    display.text(str(int(d2Val + 1)), 25, 35)
    display.text(str(int(d3Val + 1)), 25, 45)
    display.text("%", 50, 25)
    display.text("%", 50, 35)
    display.text("%", 50, 45)
    display.show()
    
    
def sub_cb(topic, msg):
    print((topic, msg))
    string = msg.decode('UTF-8')
    led, brightness = string.split(";")
    
    brightness = float(brightness) / 100
    print(brightness)
    brightness = brightness * PWM_VALUE
    print(brightness)
    if led == "D1":
        D1.duty_u16(int(brightness - 1))
    elif led == "D2":
        D2.duty_u16(int(brightness - 1))
    elif led == "D3":
        D3.duty_u16(int(brightness - 1))
    displayLEDS()
    


    
def main():
    
    displayLEDS()
    connect()
        
    Client = MQTTClient("343gr3", "192.168.1.254")
    Client.set_callback(sub_cb)
    Client.connect()
    Client.subscribe(b"josia/LED")
    while True:
        
        if SW0.value() == 0:
            tmp = json.loads(msg)
            Client.publish(tmp["topic"], tmp["msg"])
            print("succeed")
            break
        Client.check_msg()
        sleep(1)
        
        
                
                
    Client.disconnect()
    
if __name__ == "__main__":
    main()
    

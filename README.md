# Raspberry Pico W & MQTT
This is small project done in school as part of IoT connecting course. 
<br><brYou can controll Pico W leds trough your browser. Pico W also displays data on its LCD screen. It shows it's IP address and percentage of how bright each led is currently. Pico W can also publish MQTT message trough button press.

![]() <img src="https://github.com/JosiaOrava/picoW/blob/main/img/server.PNG" width="400">
![]() <img src="https://github.com/JosiaOrava/picoW/blob/main/img/picoW.jpg" width="400">

## Technologies used
This was made with the following tech:
* HTML
* Node Express
* MQTT
* MicroPython
<br><br> Browser has a very basic HTML site for entering data. Server is running in Node express and message protocol is MQTT. In the Pico W there is running MicroPython script. 

## What I learned
This teached using Node Express routes for the server and also working with MicroPython in the embedded device. On top of this it also teached the use of MQTT in both server side and also client side.
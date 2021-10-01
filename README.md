# Dash
This code uses Python and Kivy. It was created to receive and transmit CAN with an ECU. Our team uses a Motec system.
'Dash' is the original code that was created. The 'Dash with Buttons' is our newest code that we use. This code can be used with physical buttons to navigate the dash. The buttons are connected to the GPIO pins on the Raspberry Pi. 
## Materials
Raspberry Pi <br />
CANable USB to CAN adapter 
  https://canable.io/ <br />
Raspberry Pi compatible touch screen <br />
Micro SD card 32GB class10 U1
 

## Tips

Kivy introduction Youtube playlist https://youtube.com/playlist?list=PLzMcBGfZo4-kSJVMyYeOQ8CXJ3z1k7gHn  <br />

To test the code on a computer comment out line 133

`CanBus = can.ThreadSafeBus(interface='socketcan', channel='can0', bitrate=1000000)` <br />

and line 2 <br />

`import can`<br />

For 'Dash with Buttons' the settings screen is hidden in the top right corner over the 'ODO'.<br />

In the Raspberry Pi the kivy and python files with the pictures should be located in `/home/pi/Dash`. The files should also keep the same name, main.kv and main.py. 



## Screen


![basic Page](Pictures/Picture1.png)
##### Figure 1: Main Screen


![basic Page](Pictures/Picture2.png)
##### Figure 2: Drive Mode 
This screen uses CAN to select drive setups in the ECU.


![basic Page](Pictures/Picture3.png)
##### Figure 3: Brake



![basic Page](Pictures/Picture4.png)
##### Figure 4: Suspension


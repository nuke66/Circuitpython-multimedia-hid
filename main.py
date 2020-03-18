""" 
Use device as HID (keyboard) to send multimedia and keystrokes to attached PC.

This example uses Adafruit Trinket M0 and a CMOS 4021 8x input PISO to connect 8 different switches.
Each switch set up to do a different function.  Note: any unused inputs should be tied to ground.  As input 8 is 
unused it is connected to ground.

CD4021 pin connections:
           
Pin  |  Description  | Comments
-----+---------------+---------------------
1       Input 8        Connect to gnd
2       -
3       Serial out     D2 on Trinket
4       Input 4        Connect to swtich
5       Input 3        Connect to switch
6       Input 2        Connect to switch
7       Input 1        Connect to switch
8       Ground         Connect to ground
9       Load (latch)   D0 on Trinket
10      Clock          D3 on Trinket
11      Serial In      Connect to ground
12      - 
13      Input 5        Connect to switch
14      input 6        Connect to switch
15      Input 7        Connect to switch
16      Vcc            Connect to power
"""
import time
import board
import digitalio
import simpleio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import usb_hid
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl

# set up multimedia device
cc = ConsumerControl(usb_hid.devices)

# set up hid
kbd = Keyboard(usb_hid.devices)

# set up clock, data, and latch pins
clk = digitalio.DigitalInOut(board.D3)
clk.direction = digitalio.Direction.OUTPUT
data = digitalio.DigitalInOut(board.D2)
data.direction = digitalio.Direction.INPUT
latch = digitalio.DigitalInOut(board.D0)
latch.direction = digitalio.Direction.OUTPUT

# insert a small pause after keypress
def qpause():
    time.sleep(0.2)

while True:
    latch.value = False
    rs= simpleio.shift_in(data, clk)
    print("switches: {0:#010b} {0}".format(rs),end="")
    latch.value = True
    
    # more keypress codes
    # kbd.send(Keycode.CONTROL, Keycode.V)
    # kbd.send(Keycode.CONTROL, Keycode.X) 
    # cc.send(ConsumerControlCode.MUTE)
        
    if rs==1:
        cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        qpause()
    if rs==2:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        qpause()
    if rs==4:
        cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
        qpause()
    if rs==8:
        kbd.send(Keycode.F12)
        qpause()
    if rs==16:
        cc.send(ConsumerControlCode.MUTE)
        qpause()
    if rs==32:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        qpause()
    if rs==64:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        qpause()     

    time.sleep(0.05)

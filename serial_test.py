import usb.core
import usb.util
import time
import serial
from GeneralOutput import *

ser = serial.Serial(port='/dev/ttyUSB_DISPENSER',
                                baudrate = 115200,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=0)
while True:
	time.sleep(1)
	#ser.write(b'\x1C\x6C')
	#time.sleep(0.5)
	ser.write(b'\x10\x04\x14')
	time.sleep(0.5)
	printerstatus = ser.read(12)
	print(printerstatus[2])
	print(printerstatus[3])
	print(printerstatus)

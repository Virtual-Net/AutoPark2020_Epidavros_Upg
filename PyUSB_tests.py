import usb.core
import usb.util

VID = 0x067b
PID = 0x2303

dev1 = usb.core.find(idVendor=VID, idProduct=PID)
dev2 = usb.core.find(idVendor=VID, idProduct=PID)
print(dev1)
print(dev2)

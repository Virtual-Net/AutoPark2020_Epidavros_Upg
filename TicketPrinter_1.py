import usb.core
import usb.util
import os
import sys
import time


class TicketPrinter(object):
    def __init__(self, usb_port, usb_device):
        device = usb.core.find(idVendor=0x0dd4, idProduct=0x0203)
        # Was it found?
        if device is None:
            raise ValueError('Device not found')
        # Disconnect it from kernel
        needs_reattach = False
        if device.is_kernel_driver_active(0):
            needs_reattach = True
            device.detach_kernel_driver(0)
        # Set the active configuration. With no arguments, the first configuration will be the active one
        device.set_configuration()
        # get an endpoint instance
        cfg = device.get_active_configuration()
        intf = cfg[(0, 0)]
        ep = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        assert ep is not None
        self.up = usb_port
        self.ud = usb_device


    def printticket(self, barcode, timestamp, plate):
        self.up.write('\x1D\xF6')
        self.up.write('\x0A')
        self.up.write('\x1D\x21\x21')
        self.up.write('\x1B\x61\x31')
        self.up.write('\x1D\x77\x02')
        self.up.write('\x1D\x6B\x04123456789\x00')
        self.up.write('\x1B\x56\x01')
        self.up.write('\xAE \xAE \xAE\x0A')
        self.up.write('\x1B\x56\x00')
        self.up.write('POLISPARK\x0A\x0A')
        self.up.write('\x1D\x21\x11')
        self.up.write('DOUKISSIS\x0A')
        self.up.write('PLAKENTIAS\x0A')
        self.up.write('\x0A\x0A')
        self.up.write('\x1D\x21\x00')
        self.up.write('TEL: 210-7255420\x0A')
        self.up.write('DATE: 04-09-2019\x0A')
        self.up.write('TIME: 00:00:00\x0A')
        self.up.write('PLATE: YMN1679')
        self.up.write('\x0A')
        self.up.write('\x1D\xF8')
        self.up.write('\x1B\x69')
        self.up.write('\x1C\xC1\x1A')

    def getticket(self):
        self.up.write('\x10\x04\x14')
        while True:
            status = self.ud.read(0x81, 32)
            time.sleep(0.5)
            print(status)
            usb.write('\x10\x04\x14')




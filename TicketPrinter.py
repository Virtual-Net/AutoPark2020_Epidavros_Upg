import usb.core
import usb.util
import time
import serial
from GeneralOutput import *

class TicketPrinter(object):
    def __init__(self):
        self.ser = serial.Serial(port='/dev/ttyUSB_DISPENSER',
                                baudrate = 115200,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=0)
        

    def printticket(self, barcode, timestamp, datestamp, plate):
        self.ser.write(b'\x1D\xF6')#align ticket with the print head
        self.ser.write(b'\x1D\x21\x21')#character size
        self.ser.write(b'\x1B\x61\x31')#justification centered
        self.ser.write(b'\x1D\x77\x02')#barcode width
        self.ser.write(b'\x0A')#print line feed
        self.ser.write(b'\x1D\x6B\x04' + barcode.encode() + b'\x00')
        self.ser.write(b'\x1B\x7B\x00')#cancel upside-down printing
        self.ser.write(b'\x1B\x56\x01')#rotate text 90 degrees for printing arrows
        self.ser.write(b'\xAE \xAE \xAE\x0A')#print arrows
        self.ser.write(b'\x1B\x56\x00')#cancel rotate text 90 degrees 
        self.ser.write('PARKING'.encode() + b'\x0A\x0A')
        self.ser.write(b'\x1D\x21\x11')#smaller size
        self.ser.write('KYDON'.encode() + b'\x0A')
        self.ser.write('DHM.KH. A.E.'.encode() + b'\x0A')
        self.ser.write(b'\x0A\x0A')
        self.ser.write(b'\x1D\x21\x00')#change character size
        self.ser.write('TEL: 28210-99010'.encode() +b'\x0A')
        self.ser.write('DATE: '.encode() + datestamp.encode() + b'\x0A')
        self.ser.write('TIME: '.encode() + timestamp.encode() + b'\x0A')
        self.ser.write('PLATE: '.encode() + plate.encode())
        self.ser.write(b'\x0A')
        self.ser.write(b'\x1D\xF8')#align ticket @ cut
        self.ser.write(b'\x1B\x69')#total cut cmd
        self.ser.write(b'\x1C\xC1\x1A')#paper recovery after cut
        #self.ser.write(b'\x1D\xF6')#align ticket with the print head
        #self.ser.write(b'\x10\x04\x11')
        #time.sleep(0.2)
        #print('Last ticket: {}'.format(self.ser.read(32)))
        #self.ser.write(b'\x1C\xC1\x1A')#paper recovery after cut
        #self.ser.write(b'\x1C\x6C')
        #time.sleep(3)
        #self.ser.reset_input_buffer()
        #time.sleep(0.2)
        #self.ser.write(b'\x10\x04\x11')
        #time.sleep(0.2)
        #print('Last ticket: {}'.format(self.ser.read(32)))
        #time.sleep(0.2)

    def getticket(self):
        relays = GeneralOutput()
        self.ser.write(b'\x10\x04\x14')
        time.sleep(0.5)
        while True:
            time.sleep(0.5)
            self.ser.write(b'\x10\x04\x14')
            printerstatus = self.ser.read(32)
            print(printerstatus)
            #print(printerstatus[2:])
            print(printerstatus[2])
            print(printerstatus[3])
            #print(printerstatus[4])
            if printerstatus[2] == 32 and printerstatus[3] == 0 or printerstatus[2] == 100 and printerstatus[3] == 0:
                print('wait to retrieve ticket')
                self.ser.write(b'\x10\x04\x14')
                time.sleep(0.5)
            elif printerstatus[2] == 0 and printerstatus[3] == 0:
                relays.setbarrierpin()
                relays.resetbarrierpin()
                print('TICKET WAS RETRIEVED!!!')
                return True
                break
            '''elif printerstatus is None:
                print('wait to retrieve ticket')
                self.ser.write(b'\x10\x04\x14')
                time.sleep(0.5)'''
            """elif printerstatus[2] == 68:
                relays.setbarrierpin()
                relays.resetbarrierpin()
                print('TICKET WAS RETRIEVED!!!')
                return True
                break"""
        

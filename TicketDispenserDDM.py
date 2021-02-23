import time
import serial
from Logger_setup import logger


class TicketDispenserDDM(object):
    ticket_at_front = False
    ticket_at_back = False

    def __init__(self):
        self.ser = serial.Serial(port='/dev/ttyUSB_DISPENSER', baudrate=38400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

    def resetticketdispenser(self):
        self.ser.write(b'\x01\x01\x00\x01\x33\x32')
        logger.info('Ticket dispenser was reset')

    def intaketochipcmd(self):
        self.ser.write(b'\x01\x01\x00\x02\xCA\x01\xC9')
        logger.info('Send ticket dispenser intake to chip command')

    def ticketdispenserstatuscmd(self):
        self.ser.write(b'\x01\x01\x00\x01\x28\x29')
        logger.info('Send ticket dispenser read status command')

    def abortintaketochipcmd(self):
        self.ser.write(b'\x01\x01\x00\x01\xCB\xCA')
        logger.info('Send ticket dispenser abort intake to chip command')

    def returnticketcmd(self):
        self.ser.write(b'\x01\x01\x00\x01\xC6\xC7')
        logger.info('Send ticket dispenser eject command')

    def captureticketcmd(self):
        self.ser.write(b'\x01\x01\x00\x01\xC4\xC5')
        logger.info('Send ticket dispenser capture command')

    def getinfocmd(self):
        self.ser.write(b'\x01\x01\x00\x01\x72\x73')
        logger.info('Send ticket dispenser get info command')

    def getinput(self):
        self.ser.write(b'\x01\x01\x00\x02\x87\x01\x84')
        logger.info('Send ticket dispenser get input command')
        print(self.ser.write(b'\x01\x01\x00\x02\x87\x01\x84'))

    def abort(self):
        self.ser.write(b'\x01\x01\x00\x01\xC7\xC6')
        logger.info('Send ticket dispenser abort intake to chip command')

    def readticketdispenserresponse(self):
        time.sleep(0.5)
        ticketdispenserstatus = 0
        ticketdispenserstatus = self.ser.read(28)
        print(ticketdispenserstatus)
        ticketdispenserstatustr = str(ticketdispenserstatus)
        ticket_barcode = ticketdispenserstatustr[
                         ticketdispenserstatustr.find("=") + 1:ticketdispenserstatustr.find("\r")]
        # ticket_barcode = ticketdispenserstatustr[ticketdispenserstatustr.find(
        # "n\x00")+1:ticketdispenserstatustr.find("0")]
        ticket_barcode = ticket_barcode[:9]
        # ticket_barcode = str()
        # ticket_barcode = str(ticket_barcode)[2:10]
        print(ticket_barcode)
        return ticket_barcode, ticketdispenserstatus

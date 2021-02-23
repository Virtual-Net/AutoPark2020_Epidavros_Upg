import time
import serial
from Logger_setup import logger


class TicketDispenserAdel(object):
    ticket_at_front = False
    ticket_at_back = False

    def __init__(self):
        self.ser = serial.Serial(port='/dev/ttyUSB_DISPENSER', baudrate=19600, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, bytesize=serial.SEVENBITS, timeout=0.4)

    def getfirmware(self):
        self.ser.write(b'\x0202\x03')

    def resetticketdispenser(self):
        self.ser.write(b'\x02\x30\x31\x03')
        # print('r = {}'.format(r))
        logger.info('Ticket dispenser was reset')

    def intaketochipcmd(self):
        # print('djashjfhaskl')
        # self.ser.write(b'\x0205\x03')
        # time.sleep(0.2)
        self.ser.write(b'\x0204C\x03')
        logger.info('Send ticket dispenser intake to chip command')

    def disableintaketochipcmd(self):
        self.ser.write(b'\x0205\x03')
        logger.info('Send ticket dispenser disable intake to chip command')

    def barcodereadingcmd(self):
        self.ser.write(b'\x0206C0\x03')

    def ticketdispenserstatuscmd(self):
        self.ser.write(b'\x0203\x03')
        logger.info('Send ticket dispenser read status command')

    def abortintaketochipcmd(self):
        self.ser.write(b'\x01\x01\x00\x01\xCB\xCA')
        logger.info('Send ticket dispenser abort intake to chip command')

    def returnticketcmd(self):
        print('return ticket cmd')
        self.ser.write(b'\x02060E\x03')
        logger.info('Send ticket dispenser eject command')

    def captureticketcmd(self):
        self.ser.write(b'\x02\x30\x36\x30\x42\x03')
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
        # ticketdispenserstatus = 0
        ticketdispenserstatus = self.ser.readline()
        print(ticketdispenserstatus)
        # if len(ticketdispenserstatus) > 22:
        # ticket_barcode = ticketdispenserstatus[31:40]
        # print(ticket_barcode)
        ticketdispenserstatustr = str(ticketdispenserstatus)
        print(ticketdispenserstatustr)
        if "56C0" in ticketdispenserstatustr:
            ticket_barcode = ticketdispenserstatustr[
                             ticketdispenserstatustr.find("56C0") + 4:ticketdispenserstatustr.find("\x03") - 4]
        elif "56C2" in ticketdispenserstatustr:
            ticket_barcode = ticketdispenserstatustr[
                             ticketdispenserstatustr.find("56C2") + 4:ticketdispenserstatustr.find("\x03") - 4]
        elif "5600" in ticketdispenserstatustr:
            ticket_barcode = ticketdispenserstatustr[
                             ticketdispenserstatustr.find("5600") + 4:ticketdispenserstatustr.find("\x03") - 4]
        else:
            ticket_barcode = ticketdispenserstatustr[
                             ticketdispenserstatustr.find("56C3") + 4:ticketdispenserstatustr.find("\x03") - 4]

        # ticket_barcode = ticketdispenserstatustr[ticketdispenserstatustr.find(
        # "n\x00")+1:ticketdispenserstatustr.find("0")] ticket_barcode = ticket_barcode[:9] ticket_barcode = str()
        ticket_barcode = str(ticket_barcode)[0:9]
        # print ('Barcode: ' + ticket_barcode)
        return ticket_barcode, ticketdispenserstatus

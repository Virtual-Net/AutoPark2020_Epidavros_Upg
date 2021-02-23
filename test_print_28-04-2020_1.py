from dateutil.parser import parse
import datetime
from time import time as tm
"""
from HttpManagerTest import *
from TicketPrinter import *
"""
from escpos import printer
"""
tickprint = TicketPrinter
httpreq = HttpManagerTest()
resp, cont, head = httpreq.sendticketentrance("0")
contj = json.loads(cont.decode('utf-8'))
date_time = contj["entered_at"]
dt = parse(date_time)
contp = contj['vehicle']
contb = contj['ticket']
plate = contp['plate']
"""
dt = datetime.datetime.now()
date = str(dt.day) + '-' + str(dt.month) + '-' + str(dt.year)
time = str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)
barc = tm()
barc = str(round(barc*10))[2:]
plate = ".29013"
#barc = contb['code']
print(barc)


p = printer.Usb(0x0dd4, 0x0203, 0, 0x81, 0x2)
p.text('\x1D\xF6') #reload paper
p.text('\x1D\xE8\x00\x54')
p.text('\x1D\x77\x02')  # barcode width
p.text('\x1D\x6B\x04' + barc + '\x00')
p.text('\x1D\x21\x21')  # character size
p.text('\x1B\x56\x01')  # rotate text 90 degrees for printing arrows
p.text('< < < \x0A')  # print arrows
p.text('\x1B\x56\x00')  # cancel rotate text 90 degrees
p.set(align='center')
p.text('\x1D\x21\x21')  # character size
p.text('POLISPARK\x0A')
p.text('\x1D\x21\x11')  # smaller size
p.text('DOUKISSIS\x0A')
p.text('PLAKENTIAS\x0A')
p.text('\x0A\x0A')
p.text('\x1D\x21\x00')  # change character size
p.text('TEL: 210-7255420\x0A')
p.text('DATE: ' + date + '\x0A')
p.text('TIME: ' + time + '\x0A')
p.text('PLATE: ' + plate + '\x0A')
#p.text('\x0A')
p.text('\x1D\xF8')  # align ticket @ cut
p.text('\x1B\x69')  # total cut cmd




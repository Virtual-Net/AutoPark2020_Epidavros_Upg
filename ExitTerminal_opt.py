#!/usr/bin/python
# coding=utf-8
import time
import queue
import signal
import threading
from tkinter import *
from dateutil.parser import parse
import sys
import select
# from inputimeout import inputimeout, TimeoutOccurred
# internal imports
from HttpManager import *
from RFIDReader import *
from GeneralInput import *
from TicketDispenserDDM import *
from TicketDispenserAdel import *
# from BarcodeHandler import *
# from Barcode import *
from Logger_setup import logger
import json
import socket

TIMEOUT = 0.1
messageflag = False
enabledispenser = False
IP_PORT = 7000
HOSTNAME = ""


class GuiPart:

    def __init__(self, master, queue, endCommand):
        self.queue = queue
        self.GUI = Tk()
        self.master2 = master
        #self.GUI.attributes('-fullscreen', True)

        self.F1 = Frame(self.GUI)
        self.F1 = Frame(self.GUI, width=400, height=200)
        self.F1.place(height=500, width=400, x=100, y=100)
        self.F1.config()

        self.F1.grid(columnspan=10, rowspan=10)
        self.F1.grid_rowconfigure(0, weight=1)

        self.photo = PhotoImage(master=self.GUI, file="/home/pi/AutoPark2020_optimization/Images/DCS_2502.png")
        self.label = Label(self.GUI, image=self.photo)
        self.label.image = self.photo  # keep a reference!
        self.label.grid(row=0, column=0, columnspan=20, rowspan=30)

        self.line1 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 20 bold")
        self.line1.grid(row=8, column=3)
        self.line2 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
        self.line2.grid(row=9, column=3)
        self.line3 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
        self.line3.grid(row=10, column=3)
        self.line4 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 20 bold")
        self.line4.grid(row=13, column=3)
        self.line5 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
        self.line5.grid(row=14, column=3)
        self.line6 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
        self.line6.grid(row=15, column=3)
        # Add more GUI stuff here depending on your specific needs

    def processIncoming(self, msgc):
        """Handle all messages currently in the queue, if any."""
        # while self.queue.qsize():
        try:
            # msg = self.queue.get(0)
            msg = msgc
            # Check contents of message and do whatever is needed. As a
            # simple test, print it (in real life, you would
            # suitably update the GUI's display in a richer fashion).
            logger.info(msg)
            if msg == 1:
                logger.info('update messages')
                self.line1['text'] = "WELCOME"
                self.line2['text'] = "INSERT YOUR TICKET"
                self.line3['text'] = "OR YOUR CARD"
                self.line4['text'] = "??????????????????????"
                self.line5['text'] = "???????????????? ???? ??????????????????"
                self.line6['text'] = "?? ?????? ?????????? ??????"
                # self.master2.after(200, ThreadedClient.periodicCall(self))
                # ThreadedClient.root.after(200, ThrededClient.periodicCall)
            elif msg == 2:
                logger.info('update messages')
                self.line1['text'] = ""
                self.line2['text'] = ""
                self.line3['text'] = ""
                self.line4['text'] = ""
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(200, ThreadedClient.periodicCall(self))
                # ThreadedClient.root.after(200, ThrededClient.periodicCall)
            elif len(str(msg)) > 4:
                logger.info('update messages')
                self.line1['text'] = "PLEASE"
                self.line2['text'] = "WAIT"
                self.line3['text'] = "????????????????"
                self.line4['text'] = "????????????????????"
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(200, ThreadedClient.periodicCall(self))
                # ThreadedClient.root.after(800, ThrededClient.periodicCall)
            elif msg == 201:
                logger.info('update messages')
                self.line1['text'] = "VALID EXIT"
                self.line2['text'] = "THANK YOU"
                self.line3['text'] = "???????????? ??????????"
                self.line4['text'] = "????????????????????????"
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(1000, ThreadedClient.periodicCall(self))
                # ThreadedClient.root.after(1000, ThrededClient.periodicCall)
            elif msg == 405:
                logger.info('update messages')
                self.line1['text'] = "CARD NOT"
                self.line2['text'] = "REGISTERED"
                self.line3['text'] = "???? ????????????????????????"
                self.line4['text'] = "??????????"
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(4000, ThreadedClient.periodicCall(self))
                # ThreadedClient.root.after(4000, ThrededClient.periodicCall)
            elif msg == 406:
                logger.info('update messages')
                self.line1['text'] = "BOOKING NOT"
                self.line2['text'] = "FOUND"
                self.line3['text'] = "?????? ??????????????"
                self.line4['text'] = "??????????????"
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(4000, ThreadedClient.periodicCall(self))
                # ThreadedClient.root.after(4000, ThrededClient.periodicCall)
            elif msg == 404:
                logger.info('update messages')
                self.line1['text'] = "TICKET NOT"
                self.line2['text'] = "FOUND"
                self.line3['text'] = "?????? ??????????????"
                self.line4['text'] = "??????????????????"
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(4000, ThreadedClient.periodicCall(self))
                # ThreadedClient.root.after(4000, ThrededClient.periodicCall)
            elif msg == 503:
                logger.info('update messages')
                self.line1['text'] = "VEHICLE"
                self.line2['text'] = "ALREADY EXITED"
                self.line3['text'] = "???? ?????????? ????????"
                self.line4['text'] = "?????? ??????????????"
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(4000, ThreadedClient.periodicCall(self))
                # threading.Timer(4, ThreadedClient.periodicCall).start()
            elif msg == 504:
                logger.info('update messages')
                self.line1['text'] = "YOU MUST PAY"
                self.line2['text'] = "BEFORE EXIT"
                self.line3['text'] = "???????????? ???? ??????????????????"
                self.line4['text'] = "???????? ?????? ??????????"
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(4000, ThreadedClient.periodicCall(self))
                # threading.Timer(4, ThreadedClient.periodicCall).start()
            elif msg == 505:
                logger.info('update messages')
                self.line1['text'] = "PLEASE"
                self.line2['text'] = "TRY AGAIN"
                self.line3['text'] = "????????????????"
                self.line4['text'] = "??????????????????????????????"
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(4000, ThreadedClient.periodicCall(self))
                # threading.Timer(4, ThreadedClient.periodicCall).start()
            elif msg == 506:
                logger.info('update messages')
                self.line1['text'] = "PLEASE RETRIEVE"
                self.line2['text'] = "YOUR TICKET"
                self.line3['text'] = "???????????????? ????????????????????"
                self.line4['text'] = "???? ?????????????????? ??????"
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(4000, ThreadedClient.periodicCall(self))
                # threading.Timer(4, ThreadedClient.periodicCall).start()
            elif msg == 507:
                logger.info('update messages')
                self.line1['text'] = "PLEASE CONTACT"
                self.line2['text'] = "THE CASHIER"
                self.line3['text'] = "???????????????? ??????????????????????????"
                self.line4['text'] = "???? ???? ????????????"
                self.line5['text'] = ""
                self.line6['text'] = ""
                # self.master2.after(4000, ThreadedClient.periodicCall(self))
                # threading.Timer(4, ThreadedClient.periodicCall).start()
        except queue.Empty:
            # self.master2.after(200, ThreadedClient.periodicCall)
            print('QUEUE IS EMPTY')
            # just on general principles, although we don't
            # expect this branch to be taken in this case
            # threading.Timer(0.2, ThreadedClient.periodicCall).start()
            pass


class SocketHandler:
    def __init__(self, conn):
        self.conn = conn

    def run(self):
        logger.info("SocketHandler started")
        cmd = ""
        try:
            logger.info("Calling blocking conn.recv()")
            cmd = str(self.conn.recv(1024))
            print(cmd)
        except:
            logger.info("exception in conn.recv()") 
            # happens when connection is reset from the peer
        logger.info("Received cmd: " + cmd + " len: " + str(len(cmd)))
        #if len(cmd) == 0:
        #self.executeCommand(cmd)
        self.conn.close()
        #print "Client disconnected. Waiting for next client..."
        logger.info("SocketHandler terminated")

class ThreadedClient:
    """Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place."""
    rfid = RFIDReader()
    httpreq = HttpManager()
    loopinfo = GeneralInput()
    # qrcode = Barcode()
    messageflag = False
    enabledispenser = False
    ticket_at_front = False
    timer = time.time()
    looptimer = 0
    with open('/home/pi/AutoPark2020_optimization/TerminalSettings.json') as json_file:
            data = json.load(json_file)
    dispensername = data['dispenser-type']
    looptimerset = data["loop-time"]
    looptimerset = int(looptimerset)
    ticketdispenser_ = globals()['TicketDispenser' + dispensername]()

    def __init__(self, master):
        """Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O)."""
        self.master = master
        self.machinestate = 0
        r = 1

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=getattr(self, 'workerThreadDispenser' + self.dispensername))
        self.thread1.start()
        self.thread2 = threading.Thread(target=self.workerThreadRFID)
        self.thread2.start()
        self.thread3 = threading.Thread(target=self.workerThreadQrCode)
        self.thread3.start()
        self.thread4 = threading.Thread(target=self.workerThreadListener)
        self.thread4.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()
        # self.gui.processIncoming()


    def periodicCall(self):
        """Check every 200 ms if there is something new in the queue."""
        # self.gui.processIncoming()
        try:
            msgc = self.msg
            # print(self.queue.get(0))
            # print("The check msg: " + str(msgc))
            if msgc == 1 or msgc == 506:
                self.gui.processIncoming(msgc)
                self.master.after(50, self.periodicCall)
                self.messageflag = True
            if msgc == 2:
                self.gui.processIncoming(msgc)
                self.master.after(50, self.periodicCall)
                self.messageflag = False
            if msgc == 201 or msgc == 505:
                self.gui.processIncoming(msgc)
                self.master.after(2000, self.periodicCall)
                self.messageflag = False
            if msgc == 404 or msgc == 503 or msgc == 504 or msgc == 405 or msgc == 406 or msgc == 505 or msgc == 507:
                self.gui.processIncoming(msgc)
                self.master.after(4000, self.periodicCall)
                self.messageflag = False
        except:
            self.master.after(50, self.periodicCall)
            print("periodic exception")
            pass
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        # self.gui.processIncoming()

    def looptimer_tick(self):
        self.machinestate = 0

    def interrupted(self):
        "called when read times out"
        qrcodereading = raw_input()
        logger.info('...' + qrcodereading)
        return

    def workerThreadDispenserAdel(self):
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            loopstate = self.loopinfo.readloopstate()
            time.sleep(0.2)
            if loopstate == 1 or self.looptimer < self.looptimerset:
                #self.looptimer =float(time.time() - self.timer)
                logger.info('loop was activated')
                self.ticketdispenser_.ticketdispenserstatuscmd()
                ticketdispenserbarc, ticketdispenserrespcmd = self.ticketdispenser_.readticketdispenserresponse()
                # print(ticketdispenserrespcmd[9])
                # if ticketdispenserrespcmd[3] == 5:
                #    pass
                # logger.info('no ticket @ front')
                # if ticketdi spenserrespcmd[3] == 3 or ticketdispenserrespcmd[13] == 3 and len(str(ticketdispenserrespcmd)) >= 30:
                # elif ticketdispenserrespcmd[9] == 4:
                #    logger.info('TICKET DETECTED')
                #    self.ticketdispenser_.intaketochipcmd()
                try:
                    if ticketdispenserrespcmd[9] == 48:
                        self.enabledispenser = False
                        self.messageflag = False
                        self.ticket_at_front = False
                        print('no ticket @ front')
                        logger.info('no ticket @ front')
                        pass
                    if ticketdispenserrespcmd[9] == 49 and self.enabledispenser == True and self.ticket_at_front == True:
                        print('WAIT TO RETRIEVE TICKET')
                        logger.info('WAIT TO RETRIEVE TICKET')
                        self.messageflag = True
                        self.msg = 506
                    if ticketdispenserrespcmd[9] == 49 and self.enabledispenser == False:
                        # ticketdispenserbarc, ticketdispenserrespcmd = self.ticketdispenser_.readticketdispenserresponse()
                        # print("Status: " + ticketdispenserbarc)
                        # time.sleep(0)
                        print('TICKET DETECTED')
                        logger.info('TICKET DETECTED')
                        self.enabledispenser = True
                        self.ticketdispenser_.intaketochipcmd()
                        # ticketdispenser_.disableintaketochipcmd()
                        # ticketdispenser_.barcodereadingcmd()
                except:
                    pass
                    # self.ticketdispenser_.getinput()
                # self.machinestate = 1
                # looptimer = threading.Timer(10.0, self.looptimer_tick)
                # looptimer.start()
                if self.messageflag == False:
                    self.msg = 1
                    # self.queue.put(msg)
                # time.sleep(0.5)
                print('Barcode = ' + ticketdispenserbarc)
                logger.info('Barcode = ' + ticketdispenserbarc)
                if ticketdispenserbarc == '\\x03\\x06\\' or ticketdispenserbarc == '' :
                    self.msg = 505
                    self.ticketdispenser_.returnticketcmd()
                if 'x' not in ticketdispenserbarc:
                    print("BARCODE = " + ticketdispenserbarc)
                    logger.info("BARCODE = " + ticketdispenserbarc)
                    #print(int(ticketdispenserbarc))
                    # self.ticketdispenser_.getinput()
                    try:
                        resp, cont, head = self.httpreq.sendticketexit(ticketdispenserbarc)
                        c = json.loads(cont.decode('utf-8'))
                        self.msg = resp
                        #print('resp= ' + int(resp))
                        if self.msg == 503:
                            # self.ticketdispenser_.returnticketcmd()
                            # time.sleep(0.3)
                            # ticketdispenser_.resetticketcmd()
                            # time.sleep(2)
                            # self.enabledispenser = True
                            # ticketdispenser_.ticketdispenserstatuscmd()
                            # ticketdispenserrespcmd = ticketdispenser_.readticketdispenserresponse()
                            # print('...' + ticketdispenserrespcmd[9])
                            # while ticketdispenserrespcmd[9] == 49:
                            # self.msg = 506
                            # self.queue.put(msg)
                            # print('wait to retrieve ticket')
                            # else:
                            # self.enabledispenser = False
                            # return
                            ex = str(c['exception'])
                            #print
                            #print(ex)
                            logger.info(ex)
                        if self.msg == 503 and ex == "TicketNotPaidException":
                            self.msg = self.msg + 1
                            print(ex)
                            # print(type(msg))
                            #self.ticketdispenser_.returnticketcmd()
                            # time.sleep(0.3)
                            # ticketdispenser_.resetticketcmd()
                            # time.sleep(0.3)
                        if self.msg == 503 and ex == "VehicleAlreadyExitedException":
                            self.msg = 503
                            print(ex)
                        if self.msg == 503 and ex != "TicketNotPaidException" and ex != "VehicleAlreadyExitedException":
                            self.msg = self.msg +4
                            print(ex)
                            #self.ticketdispenser_.returnticketcmd()
                        #if self.msg == 404:
                            #self.ticketdispenser_.returnticketcmd()
                        self.httpreq.receive_ticket_exit(resp)
                        self.ticket_at_front = True
                    except:
                        print("BARCODE EXCEPTION")
                        pass
                    #self.httpreq.receive_ticket_exit(resp)
                timeout = 1
                print('timer= ' + str(self.looptimer))
                self.looptimer =float(time.time() - self.timer)
                # self.enabledispenser = False
                '''i, o, e = select.select([sys.stdin], [], [], timeout)
                if i:
                    qrcodereading = sys.stdin.readline().strip()
                    logger.info("qrcode: " + qrcodereading)
                else:
                    logger.info('no qrcode')'''
            elif loopstate == 0 or self.looptimer > self.looptimerset:
                self.ticketdispenser_.ticketdispenserstatuscmd()
                ticketdispenserbarc, ticketdispenserrespcmd = self.ticketdispenser_.readticketdispenserresponse()
                print(ticketdispenserrespcmd)
                if ticketdispenserrespcmd[10] == 49:
                    self.ticketdispenser_.returnticketcmd()
                if self.enabledispenser == False:
                    self.ticketdispenser_.returnticketcmd()
                    #self.ticketdispenser_.resetticketdispenser()
                    self.enabledispenser = True
                if self.messageflag == True:
                    self.msg = 2
                    
                #self.ticketdispenser_.returnticketcmd()
                self.timer = time.time()
                #self.looptimer =float(time.time() - self.timer)
                #self.ticketdispenser_.resetticketdispenser()
                    # self.queue.put(msg)

    def workerThreadDispenserDDM(self):
        """This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise."""
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            loopstate = self.loopinfo.readloopstate()
            time.sleep(0.2)
            if loopstate == 1  or self.looptimer < self.looptimerset:
                logger.info('loop was activated')
                print(self.ticketdispenser_.ticketdispenserstatuscmd())
                ticketdispenserbarc, ticketdispenserrespcmd = self.ticketdispenser_.readticketdispenserresponse()
                print(ticketdispenserrespcmd)
                # if ticketdispenserrespcmd[3] == 5: pass logger.info('no ticket @ front') if ticketdispenserrespcmd[
                # 3] == 3 or ticketdispenserrespcmd[13] == 3 and len(str(ticketdispenserrespcmd)) >= 30: elif
                # ticketdispenserrespcmd[9] == 4: logger.info('TICKET DETECTED')
                # self.ticketdispenser_.intaketochipcmd()
                try:
                    if len(ticketdispenserrespcmd) <= 10:
                        logger.info('no ticket @ front')
                        pass
                    elif len(ticketdispenserrespcmd) > 10 and ticketdispenserrespcmd[3] == 3 or len(
                            ticketdispenserrespcmd) > 10 and ticketdispenserrespcmd[13] == 3:
                        # ticketdispenserbarc, ticketdispenserrespcmd =
                        # self.ticketdispenser_.readticketdispenserresponse()
                        print("Status: " + ticketdispenserbarc)
                        # time.sleep(0)
                        logger.info('TICKET DETECTED')
                        self.ticketdispenser_.intaketochipcmd()
                except:
                    pass
                    # self.ticketdispenser_.getinput()
                # self.machinestate = 1
                # looptimer = threading.Timer(10.0, self.looptimer_tick)
                # looptimer.start()
                if self.messageflag == False:
                    self.msg = 1
                    # self.queue.put(msg)
                # time.sleep(0.5)
                if 'b' not in ticketdispenserbarc:
                    print("BARCODE = " + ticketdispenserbarc)
                    print(type(ticketdispenserbarc))
                    # self.ticketdispenser_.getinput()
                    if '<' in ticketdispenserbarc:
                        self.msg = 505
                        self.ticketdispenser_.returnticketcmd()
                    try:
                        resp, cont, head = self.httpreq.sendticketexit(ticketdispenserbarc)
                        c = json.loads(cont.decode('utf-8'))
                        self.msg = resp
                        if self.msg == 503:
                            ex = str(c['exception'])
                            logger.info(ex)
                        if self.msg == 503 and ex == "TicketNotPaidException":
                            self.msg = self.msg + 1
                            # print(type(msg))
                        elif self.msg == 503 and ex != "TicketNotPaidException":
                            self.msg = self.msg + 4
                        self.httpreq.receive_ticket_exit(resp)
                    except:
                        logger.info("BARCODE EXCEPTION")
                        pass
                timeout = 1
                # self.enabledispenser = False
                '''i, o, e = select.select([sys.stdin], [], [], timeout)
                if i:
                    qrcodereading = sys.stdin.readline().strip()
                    logger.info("qrcode: " + qrcodereading)
                else:
                    logger.info('no qrcode')'''
            elif loopstate == 0 or self.looptimer > self.looptimerset:
                if self.enabledispenser == False:
                    self.ticketdispenser_.resetticketdispenser()
                    self.enabledispenser = True
                if self.messageflag == True:
                    self.msg = 2
                    # self.queue.put(msg)

    def workerThreadRFID(self):
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            loopstate = self.loopinfo.readloopstate()
            time.sleep(0.2)
            if loopstate == 1 or self.looptimer < self.looptimerset:
                logger.info('loop was activated')
                self.machinestate = 1
                #looptimer = threading.Timer(10.0, self.looptimer_tick)
                #looptimer.start()
                #if self.messageflag == False:
                    #self.msg = 1
                    # self.queue.put(msg)
                time.sleep(0.5)
                msg = self.rfid.readrf()
                if len(str(msg)) > 4:
                    result = self.httpreq.sendcardexit(str(msg))
                    self.httpreq.receive_card_exit(result)
                    self.msg = result
                    if self.msg == 404:
                        self.msg = self.msg + 1
                    # self.queue.put(msg)
                # self.enabledispenser = False
            elif loopstate == 0 and self.looptimer > self.looptimerset:
                if self.enabledispenser == False:
                    #self.ticketdispenser_.resetticketdispenser()
                    self.enabledispenser = True
                if self.messageflag == True:
                    self.msg = 2
                    # self.queue.put(msg)

    def workerThreadQrCode(self):
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            loopstate = self.loopinfo.readloopstate()
            barcode = '0'
            time.sleep(0.2)
            if loopstate == 1 or self.looptimer < self.looptimerset:
                logger.info('loop was activated')
                self.machinestate = 1
                #looptimer = threading.Timer(10.0, self.looptimer_tick)
                #looptimer.start()
                #if self.messageflag == False:
                    #self.msg = 1
                    # self.queue.put(msg)
                time.sleep(0.5)
                #barcode = input('scan the barcode \n')
                try:
                    barcode = inputimeout(prompt='scan the barcode \n',timeout=3)
                except:
                    pass
                # print("The barcode : " + str(len(barcode)))
                if len(barcode) == 9:
                    respQR, contQR, headQR = self.httpreq.sendbookedexit(barcode)
                    print(respQR)
                    self.msg = respQR
                    if self.msg == 404:
                        self.msg = self.msg + 2
                    if self.msg == 503:
                        ex = str(c['exception'])
                        logger.info(ex)
                    if self.msg == 503 and ex == "TicketNotPaidException":
                        self.msg = self.msg + 2
                    # self.queue.put(msg)
            elif loopstate == 0 and self.looptimer > self.looptimerset:
                if self.messageflag == True:
                    self.msg = 2
                    
    def workerThreadListener(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # close port when process exits:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        logger.info("Socket created")
        try:
            serverSocket.bind((HOSTNAME, IP_PORT))
        except socket.error as msg:
            #print "Bind failed:", msg[0], msg[1]
            sys.exit()
        serverSocket.listen(10)
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            relays = GeneralOutput()
            loopstate = self.loopinfo.readloopstate()
            time.sleep(0.2)
            self.machinestate = 1
            #if self.messageflag == False:
                #msg = 1
            #self.queue.put(msg)
            time.sleep(0.5)
            logger.info("Calling blocking accept()...")
    
            conn, addr = serverSocket.accept()
            data = str(conn.recv(1024))
            print("received message:" + data)
            data = data.split("msg=",1)[1]
            print(data)
            data = data.strip()
            print(data)
            data = data.replace("@'","")
            print(data)
            if(data == "0"):
                relays.setbarrierpin()
                relays.resetbarrierpin()
                self.msq = 200
                #self.queue.put(msg)
            #graphics_test.update()
            print("Connected with client at " + addr[0])
            #socketHandler = SocketHandler(conn)
            # necessary to terminate it at program termination:
            #socketHandler.setDaemon(True)  
            #socketHandler.run()
    

    def endApplication(self):
        self.running = 0


root = Tk()
root.withdraw()

client = ThreadedClient(root)
root.mainloop()

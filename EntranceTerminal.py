#!/usr/bin/python
# coding=utf-8
import queue
import signal
import threading
from tkinter import *
from dateutil.parser import parse
import sys
import select
from inputimeout import inputimeout, TimeoutOccurred
# internal imports
from HttpManager import *
from RFIDReader import *
from GeneralInput import *
from TicketPrinter import *
from NFCHandler import *
#from BarcodeHandler import *
#from Barcode import *
from Logger_setup import logger
import socket
import time

restoreID = 0
TIMEOUT = 0.1
IP_PORT = 7000
HOSTNAME = ""

class GuiPart:

    def __init__(self, master, queue, queue2, endCommand):
        self.queue = queue
        self.queueent = queue2
        self.GUI = Tk()
        self.GUI.attributes('-fullscreen', True)

        self.F1 = Frame(self.GUI)
        self.F1 = Frame(self.GUI, width=400, height=200)
        self.F1.place(height=500, width=400, x=100, y=100)
        self.F1.config()

        self.F1.grid(columnspan=10, rowspan=10)
        self.F1.grid_rowconfigure(0, weight=1)

        self.photo = PhotoImage(master=self.GUI, file="/home/pi/Autopark2020_optimization_epidavros/Images/DCS_2502.png")
        self.label = Label(self.GUI, image=self.photo)
        self.label.image = self.photo  # keep a reference!
        self.label.grid(row=0, column=0, columnspan=20, rowspan=30)

        self.line1 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 20 bold")
        self.line1.grid(row=8, column=9)
        self.line2 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
        self.line2.grid(row=9, column=9)
        self.line3 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
        self.line3.grid(row=10, column=9)
        self.line4 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 20 bold")
        self.line4.grid(row=13, column=9)
        self.line5 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
        self.line5.grid(row=14, column=9)
        self.line6 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
        self.line6.grid(row=15, column=9)
        # Add more GUI stuff here depending on your specific needs

    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize():
            try:
                entr = self.queueent.get(0)
                print("Entries: {}".format(entr))
            except:
                pass
            try:
                msg = self.queue.get(0)
                print("incoming msg: {}".format(msg))
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                logger.info(msg)
                if msg == 1:
                    #logger.info('update messages')
                    self.line1['text'] = "WELCOME"
                    self.line2['text'] = "INSERT YOUR CARD"
                    self.line3['text'] = ""
                    self.line4['text'] = "ΚΑΛΩΣΗΡΘΑΤΕ"
                    self.line5['text'] = "ΕΙΣΑΓΕΤΕ ΤΗΝ ΚΑΡΤΑ ΣΑΣ"
                    self.line6['text'] = ""
                elif msg == 2:
                    #logger.info('update messages')
                    self.line1['text'] = ""
                    self.line2['text'] = ""
                    self.line3['text'] = ""
                    self.line4['text'] = ""
                    self.line5['text'] = ""
                    self.line6['text'] = ""
                elif msg == 3:
                    #logger.info('update messages')
                    self.line1['text'] = "OUT OF"
                    self.line2['text'] = "ORDER"
                    self.line3['text'] = "ΕΚΤΟΣ"
                    self.line4['text'] = "ΛΕΙΤΟΥΡΓΙΑΣ"
                    self.line5['text'] = ""
                    self.line6['text'] = ""
                elif len(str(msg)) > 4:
                    #logger.info('update messages')
                    self.line1['text'] = "PLEASE"
                    self.line2['text'] = "WAIT"
                    self.line3['text'] = "ΠΑΡΑΚΑΛΩ"
                    self.line4['text'] = "ΠΕΡΙΜΕΝΕΤΕ"
                    self.line5['text'] = ""
                    self.line6['text'] = ""
                    #time.sleep(1)
                elif msg == 200 or msg == 201:
                    #logger.info('update messages')
                    self.line1['text'] = "VALID ENTRANCE"
                    self.line2['text'] = "THANK YOU"
                    self.line3['text'] = "ENTRIES: {}".format(entr)
                    self.line4['text'] = "ΕΙΣΟΔΟΣ ΔΕΚΤΗ"
                    self.line5['text'] = "ΕΥΧΑΡΙΣΤΟΥΜΕ"
                    self.line6['text'] = "ΕΙΣΟΔΟΙ: {}".format(entr)
                    #time.sleep(2)
                elif msg == 404:
                    logger.info('update messages')
                    self.line1['text'] = "CARD NOT"
                    self.line2['text'] = "REGISTERED"
                    self.line3['text'] = "ΜΗ ΚΑΤΑΧΩΡΗΜΕΝΗ"
                    self.line4['text'] = "ΚΑΡΤΑ"
                    self.line5['text'] = ""
                    self.line6['text'] = ""
                    #time.sleep(4)
                elif msg == 406:
                    #logger.info('update messages')
                    self.line1['text'] = "BOOK NOT"
                    self.line2['text'] = "FOUND"
                    self.line3['text'] = "ΔΕΝ ΒΡΕΘΗΚΕ"
                    self.line4['text'] = "ΚΡΑΤΗΣΗ"
                    self.line5['text'] = ""
                    self.line6['text'] = ""
                    #self.master2.after(4000, ThreadedClient.periodicCall(self))
                    #ThreadedClient.root.after(4000, ThrededClient.periodicCall)
                elif msg == 503:
                    logger.info('update messages')
                    self.line1['text'] = "VEHICLE"
                    self.line2['text'] = "ALREADY IN"
                    self.line3['text'] = "ΤΟ ΟΧΗΜΑ"
                    self.line4['text'] = "ΒΡΙΣΚΕΤΑΙ ΕΝΤΟΣ"
                    self.line5['text'] = ""
                    self.line6['text'] = ""
                    #time.sleep(4)
                elif msg == 504:
                    #logger.info('update messages')
                    self.line1['text'] = "PARKING"
                    self.line2['text'] = "FULL"
                    self.line3['text'] = "ΠΑΡΚΙΝΓΚ"
                    self.line4['text'] = "ΠΛΗΡΕΣ"
                    self.line5['text'] = ""
                    self.line6['text'] = ""
                elif msg == 505:
                    #logger.info('update messages')
                    self.line1['text'] = "PLEASE"
                    self.line2['text'] = "TRY AGAIN"
                    self.line3['text'] = "ΠΑΡΑΚΑΛΩ"
                    self.line4['text'] = "ΞΑΝΑΠΡΟΣΠΑΘΗΣΤΕ"
                    self.line5['text'] = ""
                    self.line6['text'] = ""
                    # self.master2.after(4000, ThreadedClient.periodicCall(self))
                    # threading.Timer(4, ThreadedClient.periodicCall).start()
            except Queue.Empty:
                print('QUEUE IS EMPTY')
                # just on general principles, although we don't
                # expect this branch to be taken in this case
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
    ticketbuttoninfo = GeneralInput()
    paperlevel = GeneralInput()
    #ticket = TicketPrinter()
    rfidblock = NFCHandler()
    #qrcode = Barcode()
    messageflag = False
    timer = time.time()
    looptimer = 0
    with open('/home/pi/Autopark2020_optimization_epidavros/TerminalSettings.json') as json_file:
        data = json.load(json_file)
    looptimerset = data["loop-time"]
    looptimerset = int(looptimerset)
    msg = 1

    def __init__(self, master):
        """Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O)."""
        self.master = master
        self.machinestate = 0
        # Create the queue
        self.queue = queue.Queue()
        self.queuechk = queue.Queue()
        self.queueent = queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.queueent, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        #self.thread1 = threading.Thread(target=self.workerThreadTicketButton)
        #self.thread1.start()
        self.thread2 = threading.Thread(target=self.workerThreadRFID)
        self.thread2.start()
        #self.thread3 = threading.Thread(target=self.workerThreadQrCode)
        #self.thread3.start()
        #self.thread4 = threading.Thread(target=self.workerThreadListener)
        #self.thread4.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """Check if there is something new in the queue.(time depends on message)"""
        self.gui.processIncoming()
        try:
            if self.queuechk.qsize():
                #self.gui.proccessIncoming()
                msgc = self.queuechk.get(0)
            #msgc = self.msg
                #time.sleep(0.1)
                if msgc == 1 or msgc == 506:
                    #print("CHECK: {}".format(msgc))
                    #self.gui.processIncoming()
                    if not self.running:
                        # This is the brutal stop of the system. You may want to do
                        # some cleanup before actually shutting it down.
                        import sys
                        sys.exit(1)
                    #self.MSGTimer(4)
                    #self.MSGTimer(0.05)
                    self.messageflag = True
                    self.master.after(50, self.periodicCall)
                    pass
                if msgc == 2:
                    #print(self.queue.get(0))
                    print("CHECK: {}".format(self.msg))
                    #self.gui.processIncoming()
                    if not self.running:
                        # This is the brutal stop of the system. You may want to do
                        # some cleanup before actually shutting it down.
                        import sys
                        sys.exit(1)
                    #self.master.after(50, self.periodicCall)
                    self.messageflag = False
                    self.master.after(50, self.periodicCall)
                    pass
                if msgc == 201 or msgc == 505 or msgc == 200:
                    print("CHECK: {}".format(msgc))
                    #self.gui.processIncoming()
                    if not self.running:
                        # This is the brutal stop of the system. You may want to do
                        # some cleanup before actually shutting it down.
                        import sys
                        sys.exit(1)
                    #self.MSGTimer(2)
                    #self.master.after(50, self.periodicCall)
                    self.messageflag = False
                    self.master.after(2000, self.periodicCall)
                    pass
                if msgc == 404 or msgc == 503 or msgc == 504 or msgc == 405 or msgc == 406 or msgc == 507:
                    #self.gui.processIncoming()
                    if not self.running:
                        # This is the brutal stop of the system. You may want to do
                        # some cleanup before actually shutting it down.
                        import sys
                        sys.exit(1)
                    #self.MSGTimer(4)
                    #self.master.after(50, self.periodicCall)
                    self.messageflag = False
                    self.master.after(4000, self.periodicCall)
                    #self.MSGTimer(4)
                    pass
            else:
                while self.running == 1:
                    if self.queuechk.qsize():
                        self.master.after(10, self.periodicCall)
                        break
        except:
            #self.master.after(200, self.periodicCall)
            logger.info("Periodic Exception")
            

    def looptimer_tick(self):
        self.machinestate = 0
        
    def restorationIDincrement(self):
        global restoreID
        restoreID += 1
        logger.info('restorationid=' + str(restoreID))
        return restoreID
    
    def interrupted(self):
        "called when read times out"
        qrcodereading = raw_input()
        logger.info('...' + qrcodereading)
        return
    """    
    signal.signal(signal.SIGALRM, interrupted)

    def inputBar(self):
        try:
            print 'You have 5 seconds to type in your stuff...'
            foo = raw_input()
            return foo
        except:
            print('exception: ')
            return
    """
    def workerThreadTicketButton(self):
        """This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise."""
        
        if restoreID == 0:
            rid = str(restoreID)
            logger.info('restorationID = 0')
        else:
            rid = str(self.restorationIDincrement())
        #rid = str(restoreID)
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            loopstate = self.loopinfo.readloopstate()
            paperendsensorstate = self.paperlevel.readpapersensorstate()
            print(paperendsensorstate)
            time.sleep(0.2)
            #self.ticket.ser.write(b'\x10\x04\x14')
            #rtprinterstatus = self.ticket.ser.read(32)
            #print("Real time printer status: {}".format(rtprinterstatus))
            if loopstate == 1 and paperendsensorstate == 0 or self.looptimer < self.looptimerset:
                logger.info('loop was activated')
                i = 1
                ticketbuttonstate = self.ticketbuttoninfo.readticketbuttonstate()
                if self.machinestate == 0:
                    self.machinestate = 1
                    #looptimer = threading.Timer(10.0, self.looptimer_tick)
                    #looptimer.start()
                #self.rfid.singlerfreading()
                if self.messageflag == False:
                    self.msg = 1
                #msg = 1
                #self.queue.put(msg)
                if ticketbuttonstate == 1:
                    resp, cont, head = self.httpreq.sendticketentrance(rid)
                    msg = resp
                    #contj = json.loads(cont.decode('utf-8'))
                    contj = json.loads(cont)
                    try:
                        ex = contj["exception"]
                        if ex == "ParkingZoneFullException":
                            self.msg = msg + 1
                            self.httpreq.receive_ticket_entrance(resp)
                        if ex == "VehicleAlreadyEnteredException":
                            self.msg = msg
                            self.httpreq.receive_ticket_entrance(resp)
                    except:
                        date_time = contj["entered_at"]
                        dt = parse(date_time)
                        contp = contj['vehicle']
                        contb = contj['ticket']
                        platet = contp['plate']
                        datet = str(dt.day) + '-' + str(dt.month) + '-' + str(dt.year)
                        timet = str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)
                        barct = contb['code']
                        self.ticket.printticket(barct, timet, datet, platet)
                        retrieveticket = self.ticket.getticket()
                        self.httpreq.receive_ticket_entrance(resp)
                        if retrieveticket:
                            rid = str(self.restorationIDincrement())
                        self.msg = msg
                    #self.queue.put(msg)
                # signal.alarm(TIMEOUT)
                #timeout = 1
                print('timer= ' + str(self.looptimer))
                self.looptimer =float(time.time() - self.timer)
                #t = threading.Timer(timeout,self.interrupted())
                #t.start()
                #t.cancel()
                # signal.alarm(0)
                # --Qrcode scanner in wait for development--
                """i, o, e = select.select([sys.stdin], [], [], timeout)
                if i:
                    qrcodereading = sys.stdin.readline().strip()
                    logger.info("qrcode: " + qrcodereading)
                else:
                    logger.info('no qrcode')"""
                    
                """
                try:
                    something = inputimeout(prompt='>>', timeout=0.2)
                except TimeoutOccurred:
                    something = 'something'
                print(something)
                print('qrcode: ' + something)
                """
                # time.sleep(2)
                # if len(qrcodereading) == 0:
                    # pass
                    #logger.info(str(qrcode))
            if paperendsensorstate == 1:
                self.msg = 3
                while i == 1:
                    r = httpreq.sendlogmessage('critical', 'Το χαρτί έχει τελειώσει')
                    i = 2
                if loopstate == 0:
                    self.messageflag = True
                elif loopstate == 1:
                    self.messageflag = False
            if loopstate == 0 and self.looptimer > self.looptimerset and  paperendsensorstate == 0:
                #print('hello')
                self.timer = time.time()
                if self.messageflag == True:
                    #print('hello')
                    self.msg = 2
                
                
                
    def workerThreadRFID(self):
        self.queue.put(1)
        self.queuechk.put(1)
        self.queueent.put(1)
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            #loopstate = self.loopinfo.readloopstate()
            #print(paperendsensorstate)
            #time.sleep(0.2)
            #if loopstate == 1 or self.looptimer < self.looptimerset:
            #logger.info('loop was activated')
            #self.machinestate = 1
            #looptimer = threading.Timer(10.0, self.looptimer_tick)
            #looptimer.start()
            if self.messageflag == False:
                msg_screen = 1
            #self.queue.put(msg)
            time.sleep(0.5)
            try:
                entries, result, uid = self.rfidblock.readBlockDataEntrance()
                if len(str(uid)) > 4:
                    buzzer = GeneralOutput()
                    logger.info(uid)
                    #result = self.rfidblock.readBlockData()
                    print(result)
                    if entries > 0 and result == 0:
                        entr = self.rfidblock.writeNewBlockDataEntrance(entries)
                        buzzer.setbuzzerpin(0.3)
                        print(entr)
                        if entr == None:
                            logger.info("Could not write card")
                            msg = 505
                        else:
                            msg = 201
                            #self.httpreq.receive_card_entrance(msg)
                    if entries == 0:
                        logger.info("No more entries on card")
                        msg = 404
                        #self.httpreq.receive_card_entrance(msg)
                    if result != 0:
                        logger.info("Vechicle already in")
                        msg = 503
                    if msg != 201:
                        entr = 1
                    self.httpreq.receive_card_entrance(msg,entr)
                    msg_screen = msg
                    #self.queue.put(msg)
            except:
                pass
            try:
                if self.msg != msg_screen:
                    self.msg = msg_screen
                    self.queue.put(msg_screen)
                    self.queuechk.put(msg_screen)
                    if msg == 201:
                        self.queueent.put(entr)
                    # print(self.queue.get(0))
                # print(msg_screen)
            except:
                print('no msg')
            #print('timer= ' + str(self.looptimer))
            #self.looptimer =float(time.time() - self.timer)
            """if loopstate == 0 and self.looptimer > self.looptimerset:
                #print('hello')
                self.timer = time.time()
                if self.messageflag == True:
                    #print('hello')
                    self.msg = 2
                    self.messageflag == False"""
            """if paperendsensorstate == 1:
                self.msg = 3
            if loopstate == 0 and self.looptimer > 8 and  paperendsensorstate == 0:
                if self.messageflag == True:
                    self.msg = 2"""
                
                
    
    def workerThreadQrCode(self):
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            loopstate = self.loopinfo.readloopstate()
            paperendsensorstate = self.paperlevel.readpapersensorstate()
            #print(paperendsensorstate)
            barcode = '0'
            time.sleep(0.2)
            if loopstate == 1 or self.looptimer < self.looptimerset:
                logger.info('loop was activated')
                self.machinestate = 1
                #looptimer = threading.Timer(10.0, self.looptimer_tick)
                #looptimer.start()
                #if self.messageflag == False:
                    #self.msg = 1
                    #self.queue.put(msg)
                time.sleep(0.5)
                try:
                    barcode = inputimeout(prompt='scan the barcode \n',timeout=3)
                except:
                    pass
                #print("The barcode : " + str(len(barcode)))
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
                    #self.queue.put(msg)
            """elif paperendsensorstate == 1:
                self.msg = 3
            elif loopstate == 0 and self.looptimer > 8 and  paperendsensorstate == 0:
                if self.messageflag == True:
                    self.msg = 2"""
                    
                    
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

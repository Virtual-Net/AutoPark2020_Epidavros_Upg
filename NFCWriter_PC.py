import logging
import json
from GeneralOutput import GeneralOutput
from pn532 import *
import pn532.pn532 as nfc
import time
from NFCHandler import *                     
from tkinter import *
import threading
import socket
from Logger_setup import logger

IP_PORT = 7000
HOSTNAME = ""

class ThreadedClient:
    """Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place."""

    rfidblock = NFCHandler()
    buzz = GeneralOutput()


    def __init__(self, master):
        """Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O)."""
        self.master = master
        self.machinestate = 0
        # Create the queue
        #self.queue = queue.Queue()

        # Set up the GUI part
        #self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThreadListener)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything

                    
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
            #relays = GeneralOutput()
            #loopstate = self.loopinfo.readloopstate()
            time.sleep(0.2)
            self.machinestate = 1
            #if self.messageflag == False:
                #msg = 1
            #self.queue.put(msg)
            time.sleep(0.5)
            logger.info("Calling blocking accept()...")
            conn, addr = serverSocket.accept()
            data = str(conn.recv(4096).decode())
            #print(data)
            #data = int(data)
            trcontj = json.loads(data)
            action = trcontj["action"]
            if action == "charge":
                transits = int(trcontj["transits"])
                print("transits: {}".format(transits))
                """data = data.replace("b","")
                data = data.replace("'","")
                data = int(data)
                print("received message: {}".format(data))"""
                try:
                    uid, tran = self.rfidblock.readWriteRF(transits)
                    response = json.dumps({ "rfid" : str(uid), "transits": int(tran) })
                    bresponse = str.encode(response)
                    #graphics_test.update()
                    print("Connected with client at {} and port {}".format(addr[0], addr[1]))
                    #self.buzz.setbuzzerpin(2)
                    conn.send(bresponse)
                except:
                    logger.info("Card reading problem")
                    pass
                    #socketHandler = SocketHandler(conn)
                    # necessary to terminate it at program termination:
                    #socketHandler.setDaemon(True)  
                    #socketHandler.run()
            if action == "balance":
                try:
                    uid, transits = self.rfidblock.readBalance()
                    response = json.dumps({ "rfid" : str(uid), "transits": int(transits) })
                    bresponse = str.encode(response)
                    #graphics_test.update()
                    print("Connected with client at {} and port {}".format(addr[0], addr[1]))
                    #self.buzz.setbuzzerpin(2)
                    print(bresponse)
                    conn.send(bresponse)
                except:
                    logger.info("Card reading problem")
                    conn.send(b"Card missing")
                    pass
            if action == "clear":
                try:
                    uid, transits = self.rfidblock.resetBalance()
                    response = json.dumps({ "rfid" : str(uid), "transits": int(transits) })
                    bresponse = str.encode(response)
                    #graphics_test.update()
                    print("Connected with client at {} and port {}".format(addr[0], addr[1]))
                    #self.buzz.setbuzzerpin(2)
                    conn.send(bresponse)
                except:
                    logger.info("Card reading problem")
                    pass

    def endApplication(self):
        self.running = 0


root = Tk()
root.withdraw()

client = ThreadedClient(root)
root.mainloop()



import logging
import json
from GeneralOutput import *
from pn532 import *
import pn532.pn532 as nfc
import time
from tkinter import *

class NFCHandler(object):
    buzz = GeneralOutput()
      
    def readWriteRF(self, entries):
        try:
            pn532 = PN532_UART(debug=False, reset=20)
            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()
            block_number = 30
            key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'

            print('Waiting for RFID/NFC card...')
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=1)
            pn532.mifare_classic_authenticate_block(uid, block_number=block_number,
                                                            key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
            bdata = pn532.mifare_classic_read_block(block_number)
            # print('.', end="")
            # Try again if a no card is available.
            data = bytes([bdata[0] + entries, bdata[1], 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
            if uid is None:
                return
            else:
                print('Found card with UID:', [hex(i) for i in uid])
                print(uid)
                uid_ = uid.hex()
                print(uid_)
                b_uid = str.encode(uid_)
                print(b_uid)
                try:
                    pn532.mifare_classic_authenticate_block(uid, block_number=block_number,
                                                            key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
                    pn532.mifare_classic_write_block(block_number, data)
                    if pn532.mifare_classic_read_block(block_number) == data:
                        print('write block {} successfully'.format(block_number))
                        print('Block has been writen successfully with data: {}'.format(data.hex()))
                        if data[0] < 3:
                              self.buzz.setbuzzerpin(1)
                        # print(bytes.fromhex(data.hex()).decode('utf-8'))
                except:
                    print("block was not read")
                    #self.buzz.setbuzzerpin(3)
                    b_uid = None
                    pass
                return uid_, data[0]
            # GPIO.cleanup()
        except:
            # block4 = pn532.mifare_classic_read_block()
            # print("Block4: {}".format(block4))
            pass
            
    def readBalance(self):
        try:
            pn532 = PN532_UART(debug=False, reset=20)
            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()
            block_number = 30
            key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'

            print('Waiting for RFID/NFC card...')
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=1)
            pn532.mifare_classic_authenticate_block(uid, block_number=block_number,
                                                            key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
            bdata = pn532.mifare_classic_read_block(block_number)
            # print('.', end="")
            # Try again if a no card is available.
            #data = bytes([bdata[0] + entries, 0, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
            if uid is None:
                print("Card not found")
                return None, None
            else:
                print('Found card with UID:', [hex(i) for i in uid])
                print(uid)
                uid_ = uid.hex()
                print(uid_)
                b_uid = str.encode(uid_)
                print(b_uid)
                """try:
                    pn532.mifare_classic_authenticate_block(uid, block_number=block_number,
                                                            key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
                    pn532.mifare_classic_write_block(block_number, data)
                    if pn532.mifare_classic_read_block(block_number) == data:
                        print('write block {} successfully'.format(block_number))
                        print('Block has been writen successfully with data: {}'.format(data.hex()))
                        self.buzz.setbuzzerpin(1)
                        # print(bytes.fromhex(data.hex()).decode('utf-8'))
                except:
                    print("block was not read")
                    self.buzz.setbuzzerpin(3)
                    pass"""
                
                return uid_, bdata[0]
            # GPIO.cleanup()
        except:
            uid_ = "None"
            bdata[0] = 0  
            return uid_, bdata[0]
            # block4 = pn532.mifare_classic_read_block()
            # print("Block4: {}".format(block4))
            pass

    def resetBalance(self):
        try:
            pn532 = PN532_UART(debug=False, reset=20)
            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()
            block_number = 30
            key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'

            print('Waiting for RFID/NFC card...')
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=1)
            pn532.mifare_classic_authenticate_block(uid, block_number=block_number,
                                                            key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
            bdata = pn532.mifare_classic_read_block(block_number)
            # print('.', end="")
            # Try again if a no card is available.
            data = bytes([0, 0, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
            if uid is None:
                return
            else:
                print('Found card with UID:', [hex(i) for i in uid])
                print(uid)
                uid_ = uid.hex()
                print(uid_)
                b_uid = str.encode(uid_)
                print(b_uid)
                try:
                    pn532.mifare_classic_authenticate_block(uid, block_number=block_number,
                                                            key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
                    pn532.mifare_classic_write_block(block_number, data)
                    if pn532.mifare_classic_read_block(block_number) == data:
                        print('write block {} successfully'.format(block_number))
                        print('Block has been writen successfully with data: {}'.format(data.hex()))
                        #self.buzz.setbuzzerpin(1)
                        # print(bytes.fromhex(data.hex()).decode('utf-8'))
                except:
                    print("block was not read")
                    #self.buzz.setbuzzerpin(3)
                    uid_ = None
                    data[0] = None
                    pass
                return uid_, data[0]
            # GPIO.cleanup()
        except:
            # block4 = pn532.mifare_classic_read_block()
            # print("Block4: {}".format(block4))
            pass

    def readBlockDataEntrance(self):
        try:
            pn532 = PN532_UART(debug=False, reset=20)
            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()

            print('Waiting for RFID/NFC card...')
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=1)
            block_number = 30
            key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'
            pn532.mifare_classic_authenticate_block(uid, block_number=block_number, key_number=nfc.MIFARE_CMD_AUTH_A,
                                                    key=key_a)
            data30 = pn532.mifare_classic_read_block(30)
            entries = data30[0]
            result = data30[1]
            # entries = int(entries)
            # entries = 99
            # if entries < 100:
            #   entries = '0{}'.format(entries)
            # print(hex(entries[:2]))
            print(entries)
            return entries, result, uid
        except:
            pass

    def writeNewBlockDataEntrance(self, entries):
        try:
            pn532 = PN532_UART(debug=False, reset=20)
            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()

            print('Waiting for RFID/NFC card...')
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=1)
            # print('.', end="")
            # Try again if a no card is available.
            block_number = 30
            key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'
            # print(bytes('0x{}'.format(entries[:2])))
            new_entries = entries - 1
            data = bytes(
                [new_entries, 1, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
            print(str(data))
            if uid is None:
                return
            else:
                print('Found card with UID:', [hex(i) for i in uid])
                print(uid)
                uid_ = uid.hex()
                print(uid_)
                try:
                    pn532.mifare_classic_authenticate_block(uid, block_number=block_number,
                                                            key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
                    pn532.mifare_classic_write_block(block_number, data)
                    if pn532.mifare_classic_read_block(block_number) == data:
                        print('write block {} successfully'.format(block_number))
                        print('Block has been writen successfully with data: {}'.format(data.hex()))
                        print(bytes.fromhex(data.hex()).decode('utf-8'))
                        return new_entries
                except:
                    print("block was not read")
                    pass
            # GPIO.cleanup()
        except:
            # block4 = pn532.mifare_classic_read_block()
            # print("Block4: {}".format(block4))
            pass

    def readBlockDataExit(self):
        try:
            pn532 = PN532_UART(debug=False, reset=20)
            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()

            print('Waiting for RFID/NFC card...')
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=1)
            block_number = 30
            key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'
            pn532.mifare_classic_authenticate_block(uid, block_number=block_number, key_number=nfc.MIFARE_CMD_AUTH_A,
                                                    key=key_a)
            data30 = pn532.mifare_classic_read_block(30)
            entries = data30[0]
            result = data30[1]
            # entries = int(entries)
            # entries = 99
            # if entries < 100:
            #   entries = '0{}'.format(entries)
            # print(hex(entries[:2]))
            print(entries)
            return entries, result, uid
        except:
            pass

    def writeNewBlockDataExit(self, entries):
        try:
            pn532 = PN532_UART(debug=False, reset=20)
            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()

            print('Waiting for RFID/NFC card...')
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=1)
            # print('.', end="")
            # Try again if a no card is available.
            block_number = 30
            key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'
            # print(bytes('0x{}'.format(entries[:2])))
            data = bytes([entries, 0, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
            #print(str(data))
            if uid is None:
                return
            else:
                print('Found card with UID:', [hex(i) for i in uid])
                print(uid)
                uid_ = uid.hex()
                print(uid_)
                try:
                    pn532.mifare_classic_authenticate_block(uid, block_number=block_number,
                                                            key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
                except:
                    logger.info("Block could not be authenticated")
                try:
                    pmcwb = pn532.mifare_classic_write_block(block_number, data)
                    logger.info(pmcwb)
                except:
                    logger.info("Block was not writen")
                try:
                    if pn532.mifare_classic_read_block(block_number) == data:
                        logger.info('write block {} successfully'.format(block_number))
                        logger.info('Block has been writen successfully with data: {}'.format(data.hex()))
                        logger.info(bytes.fromhex(data.hex()).decode('utf-8'))
                        logger.info(pn532.mifare_classic_read_block(block_number)[2])
                        return pn532.mifare_classic_read_block(block_number)[2]
                    else:
                        print("block was not writen")
                except:
                    logger.info("block was not writen")
                    pass
            # GPIO.cleanup()
        except:
            # block4 = pn532.mifare_classic_read_block()
            # print("Block4: {}".format(block4))
            pass

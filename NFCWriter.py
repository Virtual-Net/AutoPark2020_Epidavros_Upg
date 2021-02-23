import logging
import json
# from GeneralOutput import GeneralOutput
from pn532 import *
import pn532.pn532 as nfc
import time


def WriteRF(entries):
    # try:
    pn532 = PN532_UART(debug=False, reset=20)
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

    # Configure PN532 to communicate with MiFare cards
    pn532.SAM_configuration()

    print('Waiting for RFID/NFC card...')
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=3)
    # print('.', end="")
    # Try again if a no card is available.
    block_number = 30
    key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'
    data = bytes([entries, 0, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
    if uid is None:
        return
    else:
        print('Found card with UID:', [hex(i) for i in uid])
        print(uid)
        uid_ = uid.hex()
        print(uid_)
        try:
            pn532.mifare_classic_authenticate_block(uid, block_number=block_number, key_number=nfc.MIFARE_CMD_AUTH_A,
                                                    key=key_a)
            pn532.mifare_classic_write_block(block_number, data)
            if pn532.mifare_classic_read_block(block_number) == data:
                print('write block {} successfully'.format(block_number))
                print('Block has been writen successfully with data: {}'.format(data.hex()))
                # print(bytes.fromhex(data.hex()).decode('utf-8'))
        except:
            print("block was not read")
            pass
        return uid_
        # GPIO.cleanup()
    # except:
    # block4 = pn532.mifare_classic_read_block()
    # print("Block4: {}".format(block4))
    # pass


entries = input("Enter number of availiable entries")
entries = int(entries)
WriteRF(entries)

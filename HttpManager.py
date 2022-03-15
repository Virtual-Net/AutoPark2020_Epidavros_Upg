import requests
import json
from Logger_setup import logger
from GeneralOutput import *
from TicketDispenserAdel import *
from TicketDispenserDDM import *


class HttpManager:
    relays = GeneralOutput()
    #ticketdispenser = TicketDispenser()

    def __init__(self):
        with open('/home/pi/Autopark2020_optimization_epidavros/TerminalSettings.json') as json_file:
            self.data = json.load(json_file)

    '''http requests'''
    def retreivecurrentuserentrance(self):
        get_currentuser = self.data['get_current_user']
        api_token_entrance = self.data['api_token_entrance']
        server_ip = self.data['server_ip']
        request = 'http://' + server_ip + get_currentuser
        user_response = requests.get(request, headers={'Authorization': 'Bearer ' + api_token_entrance})
        logger.info(user_response)
        return user_response, user_response.content, user_response.headers

    def sendticketentrance(self, restorationid):
        ticket_entrance = self.data['ticket_entrance']
        api_token_entrance = self.data['api_token_entrance']
        server_ip = self.data['server_ip']
        request = 'http://' + server_ip + ticket_entrance + restorationid
        ticket_response = requests.get(request, headers={'Authorization': 'Bearer ' + api_token_entrance})
        logger.info(ticket_response)
        return ticket_response.status_code, ticket_response.text, ticket_response.headers

    def sendcardentrance(self, cardid):
        card_entrance = self.data['card_entrance']
        api_token_entrance = self.data['api_token_entrance']
        server_ip = self.data['server_ip']
        comm_protocol = "http://"
        request = comm_protocol + server_ip + card_entrance + cardid
        card_response = requests.get(request, headers={'Authorization': 'Bearer ' + api_token_entrance})
        logger.info(card_response.content)
        return card_response.status_code

    def sendbookedentrance(self, qrcode):
        booked_entrance = self.data['booked_entrance']
        api_token_entrance = self.data['api_token_entrance']
        server_ip = self.data['server_ip']
        comm_protocol = "http://"
        request = comm_protocol + server_ip + booked_entrance + qrcode
        print(request)
        booked_response = requests.get(request, headers={'Authorization': 'Bearer ' + api_token_entrance})
        print(booked_response.content)
        logger.info(booked_response)
        return booked_response, booked_response.content, booked_response.headers
        
        
    def sendticketexit(self, ticket_barcode):
        ticket_exit = self.data['ticket_exit']
        api_token_exit = self.data['api_token_exit']
        server_ip = self.data['server_ip']
        request = 'http://' + server_ip + ticket_exit + ticket_barcode
        ticket_response = requests.get(request, headers={'Authorization': 'Bearer ' + api_token_exit})
        logger.info(ticket_response)
        return ticket_response.status_code, ticket_response.content, ticket_response.headers

    def sendcardexit(self, cardid):
        card_exit = self.data['card_exit']
        api_token_exit = self.data['api_token_exit']
        server_ip = self.data['server_ip']
        comm_protocol = "http://"
        request = comm_protocol + server_ip + card_exit + cardid
        card_response = requests.get(request, headers={'Authorization': 'Bearer ' + api_token_exit})
        logger.info(card_response.content)
        return card_response.status_code
        
    def sendbookedexit(self, qrcode):
        booked_exit = self.data['booked_exit']
        api_token_exit = self.data['api_token_exit']
        server_ip = self.data['server_ip']
        comm_protocol = "http://"
        request = comm_protocol + server_ip + booked_exit + qrcode
        print('request: ' + request)
        booked_response = requests.get(request, headers={'Authorization': 'Bearer ' + api_token_exit})
        #print(booked_response.content)
        logger.info(booked_response)
        return booked_response.status_code, booked_response.content, booked_response.headers
        
    def testliveserver(self):
        test_live_server = self.data['test_live_server']
        server_ip = self.data['server_ip']
        request = 'http://' + server_ip + test_live_server
        test_live_server_response = requests.get(request)
        logger.info(test_live_server_response)
        return test_live_server_response, test_live_server_response.content, test_live_server_response.headers

    def retrievebusinessinfo(self):
        business_info = self.data['business_info']
        server_ip = self.data['server_ip']
        api_token = self.data['api_token_entrance']
        request = 'http://' + server_ip + business_info
        business_info_response = request.get(request, headers={'Authorization': 'Bearer ' + api_token})
        logger.info(business_info_response)
        return business_info_response, business_info_response.content, business_info_response.headers

    def sendpaperlow(self):
        paper_low = self.data['paper_low']
        server_ip = self.data['server_ip']
        api_token_entrance = self.data['api_token_entrance']
        request = 'http://' + server_ip + paper_low
        paper_low_response = requests.get(request, headers={'Authorization': 'Bearer ' + api_token_entrance})
        logger.info(paper_low_response)
        return paper_low_response, paper_low_response.content, paper_low_response.headers
        
    def sendlogmessage(self, message_level, message_text):
        log_message = self.data['log_message']
        server_ip = self.data['server_ip']
        api_token_entrance = self.data['api_token_entrance']
        request = 'http://' + server_ip + log_message
        log_message_response = requests.get(request, headers={'Authorization': 'Bearer ' + api_token_entrance})
        logger.info(log_message_response)
        return log_message_response, log_message.content, log_message.headers

    '''http responses'''

    @staticmethod
    def receive_card_entrance(result_,ent):
        buzzer = GeneralOutput()
        relays = GeneralOutput()
        if result_ == 503:
            buzzer.setbuzzerpin(1.5)
            logger.info('card service unavailable')
        elif result_ == 200:
            relays.setbarrierpin()
            relays.resetbarrierpin()
            buzzer.setbuzzerpin(0.5)
            time.sleep(0.2)
            buzzer.setbuzzerpin(0.5)
            logger.info('card entrance granted, 200')
        elif result_ == 201:
            relays.setbarrierpin()
            relays.resetbarrierpin()
            if ent > 2:
                buzzer.setbuzzerpin(0.5)
                #time.sleep(0.2)
                #buzzer.setbuzzerpin(0.5)
            else:
                buzzer.setbuzzerpin(1)
                time.sleep(0.2)
                buzzer.setbuzzerpin(1)
            logger.info('card entrance granted, 201')
        elif result_ == 404:
            buzzer.setbuzzerpin(1.5)
            logger.info('card not found')
        elif result_ == 500:
            buzzer.setbuzzerpin(1.5)
            logger.info('server down... send system busy')
        else:
            logger.info("Unknown response status code")
        

    @staticmethod
    def receive_card_exit(result_):
        buzzer = GeneralOutput()
        relays = GeneralOutput()
        if result_ == 503:
            buzzer.setbuzzerpin(1.5)
            logger.info('card service unavailable')
        elif result_ == 200:
            relays.setbarrierpin()
            relays.resetbarrierpin()
            buzzer.setbuzzerpin(0.5)
            time.sleep(0.2)
            buzzer.setbuzzerpin(0.5)
            logger.info('card entrance granted, 200')
        elif result_ == 201:
            relays.setbarrierpin()
            relays.resetbarrierpin()
            buzzer.setbuzzerpin(0.5)
            time.sleep(0.2)
            buzzer.setbuzzerpin(0.5)
            logger.info('card entrance granted, 201')
        elif result_ == 404:
            buzzer.setbuzzerpin(1.5)
            logger.info('card not found')
        elif result_ == 500:
            buzzer.setbuzzerpin(1.5)
            logger.info('server down... send system busy')
        else:
            logger.info("Unknown response status code")
            
    @staticmethod
    def receive_ticket_entrance(result_):
        buzzer = GeneralOutput()
        relays = GeneralOutput()
        if result_ == 503:
            buzzer.setbuzzerpin(1.5)
            logger.info('ticket service unavailable')
        elif result_ == 200:
            relays.setbarrierpin()
            relays.resetbarrierpin()
            buzzer.setbuzzerpin(0.5)
            time.sleep(0.2)
            buzzer.setbuzzerpin(0.5)
            logger.info('ticket entrance granted, 200')
        elif result_ == 201:
            relays.setbarrierpin()
            relays.resetbarrierpin()
            buzzer.setbuzzerpin(0.5)
            time.sleep(0.2)
            buzzer.setbuzzerpin(0.5)
            logger.info('ticket entrance granted, 201')
        elif result_ == 404:
            buzzer.setbuzzerpin(1.5)
            logger.info('ticket not found')
        elif result_ == 500:
            buzzer.setbuzzerpin(1.5)
            logger.info('server down... send system busy')
        else:
            logger.info("Unknown response status code")
            
    @staticmethod
    def receive_ticket_exit(result_):
        with open('/home/pi/Autopark2020_optimization/TerminalSettings.json') as json_file:
            data = json.load(json_file)
        dispensername = data['dispenser-type']
        ticketdispenser = globals()['TicketDispenser' + dispensername]()
        #print(type(ticketdispenser))
        buzzer = GeneralOutput()
        relays = GeneralOutput()
        if result_ == 503:
            ticketdispenser.returnticketcmd()
            buzzer.setbuzzerpin(1.5)
            logger.info('ticket service unavailable')
        elif result_ == 200:
            relays.setbarrierpin()
            relays.resetbarrierpin()
            buzzer.setbuzzerpin(0.5)
            time.sleep(0.2)
            buzzer.setbuzzerpin(0.5)
            ticketdispenser.captureticketcmd()
            logger.info('ticket exit granted, 200')
        elif result_ == 201:
            relays.setbarrierpin()
            relays.resetbarrierpin()
            buzzer.setbuzzerpin(0.5)
            time.sleep(0.2)
            buzzer.setbuzzerpin(0.5)
            ticketdispenser.captureticketcmd()
            logger.info('ticket exit granted, 201')
        elif result_ == 404:
            buzzer.setbuzzerpin(1.5)
            ticketdispenser.returnticketcmd()
            logger.info('ticket not found')
        elif result_ == 500:
            buzzer.setbuzzerpin(1.5)
            ticketdispenser.returnticketcmd()
            logger.info('server down... send system busy')
        else:
            logger.info("Unknown response status code")
        

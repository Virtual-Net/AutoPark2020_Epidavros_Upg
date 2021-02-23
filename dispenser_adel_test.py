from TicketDispenserAdel import *
from GeneralOutput import *

tda = TicketDispenserAdel()
buzzer = GeneralOutput()
"""TicketDispenserAdel().resetticketdispenser()
TicketDispenserAdel().readticketdispenserresponse()
time.sleep(2)
TicketDispenserAdel().ticketdispenserstatuscmd()
TicketDispenserAdel().readticketdispenserresponse()
time.sleep(2)
TicketDispenserAdel().returnticketcmd()
TicketDispenserAdel().readticketdispenserresponse()
time.sleep(2)"""
#tda.ticketdispenserstatuscmd()
#time.sleep(2)
#tda.intaketochipcmd()
#time.sleep(4)
#tda.readticketdispenserresponse()
#TicketDispenserAdel().resetticketdispenser()
#tda.intaketochipcmd()

while True:
	#t = TicketDispenserAdel().ser.in_waiting
	#print(t)
	tda.ticketdispenserstatuscmd()
	response = tda.readticketdispenserresponse()
	buzzer.setbuzzerpin(2)
	#if response is None:
		#TicketDispenserAdel().resetticketdispenser()
		#TicketDispenserAdel().resetticketdispenser()
	#TicketDispenserAdel().ticketdispenserstatuscmd()	#TicketDispenserAdel().ticketdispenserstatuscmd()

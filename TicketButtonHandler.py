import GeneralInput


class TicketButtonHandler:
    def __init__(self):
        print('Ticket Button handler init function')

    def readticketbuttonstate(self):
        if GeneralInput.readticketbuttonstate() == 1:
            print('Ticket button pressed')
            return True
        else:
            print('Wait to press button')
            return False

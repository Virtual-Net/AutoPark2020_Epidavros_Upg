import automationhat
from Logger_setup import logger

class GeneralInput():
    def __init__(self, *args, **kwargs):
        if automationhat.is_automation_hat():
            automationhat.light.power.write(1)

    def readloopstate(self):
        loop = automationhat.input.one.read()
        """if loop == 1:
            logger.info("loop activated")
        elif loop == 0:
            logger.info("loop off")"""
        return loop

    def readticketbuttonstate(self):
        ticketButton = automationhat.input.two.read()
        if ticketButton == 1:
            logger.info("button pressed")
        elif ticketButton == 0:
            logger.info("button not pressed")
        return ticketButton

    def readpapersensorstate(self):
        papersensor = automationhat.input.three.read()
        if papersensor == 0:
            logger.info("Paper level ok")
        elif papersensor == 1:
            logger.info("Paper end")
        return papersensor







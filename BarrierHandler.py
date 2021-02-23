import GeneralOutput


class BarrierHandler:
    def __init__(self, fname, lname):
        GeneralOutput.__init__(self, fname, lname)


    def openbarrierrelay(outputstate, time, on=None):
        openbarrier = GeneralOutput
        openbarrier.setbarrierpin(on)

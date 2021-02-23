from GeneralInput import GeneralInput


class PaperSensorHandler(GeneralInput):
    def __init__(self, fname, lname):
        GeneralInput.__init__(self, fname, lname)

    def __run__(self):
        if GeneralInput.readpapersensorstate() == 0:
            print('paper full')
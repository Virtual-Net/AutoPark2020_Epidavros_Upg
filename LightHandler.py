import GeneralOutput


class LightHandler(GeneralOutput):
    def __init__(self, fname, lname):
        GeneralOutput.__init__(self, fname, lname)

    def greenlighton(self):
        light = 0

    def redlighton(self):
        light = 1
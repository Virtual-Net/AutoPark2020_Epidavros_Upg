import GeneralInput


class LoopHandler(GeneralInput):
    def __init__(self, fname, lname):
        GeneralInput.__init__(self, fname, lname)

    def __run__(self):
        if GeneralInput.readloopstate(self) == 1:
            print('loop is activated')



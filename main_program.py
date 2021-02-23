import time
from EntranceTerminal import EntranceTerminal



if __name__ == "__main__":
    entranceTerminal = EntranceTerminal()
    entranceTerminal.boot()
    while True:
        print('main loop')
        entranceTerminal.waitforcustomer()
        time.sleep(0.5)


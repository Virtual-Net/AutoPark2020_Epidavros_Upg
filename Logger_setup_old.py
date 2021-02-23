from datetime import date
import logging
import os

def fname():
    today = date.today()
    return str(today)
log_dir = os.path.join(os.path.normpath(os.getcwd()), 'logs')

if not os.path.exists(log_dir):
    os.mkdir(log_dir)
else:
    pass

# log_fname = os.path.join(log_dir, str(today) + '.log')

logging.basicConfig(format='%(asctime)-8s %(levelname)s: %(message)s', filename=log_dir + r'/' + fname() + '.log',
                    level=logging.INFO, datefmt='%H:%M:%S')
logger = logging.getLogger('info')
"""
class Loggings:
    @staticmethod
    def Debug():
        logging.basicConfig(level=logging.DEBUG)
    @staticmethod
    def Info():

    @staticmethod
    def Warning():

    @staticmethod
    def Error():

    @staticmethod
    def Critical():
"""

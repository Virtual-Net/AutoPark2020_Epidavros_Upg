import logging
from logging.handlers import TimedRotatingFileHandler
import os


log_dir = os.path.join(os.path.normpath(os.getcwd()), 'logs')

if not os.path.exists(log_dir):
    os.mkdir(log_dir)
else:
    pass

logName = 'Terminal_Logger'
logger = logging.getLogger('testing')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)-8s %(levelname)s: %(message)s')
timeRotationHandler = TimedRotatingFileHandler(log_dir + r'/' + logName, backupCount=31, when='midnight', interval=1, )
timeRotationHandler.suffix = "%Y-%m-%d.log"
timeRotationHandler.setFormatter(formatter)
timeRotationHandler.setLevel(logging.INFO)
logger.addHandler(timeRotationHandler)

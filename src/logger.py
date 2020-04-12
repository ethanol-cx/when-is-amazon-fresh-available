from dotenv import load_dotenv
import logging
import os
from time import gmtime, strftime

# load env variables (including username and password for login)
load_dotenv()


def getLogger(logName):
    logging.basicConfig(filename='{}.{}'.format(str(os.getenv(
        'LOG_FILENAME')), strftime("%Y-%b-%d-%H%M%S", gmtime())),
        format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)
    return logging.getLogger(logName)

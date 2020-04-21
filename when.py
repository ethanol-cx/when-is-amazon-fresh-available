from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging
import os
import random
import requests
import sys
import time

# load env variables (including username and password for login)
load_dotenv()

from src.utils import initializeLogger
initializeLogger()

from src.login import login
from src.action import checkAvailability, checkout

logger = logging.getLogger(__name__)


def setBrandEnviron(argv):
    if len(argv) > 1:
        if argv[1] == '0':
            os.environ['WHOLEFOODS_OR_FRESH'] = 'wholefoods'
            os.environ['BRAND_ID'] = 'VUZHIFdob2xlIEZvb2Rz'
        elif argv[1] == '1':
            os.environ['WHOLEFOODS_OR_FRESH'] = 'fresh'
            os.environ['BRAND_ID'] = 'QW1hem9uIEZyZXNo'
        return True
    return False


def main(argv):
    if not setBrandEnviron(argv):
        print("Please append either '0' (for wholefoods) or '1' (for amazon fresh)")
    session = requests.Session()

    # login
    login(session, os.getenv('EMAIL'), os.getenv('PASSWORD'))

    i = 0
    MAX_NUM_OF_ITERATIONS = 10000
    while True:
        # check availability
        isAvailable = checkAvailability(session)
        if isAvailable:
            # checkout
            checkout(session)
            exit()
        i += 1
        if i % 50 == 0:
            logger.debug(
                'Checking for the {}th time'.format(i))
        if i == MAX_NUM_OF_ITERATIONS:
            logger.warn(
                'Maximum trial: {} achieved. Exiting...'.format(MAX_NUM_OF_ITERATIONS))
            exit(1)
        # sleep this thread while allowing others
        logger.debug('Could not find available spots. Sleeping...')
        time.sleep(random.randint(5, 30))


if __name__ == '__main__':
    main(sys.argv)

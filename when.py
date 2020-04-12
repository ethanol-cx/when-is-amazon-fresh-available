from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging
import os
import random
import requests
import time

from src.login import login
from src.action import checkAvailability, checkout
from src.logger import getLogger

# load env variables (including username and password for login)
load_dotenv()

logger = getLogger(__name__)

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
    time.sleep(random.randint(3, 6))

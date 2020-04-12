from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging
import os
import random
import requests
import time


from src.login import login
from src.action import checkAvailability, checkout


# load env variables (including username and password for login)
load_dotenv()

logging.basicConfig(filename=os.getenv(
    'LOG_FILENAME'), level=os.getenv('logLevel'), filemode='w')

session = requests.Session()

# login
login(session, os.getenv('EMAIL'), os.getenv('PASSWORD'))

i = 0
MAX_NUM_OF_ITERATIONS = 10000
while True:
    # check availability
    availableSpotsNum = checkAvailability(session)
    if availableSpotsNum > 0:
        # checkout
        checkout(session)
        exit()
    i += 1
    if i % 50 == 0:
        logging.debug(
            'Checking for the {}th time'.format(i))
    if i == MAX_NUM_OF_ITERATIONS:
        logging.debug(
            'Maximum trial: {} achieved. Exiting...'.format(MAX_NUM_OF_ITERATIONS))
    # sleep this thread while allowing others
    logging.debug('Could not find available spots. Sleeping...')
    time.sleep(random.randint(3, 6))

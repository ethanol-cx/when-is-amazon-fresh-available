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
    'LOG_FILENAME'), level=logging.DEBUG, filemode='w')

session = requests.Session()

# login
login(logging, session, os.getenv('EMAIL'), os.getenv('PASSWORD'))

while True:
    # check availability
    isAvailable = checkAvailability(session)
    if isAvailable > 0:
        # checkout
        checkout(session)
        exit()

    # sleep this thread while allowing others
    time.sleep(random.randint(3, 6))

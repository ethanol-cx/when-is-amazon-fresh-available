from dotenv import load_dotenv
import logging
import os
import random
import requests
import time


from src.login import login
from src.action import checkAvailability, checkout


def main():
    # load env variables (including username and password for login)
    load_dotenv()

    logging.basicConfig(filename=os.getenv(
        'LOG_FILENAME'), level=logging.DEBUG)

    session = requests.Session()

    # login
    response = login(session, os.getenv('EMAIL'), os.getenv('PASSWORD'))
    if response['Status'] == 302:
        time.sleep(300)
    elif response['Status'] == 200:
        logging.debug('Login Successful!')
    else:
        logging.error('Failed to login: {}'.format(response))
        return -1

    while True:
        # check availability
        isAvailable = checkAvailability(session)
        if isAvailable:
            # checkout
            checkout(session)
            return

        # sleep this thread while allowing others
        time.sleep(random.randint(3, 6))


if __name__ == '__main__':
    main()

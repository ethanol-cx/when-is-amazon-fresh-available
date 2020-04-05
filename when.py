from dotenv import load_dotenv
import os
import time
import random
import requests

from src.login import login


def main():
    # load env variables (including username and password for login)
    load_dotenv()

    while True:
        session = requests.Session()

        # TODO: log in

        # TODO: check availability
        available = True
        if available:
            # TODO: checkout
            return

        # sleep this thread while allowing others
        time.sleep(random.randint(3, 6))


if __name__ == '__main__':
    main()

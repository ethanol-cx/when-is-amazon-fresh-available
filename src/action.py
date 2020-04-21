from bs4 import BeautifulSoup
import logging
import os
import random
import requests
import sys
import time

from src.login import login
from src.utils import alarm

logger = logging.getLogger(__name__)


def checkoutCart(session):
    url = "https://www.amazon.com/alm/byg"

    querystring = {"sessionID": os.getenv('SESSION_ID'), "useDefaultCart": "1", "almBrandId": os.getenv('BRAND_ID'),
                   "ref_": "alm_cx_byg_proceed", "proceedToALMCheckout-VUZHIFdob2xlIEZvb2Rz": "Proceed+to+checkout", "proceedToCheckout": "1"}

    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9",
        'cookie': os.getenv('COOKIE'),
        'referer': "https://www.amazon.com/gp/cart/view.html?ref_=nav_cart",
        'sec-fetch-dest': "document",
        'sec-fetch-mode': "navigate",
        'sec-fetch-site': "same-origin",
        'sec-fetch-user': "?1",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        'Cache-Control': "no-cache",
    }

    response = session.get(url=url, headers=headers, params=querystring)

    time.sleep(10)
    return response


def checkSubstitution(session):
    url = "https://www.amazon.com/alm/substitution"

    querystring = {"almBrandId": os.getenv('BRAND_ID'),
                   "sessionID": os.getenv('SESSION_ID'), "ref_": "alm_cx_byg_proceed"}

    headers = {
        'method': "GET",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9",
        'cookie': os.getenv('COOKIE'),
        'referer': "https://www.amazon.com/alm/byg?sessionID={}&useDefaultCart=1&almBrandId={}&ref_=alm_cx_byg_proceed&proceedToALMCheckout-VUZHIFdob2xlIEZvb2Rz=Proceed+to+checkout&proceedToCheckout=1".format(os.getenv('SESSION_ID'), os.getenv('BRAND_ID')),
        'sec-fetch-dest': "document",
        'sec-fetch-mode': "navigate",
        'sec-fetch-site': "same-origin",
        'sec-fetch-user': "?1",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        'Cache-Control': "no-cache",
    }

    session.get(url=url, headers=headers, params=querystring)
    time.sleep(random.randint(2, 6))


def checkAvailability(session):
    # cookieString = session.cookies['cookieString']
    # session.cookies = session.cookies['cookies']
    # cookies = requests.utils.dict_from_cookiejar(session.cookies)

    url = "https://www.amazon.com/gp/cart/desktop/go-to-checkout.html/ref=alm_cx_byg_proceed"

    querystring = {"proceedToCheckout": "1", "ie": "UTF8", "isFresh": "1",
                   "useDefaultCart": "1", "brandId": os.getenv('BRAND_ID'), "sessionID": os.getenv('SESSION_ID')}

    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9",
        'cookie': os.getenv('COOKIE'),
        'sec-fetch-dest': "document",
        'sec-fetch-mode': "navigate",
        'sec-fetch-site': "same-origin",
        'sec-fetch-user': "?1",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        'Cache-Control': "no-cache",
    }

    time.sleep(random.randint(2, 6))
    response = session.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        logger.error('Failed to check availability: {}'.format(response.text))
        exit(-1)
    logger.debug('Finished checking availability')
    return parseAvailabilityPage(session, response.text)


def parseAvailabilityPage(session, page):
    # returning the number of available spots - a hidden input named 'groupCount' in the form
    soup = BeautifulSoup(page)
    titleDirLtr = soup.find('title', {'dir': 'ltr'})
    if titleDirLtr and titleDirLtr.string == 'Amazon Sign-In':
        logger.info(
            'Need to re-Log into the account. Please login manually. Sleeping for 120s')
        logger.debug(page)
        # repeat 'SystemHand' for that 10 times.
        # 'SystemHand' is a type of sound in windows.
        # It will be ignored within `alarm()` if it is not on windows.
        alarm(10, 'SystemHand')
        time.sleep(random.randint(2, 10))
        login(session, os.getenv('EMAIL'), os.getenv('PASSWORD'))
    if str(os.getenv('WHOLEFOODS_OR_FRESH')) == 'wholefoods':
        days = soup.find_all(
            'div', {'class': 'ufss-date-select-toggle-text-availability'})
        if days and (days[0].string.strip() != 'Not available' or days[1].string.strip() != 'Not available'):
            print('Go get the SPOT!')
            logger.debug('Found new availability at Wholefoods')
            logger.debug(str(page).encode('gbk', 'ignore'))
            return True
        return False
    else:
        groupCount = soup.find('input', {'name': 'groupCount'})
        if not groupCount:
            print('Go get the SPOT!')
            logger.debug('Found new availability at Amazon Fresh')
            logger.debug(page)
            return True
        elif groupCount.attrs['value'] == '0':
            return False
        # TODO: Add condition / Change
        logger.info('Found a new page. Maybe it is the available page.')
        # logging the page for future development
        logger.debug(str(page).encode('gbk', 'ignore'))
        return True


def checkout(session):
    # currently just alarming instead of checking out the system
    # TODO: checkout the cart
    alarm()
    return

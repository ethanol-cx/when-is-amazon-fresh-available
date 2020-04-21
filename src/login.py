from bs4 import BeautifulSoup
import json
import logging
import os
import time
import requests

from src.utils import alarm

logger = logging.getLogger(__name__)


def login(session, email, password):
    url = "https://www.amazon.com/ap/signin"

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"appActionToken\"\r\n\r\nOLFb6Ke0gSAHkb06Lqj2BLWvdE3JAj3D\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"appAction\"\r\n\r\nSIGNIN_PWD_COLLECT\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"subPageType\"\r\n\r\nSignInClaimCollect\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"openid.return_to\"\r\n\r\nape:aHR0cHM6Ly93d3cuYW1hem9uLmNvbS9ncC95b3Vyc3RvcmUvaG9tZT9pZT1VVEY4JmFjdGlvbj1zaWduLW91dCZwYXRoPSUyRmdwJTJGeW91cnN0b3JlJTJGaG9tZSZyZWZfPW5hdl95b3VyYWNjb3VudF9zaWdub3V0JnNpZ25Jbj0xJnVzZVJlZGlyZWN0T25TdWNjZXNzPTE=\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"prevRID\"\r\n\r\nape:RFA2UzlQSDRSRkg2NjhHNEVNRlg=\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"workflowState\"\r\n\r\neyJ6aXAiOiJERUYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.wm3FJJAuWyynsBjPPJLRiM_r2yavzpocxcZXYtOsJRKx3I0oaTD-lQ.SrUS_DN3aPY5gXJR.nQK_8NECgsv-p-3dY0JaRUZp7LiFrIuNKD_9TmaVz3unHg3-JQx5wvoGt2mHvPprdY5Mi84EfAXJUxEcovCiN8lC5nRHXlxZtAcWaBbT-BY003x-bKE6HmcxF8-wyvpiVkFnC1l7V3O9mOX1y6ZQbfH5TQx0CQQiDpzqfWOEmEYzCyR0CeIdtgkmjb993P9JmHx3eRjHDTK_GTRJ2DnyCuG6tWW19av8R6Kkdoi3DMbf4VfVQcUM-xACuNN_ckDSj73QarP8fTPWiQd8qqzt5BOFqkAi8W_cWMYk15JthIHjkRYtsVfVW28Me5BuHdmDF0yUrOYHGJQOyA.JWs0BJaBIC9Bd-4X-1vnaw\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"create\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(
        str(email), str(password))

    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9",
        'Cache-Control': "no-cache",
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cookie': os.getenv('COOKIE'),
        'origin': "https://www.amazon.com",
        'referer': "https://www.amazon.com/ap/signin",
        'sec-fetch-dest': "document",
        'sec-fetch-mode': "navigate",
        'sec-fetch-site': "same-origin",
        'sec-fetch-user': "?1",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }

    response = session.post(url, data=payload, headers=headers)
    logger.debug('Response after LogIn')
    logger.debug(response.text)

    # appending the cookieString from the header
    # session.cookies = {'cookies': session.cookies,
    #                    'cookieString': response.headers['set-cookie']}

    if response.status_code == 302:
        logger.warn('Login status code 302')
        return True
    elif response.status_code == 200:
        logger.info('Login Successful!')
        return True
    logger.error('Failed to login: {}'.format(response.text))
    return False

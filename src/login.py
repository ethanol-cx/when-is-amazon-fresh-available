import json
import logging
import os
import time
import requests

from .logger import getLogger

logger = getLogger(__name__)


def login(session, email, password):
    url = "https://www.amazon.com/ap/signin"

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"appActionToken\"\r\n\r\nOLFb6Ke0gSAHkb06Lqj2BLWvdE3JAj3D\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"appAction\"\r\n\r\nSIGNIN_PWD_COLLECT\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"subPageType\"\r\n\r\nSignInClaimCollect\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"openid.return_to\"\r\n\r\nape:aHR0cHM6Ly93d3cuYW1hem9uLmNvbS9ncC95b3Vyc3RvcmUvaG9tZT9pZT1VVEY4JmFjdGlvbj1zaWduLW91dCZwYXRoPSUyRmdwJTJGeW91cnN0b3JlJTJGaG9tZSZyZWZfPW5hdl95b3VyYWNjb3VudF9zaWdub3V0JnNpZ25Jbj0xJnVzZVJlZGlyZWN0T25TdWNjZXNzPTE=\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"prevRID\"\r\n\r\nape:RFA2UzlQSDRSRkg2NjhHNEVNRlg=\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"workflowState\"\r\n\r\neyJ6aXAiOiJERUYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.wm3FJJAuWyynsBjPPJLRiM_r2yavzpocxcZXYtOsJRKx3I0oaTD-lQ.SrUS_DN3aPY5gXJR.nQK_8NECgsv-p-3dY0JaRUZp7LiFrIuNKD_9TmaVz3unHg3-JQx5wvoGt2mHvPprdY5Mi84EfAXJUxEcovCiN8lC5nRHXlxZtAcWaBbT-BY003x-bKE6HmcxF8-wyvpiVkFnC1l7V3O9mOX1y6ZQbfH5TQx0CQQiDpzqfWOEmEYzCyR0CeIdtgkmjb993P9JmHx3eRjHDTK_GTRJ2DnyCuG6tWW19av8R6Kkdoi3DMbf4VfVQcUM-xACuNN_ckDSj73QarP8fTPWiQd8qqzt5BOFqkAi8W_cWMYk15JthIHjkRYtsVfVW28Me5BuHdmDF0yUrOYHGJQOyA.JWs0BJaBIC9Bd-4X-1vnaw\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\{0}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{1}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"create\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(
        email, password)
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9",
        'Cache-Control': "no-cache",
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cookie': "skin=noskin; session-id=132-5064857-6167532; ubid-main=131-5796902-1882944; sid=\"Cdf8u0UJob2eti9zcUn89A==|9//J0SYXXu0LArTk4IDq7VPeW0maHaec4DQPfe6XV3c=\"; s_cc=true; s_vnum=2018049351129%26vn%3D1; s_sq=%5B%5BB%5D%5D; s_ppv=35; s_nr=1586049359289-New; s_dslv=1586049359293; sst-main=Sst1|PQG4EsIEBUh-u8ePSvEFHbjtCxaVdfbuT7yiHUNiC_j359LgZRR1NwmtHo86_jdzlYta_KEWR1QZyjnpGylxmsZn1mT_3lWqvKKLuDH4Oth9bXIBZ3JA5e_xz49mYcsKEGzSFdqipFVqUgDU41c0rDfwIwoU4nfZHtfb5VTzqlX-RcoT1pmBFdxiMyxV7DaLCwNtAEhbxW9PrZuslKR_Gggk8zMHT3cpgwzGgs2zYnAVmrGNDNU_cAxWh_c9cDEP4J9UpnwIuSHOVee5NYsc1sg3T8w8q0vYLdp8e99q2dyl799vrLz8Y6tPJQmj8alKrBBqkgdC7gp8KEipWC6JHEyfJA; i18n-prefs=USD; x-wl-uid=1wN0jxI4tshCpP0GQ7QYBWPuxWGQKYWJd8o/RfOZFslwNXWHnKmG7wzQzuZH5c1r+kM65Hwx62g1cPhTTe9+CARuzeJYetmFrLnxnC4YGe8+WVP2haHobaKwdvn7Hhc85EyhFI/bNiIk=; cdn-session=AK-a824df9160a500a4e4d9fd877fb73564; session-token=w7SvJii7+iY+385t+iE5fmftHT0zGD5PEciHUlsJVduqS7fvnPFSB0KbuBfgZKvpubMlS9fAyYU+f1eeT/UI0o7IUMG4NK+iXQ3n/vlM++B3ULp+FAh73VGhfK6oTA3E19yaBKjkf4VfFFEv0Y3rseaxspkX0zrEVfyNS/kT+q4cR3KZe8BPPoFKZFH1H+5ZtWM6jG4FBuGd7ffZJT/3YA6j+jmakLU3q4IcnEb6jBLNpj1YjISvV864Ey20kCcq; session-id-time=2216849787l; csm-hit=tb:S4B4AM35ZDDHBFMEAGQG+s-DP6S9PH4RFH668G4EMFX|1586129788430&t:1586129788430&adb:adblk_yes",
        'origin': "https://www.amazon.com",
        'referer': "https://www.amazon.com/ap/signin",
        'sec-fetch-dest': "document",
        'sec-fetch-mode': "navigate",
        'sec-fetch-site': "same-origin",
        'sec-fetch-user': "?1",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        'Postman-Token': "2f686240-2358-42a4-8d4b-f5404a48f1fc"
    }

    response = session.post(url, data=payload, headers=headers)

    # appending the cookieString from the header
    # session.cookies = {'cookies': session.cookies,
    #                    'cookieString': response.headers['set-cookie']}

    if response.status_code == 302:
        logging.warn('Login status code 302')
        time.sleep(300)
    elif response.status_code == 200:
        logging.info('Login Successful!')
        return True
    logging.error('Failed to login: {}'.format(response.text))
    return False

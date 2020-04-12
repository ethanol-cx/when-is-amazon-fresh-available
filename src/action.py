from bs4 import BeautifulSoup
import logging
import os
import requests
import sys

logging.basicConfig(filename=os.getenv(
    'LOG_FILENAME'), level=os.getenv('LOG_LEVEL'))


def checkAvailability(session):
    # cookieString = session.cookies['cookieString']
    # session.cookies = session.cookies['cookies']
    # cookies = requests.utils.dict_from_cookiejar(session.cookies)

    url = "https://www.amazon.com/gp/cart/desktop/go-to-checkout.html/ref=alm_cx_byg_proceed"

    querystring = {"proceedToCheckout": "1", "ie": "UTF8", "isFresh": "1",
                   "useDefaultCart": "1", "brandId": "QW1hem9uIEZyZXNo", "sessionID": "132-5064857-6167532"}

    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9",
        'cookie': "skin=noskin; session-id=132-5064857-6167532; ubid-main=131-5796902-1882944; sid=\"Cdf8u0UJob2eti9zcUn89A==|9//J0SYXXu0LArTk4IDq7VPeW0maHaec4DQPfe6XV3c=\"; s_cc=true; s_vnum=2018049351129%26vn%3D1; s_sq=%5B%5BB%5D%5D; s_ppv=35; s_nr=1586049359289-New; s_dslv=1586049359293; x-wl-uid=1wN0jxI4tshCpP0GQ7QYBWPuxWGQKYWJd8o/RfOZFslwNXWHnKmG7wzQzuZH5c1r+kM65Hwx62g1cPhTTe9+CARuzeJYetmFrLnxnC4YGe8+WVP2haHobaKwdvn7Hhc85EyhFI/bNiIk=; cdn-session=AK-a824df9160a500a4e4d9fd877fb73564; lc-main=en_US; session-token=\"sGGmgZqFHsXgh7P57UZLvN3mNvUQDMGs6eahFKmuVV30Tx146HdQVBWdXyCU5spk26B4Jiu7HZXw+a2KvzBwf51Y0Guec/kEWkjdy5fgham5Xq28AGjgHW7Ta/t8mDOjKGYoBxhWW3tYnDws/mYHarRC2c8LTT4izFtbv6VrcDkXzVhicsYm22gUNYa3Zj0IaNvb4dVDr/GRqeZ9MhWJF7zXZBTygJtCbUyLOWa905o=\"; x-main=\"cbQTizZWDX?5ETSG7C0uozBdDXHgGv5AGkoBb0oQoE?rQ1Wj3ldp@NUyr3MA9qMy\"; at-main=Atza|IwEBIHPnriwHjAL3Qek0jMTD8FeUITJumxL6-zgM0ipDHkeW2jpv4Cn71SkXFTqFtT4p_pj6iVClggllfS1rDuS0q08lru-MqUgEvVoscQK91pkc-a3cSy8BA8QggwEvEUM288BOwEB6mRJtVeyw5s3kcm9f50bCLjYUtrCIY839UlqCfzckeYlCHDPOHHQEw6lBWi-xePEUkODWSLQXeZb7440Alv_g8g17SsPgnyLuWcZN0uRsRG0rsADISmeDxKe2nvtSD0_fXUMUNh51FBIVrlOkLgiVb6kdyMxiaqGrxD6ofmGDBgBriCnRDo8zsQbLWxvy7SfHSVrNIvrgvKkpVUrvJXm8i7WEg-jI3Q6oy-yCijMo5PqHzYCuFTKcIwo_IRN7xL-OdoGcAXr2R_x8-ocA; sess-at-main=\"VaApr61zHQceOaLtTajYC6+JKFPiKpY1kjvDbxmKviA=\"; sst-main=Sst1|PQGvDH-IfY2TBKznf5Hbdrm6CxE6NlBceorbOro1E0SbMQeVOKoEiWItTLKw0_h_wMO9UnnjPgdx15r_uB54cGwhpruLa-DzcjEENOWXrwR2ved5oaR2NBYa57MzQbjlN6AFJrffwK-LasObVjo5NN9Qqlhsd8SWg4ZBGkfG-MewumgEaqeCVNHDWEFZXZvzdWi-ZYTATB3MZGCr-5YnylivpVpZSReNnVGKqNe-K7-ulNhUefBgeGwcDchE4JtoByah6Z6RMNgTWRBSKcty7HJDRHZAiz7HpTbh8xzmyahq6HfpMLzKXSYkvVu7aXLgCp6znMv4_n2OMau_wR4VQWeyMA; session-id-time=2082787201l; i18n-prefs=USD; csm-hit=tb:8FPJ726SCR0BX6SMCGAK+s-3JT8W5YM64B2HXBD5G26|1586149086084&t:1586149086084&adb:adblk_yes",
        'referer': "https://www.amazon.com/alm/byg?sessionID=132-5064857-6167532&useDefaultCart=1&brandId=QW1hem9uIEZyZXNo&ref_=alm_cx_byg_proceed&proceedToALMCheckout-QW1hem9uIEZyZXNo=Proceed+to+checkout&proceedToCheckout=1",
        'sec-fetch-dest': "document",
        'sec-fetch-mode': "navigate",
        'sec-fetch-site': "same-origin",
        'sec-fetch-user': "?1",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        'Cache-Control': "no-cache",
        'Postman-Token': "0910fb97-d81b-4d72-ae09-6a3144b763e6"
    }

    response = session.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logging.error('Failed to check availability: {}'.format(response.text))
        return False
    logging.debug('Finished checking availability')
    return parseAvailabilityPage(response.text)


def parseAvailabilityPage(page):
    # returning the number of available spots - a hidden input named 'groupCount' in the form
    return int(BeautifulSoup(page).find('input', {'name': 'groupCount'}).get('value'))


def checkout(session):
    # currently just alarming instead of checking out the system
    alarm()
    return


def alarm():
    if sys.platform == 'win32':
        import winsound
        while True:
            winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    else:
        # has to have previous setup in the os
        # On Debian / Ubuntu / Linux Mint, run this in your terminal: `sudo apt install sox`
        # On Mac, run this in your terminal (using macports): `sudo port install sox`
        duration = 60  # seconds
        freq = 440  # Hz
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    return

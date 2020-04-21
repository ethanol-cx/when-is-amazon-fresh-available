from dotenv import load_dotenv
import logging
import os
from time import gmtime, strftime
import sys
from pathlib import Path


def initializeLogger():
    # create the log directory
    os.makedirs(os.path.abspath(str(os.getenv('LOG_FILENAME'))), exist_ok=True)

    # create a file handler
    filehandler = logging.FileHandler(filename='{}.{}'.format(str(os.getenv(
        'LOG_FILENAME')), strftime("%Y-%b-%d-%H%M%S", gmtime())), encoding='utf-8')
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)

    # set the root logger
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().addHandler(filehandler)


def alarm(itNum=400, type='SystemQuestion'):
    if sys.platform == 'win32':
        import winsound
        for _ in range(itNum):
            # `Playsound` itself does have a short break in between sounds
            winsound.PlaySound(type, winsound.SND_ALIAS)
    else:
        # has to have previous setup in the os
        # On Debian / Ubuntu / Linux Mint, run this in your terminal: `sudo apt install sox`
        # On Mac, run this in your terminal (using macports): `sudo port install sox`
        duration = 60  # seconds
        freq = 440  # Hz
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    return

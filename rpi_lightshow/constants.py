"""Contains constants used in the program."""

import pyaudio


# Program info
NAME = 'rpi-led-lightshow'
VERSION = '0.0.1'
DESCRIPTION = 'Perform a sexy light show with your Raspberry Pi and some LEDs!'

# Audio stream settings (see
# https://people.csail.mit.edu/hubert/pyaudio/docs/ for more details on
# any of these)
FRAMES_PER_BUFFER = 1024    # number of audio frames per buffer
FORMAT = pyaudio.paInt16    # sampling size and format
CHANNELS = 1                # number of audio channels
RATE = 44100                # sampling rate in Hz

# This is a list of frequency ranges of interest, based
# mostly on intuition and testing, and also information online. Tweaking
# these may lead to better results.
FREQUENCY_BINS = [(60, 150),    # bass (consider going further than 150)
                  (250, 500),   # low midrange
                  (500, 2e3),   # midrange
                  (2e3, 4e3),   # upper midrange
                  (4e3, 6e3),   # "presence"
                  (6e3, 20e3),  # "brilliance"
                 ]

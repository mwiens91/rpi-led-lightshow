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

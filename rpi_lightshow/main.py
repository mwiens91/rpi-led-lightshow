"""Main program for the light show."""

import pyaudio
import RPi.GPIO as GPIO
from rpi_lightshow.constants import (FRAMES_PER_BUFFER,
                                     FORMAT,
                                     CHANNELS,
                                     RATE,
                                     GPIO_PINS)

def pyaudio_stream_callback(raw_audio_string, *_):
    """Callback function for PyAudio stream."""
    pass

def main():
    """The main function for the light show."""
    # Start PyAudio
    this_pyaudio = pyaudio.PyAudio()

    # Use the RPi's audio output
    audio_stream = this_pyaudio.open(format=FORMAT,
                                     channels=CHANNELS,
                                     rate=RATE,
                                     frames_per_buffer=FRAMES_PER_BUFFER,
                                     stream_callback=pyaudio_stream_callback,
                                     input=True,
                                     output=False)

    # Set up the GPIO pins
    GPIO.setmode(GPIO.BOARD)    # refer to pin numbers on RPi board
    pwms = []

    for pin_number in GPIO_PINS:
        # Activate the pin
        GPIO.setup(pin_number, GPIO.OUT)

        # Start Pulse Width Modulation
        pwm = GPIO.PWM(pin_number, 100)   # 2nd arg is frequency
        pwm.start(0)

        # Add to list of pwms
        pwms.append(pwm)

    # Now we're in normal running operation. Exit when user tells us to.
    input("\n" + "-" * 5 + " hit enter anytime to exit " + "-" * 5 + "\n")

    # Turn off audio stream
    audio_stream.stop_stream()
    audio_stream.close()
    this_pyaudio.terminate()

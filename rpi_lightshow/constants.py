"""Contains constants used in the program."""

# Audio stream settings

# This should be a power of 2, and is the best number to tweak in terms
# of performance, as increasing/decreasing this value by a factor of two
# will half/double the number of times a Fast Fourier Transform is
# computed (expensive!).
FRAMES_PER_BUFFER = 2048  # number of audio frames per buffer

# Choose between the following:
# - int8
# - int16
# - int32
# - float32
# - uint8
FORMAT = "int16"  # sampling size and format

# Do NOT change this. Dealing with 2 channels is non-trivial. See
# https://stackoverflow.com/questions/22636499/convert-multi-channel-pyaudio-into-numpy-array
# to understand why.
CHANNELS = 1  # number of audio channels

# You should be able to change this to whatever you want, but this
# hasn't been tested at all. I don't see why you'd want to change this
# though (hence, why other values haven't been tested).
RATE = 44100  # sampling rate in Hz


# This is a list of frequency ranges of interest. There must be exactly
# 5 frequency bins, and their upper limit must never exceed the Nyquist
# frequency, which is around half of the sampling rate. So, for a
# sampling rate of 44.1KHz, the upper limits of the frequency ranges
# must be less than around 22KHz).
#
# The frequency ranges (or bins) work as follows: it will recombine the
# frequency bins computed by a Fast Fourier Transform (FFT) such that
# all of the bins it combines are greater than the lowest frequency and
# lower than the highest frequency. Thus, selecting too narrow a width
# can lead to not combining any of the FFTs bins, causing the program to
# crash. The size of the frequency bins computed by the FFT depend
# inversely with the number of audio frames per buffer, so the lower
# your frames per buffer the wider your widths must be.
FREQUENCY_BINS = (
    (45, 85),  # dat beat
    (120, 160),  # dat snare
    (252, 500),  # dat low voice
    (400, 800),  # dat melody
    (600, 1.5e3),  # more of dat melody
)


# The thresholds for an LEDs PWM duty cycle below which the LED will not
# light up. Note that the thresholds take effect *prior* to duty cycle
# averaging.
LED_DUTY_CYCLE_THRESHOLDS = (27, 4, 0, 0, 0)


# Raspberry Pi GPIO pins to use. The index of each pin is consistent
# with the index of the frequency bins and LED duty cycle thresholds
# above.
GPIO_PINS = (12, 18, 22, 36, 38)

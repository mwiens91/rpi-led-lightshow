"""Main program for the light show."""

import numpy as np
import pyaudio
import RPi.GPIO as GPIO
from rpi_lightshow.audio_analysis import fill_frequency_bins
from rpi_lightshow.constants import (FRAMES_PER_BUFFER,
                                     FORMAT,
                                     CHANNELS,
                                     RATE,
                                     FREQUENCY_BINS,
                                     LED_DUTY_CYCLE_THRESHOLDS,
                                     GPIO_PINS)
from rpi_lightshow.helpers import get_library_number_format
from rpi_lightshow.runtime_settings import parse_runtime_args


def pyaudio_stream_callback_closure(pulse_width_modulators,
                                    show_duty_cycles):
    """Provides a closure for audio stream callback function.

    Specifically, this returns a callback function aware of the passed
    in PWMs, and also of the maximum frequencies seen so far. It also
    let's the callback function keep track of its previous duty cycle.

    Args:
        pulse_width_modulators: A list of RPi.GPIO.PWMs corresponding to
            the connected LEDs.
        show_duty_cycles: A boolean specifying whether to print the duty
            cycles to the terminal.

    Returns:
        The callback function for PyAudio.
    """
    # The maximum frequency bin levels seen so far
    max_freq_levels = [1 for i in range(len(FREQUENCY_BINS))]

    # The previous duty cycles
    last_duty_cycles = [0 for i in range(len(GPIO_PINS))]


    # The callback function
    def pyaudio_stream_callback(raw_audio_string, *_):
        """Callback function for PyAudio stream.

        Takes in a string encoding audio for each buffer, and lights up LEDs
        according to the audio buffer.

        Arg:
            raw_audio_string: A bytes string encoding an audio buffer using
                the format specified in FORMAT.
        Returns:
            The exact raw_audio_string passed into the function, and a
            signal to tell PyAudio to keep running.
        """
        nonlocal last_duty_cycles, max_freq_levels

        # Put the audio data into an array
        data_array = np.fromstring(raw_audio_string,
                                   get_library_number_format(FORMAT, 'numpy'))

        # Fill the frequency bins
        levels = fill_frequency_bins(data_array)

        # Update maximum value for each frequency bin
        for bin_idx, bin_pair in enumerate(zip(max_freq_levels, levels)):
            # Check for new maximum
            if bin_pair[1] > bin_pair[0]:
                max_freq_levels[bin_idx] = bin_pair[1]

        # Scale the frequency levels by their maximum to determine duty
        # cycles
        duty_cycles = [level / max_freq_level * 100
                    for level, max_freq_level in zip(levels, max_freq_levels)]

        # Kill any duty cycle that doesn't meet the required theshold
        for dc_idx, dc_pair in enumerate(zip(duty_cycles,
                                             LED_DUTY_CYCLE_THRESHOLDS)):
            if dc_pair[0] < dc_pair[1]:
                # Don't light the LED at all
                duty_cycles[dc_idx] = 0

        # Average the duty cycles we have so far with the previous duty
        # cycles
        avg_duty_cycles = [(prev + new) / 2
                           for prev, new in zip(last_duty_cycles, duty_cycles)]

        # Store the current duty cycles for next round
        last_duty_cycles = duty_cycles

        # Pulse each corresponding LED with its frequency bin level
        for pwm, duty_cycle in zip(pulse_width_modulators, avg_duty_cycles):
            pwm.ChangeDutyCycle(duty_cycle)

        # Print the duty cycles for testing purposes
        if show_duty_cycles:
            for dc in avg_duty_cycles:
                # Zero-pad the printing
                if dc >= 50:
                    # Display high values in bold red
                    print("\033[91m\033[1m%03d\033[0m" % dc, end=' ')
                else:
                    print("%03d" % dc, end=' ')
            print()

        # Tell PyAudio to keep going
        return(raw_audio_string, pyaudio.paContinue)

    # Return the callback function
    return pyaudio_stream_callback


def main():
    """The main function for the light show."""
    # Get runtime arguments
    runtimeargs = parse_runtime_args()

    # Start PyAudio
    this_pyaudio = pyaudio.PyAudio()

    # Set up the GPIO pins
    GPIO.setmode(GPIO.BOARD)    # refer to pin numbers on RPi board
    pwms = []

    for pin_number in GPIO_PINS:
        # Activate the pin
        GPIO.setup(pin_number, GPIO.OUT)

        # Start Pulse Width Modulation
        pwm = GPIO.PWM(pin_number, 100)   # 2nd arg is frequency
        pwm.start(0)

        # Add to list of PWMs
        pwms.append(pwm)

    # Use the RPi's audio output
    audio_stream = this_pyaudio.open(
                    format=get_library_number_format(
                                FORMAT,
                                'portaudio'),
                    channels=CHANNELS,
                    rate=RATE,
                    frames_per_buffer=FRAMES_PER_BUFFER,
                    stream_callback=pyaudio_stream_callback_closure(
                                pwms,
                                runtimeargs.show_duty_cycles),
                    input=True,
                    output=False)

    # Now we're in normal running operation. Exit when user tells us to.
    input("\n" + "-" * 5 + " hit enter anytime to exit " + "-" * 5 + "\n")

    # Clean up GPIO pins
    for pwm in pwms:
        pwm.stop()
    GPIO.cleanup()

    # Turn off audio stream
    audio_stream.stop_stream()
    audio_stream.close()
    this_pyaudio.terminate()

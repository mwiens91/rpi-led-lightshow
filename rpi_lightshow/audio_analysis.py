"""Contains functions to analyze audio."""

import audioop
import numpy as np
from rpi_lightshow.constants import (FRAMES_PER_BUFFER,
                                     FORMAT,
                                     RATE,
                                     FREQUENCY_BINS)
from rpi_lightshow.helpers import static_vars


@static_vars(window=np.hanning(FRAMES_PER_BUFFER))
def apply_window(data):
    """Applies a Hanning window to audio data.

    This reduces "spectral leakage" when performing an FFT. This link
    explains what this means and why windowing is useful:
    http://download.ni.com/evaluation/pxi/Understanding%20FFTs%20and%20Windowing.pdf.

    Arg:
        data: A numpy.array of numbers representing audio data.
    Returns:
        The `data` array with a Hanning window applied.
    """
    return data * apply_window.window

def make_frequency_bin(frequencies, bin_width, low_freq, high_freq):
    """Combine frequency bins together into a new bin.

    The new bin is scaled by how many of the old bins are combined to
    make it. This leads to ... okay results. I feel like scaling should
    depend on frequency, too, but at the moment not sure how best to go
    about that.

    Args:
        frequencies: A numpy.array of frequency bins, where the
            frequencies represented are given by the index multiplied by
            the bin width.
        bin_width: A number representing how many frequencies each bin
            respresents.
        low_freq: The lowest allowed frequency in the new bin.
        high_freq: The highest allowed frequency in the new bin.
    Returns:
        A number representing the magnitude of the new frequency bin.
    """
    # Find the indices for the lowest and highest bins to include
    low_bin_idx = int(np.ceil(low_freq / bin_width))
    high_bin_idx = int(np.floor(high_freq / bin_width))

    # Find the number of bins used
    num_bins = high_bin_idx - low_bin_idx + 1

    # Return the magnitude of the new bin
    return sum(frequencies[low_bin_idx:high_bin_idx + 1]) / num_bins

def fill_frequency_bins(audio_data,
                        sample_rate=RATE,
                        target_frequency_bins=FREQUENCY_BINS):
    """Returns magnitudes of target frequency ranges from an audio sample.

    Args:
        audio_data: A numpy.array of numbers representing audio data.
        sample_rate: Sampling rate of audio data in Hz.
        targest_frequency_bins: A list or tuple of two-tuples containing
            the lowest and highest frequencies to be included in a
            frequency bin.
    Returns:
        A list of numbers containing the magnitudes of each target
        frequency range, scaled by the number of frequencies included in
        each range.
    """
    # Frequency width for each bin the FFT will give us
    fft_width = sample_rate / len(audio_data)

    # Apply a Hanning window to the audio data
    windowed_data = apply_window(audio_data)

    # Perform an FFT and take the magnitude of each resulting complex
    # number
    fft_frequencies = np.abs(np.fft.rfft(windowed_data))

    # Build the target bins
    target_frequency_bins = [make_frequency_bin(fft_frequencies,
                                                fft_width,
                                                target_frequency_bins[i][0],
                                                target_frequency_bins[i][1],)
                                for i in range(len(target_frequency_bins))]

    return target_frequency_bins

def find_volume(audio_bytes_string, format_=FORMAT):
    """Returns the RMS of an audio sample.

    Arg:
        audio_bytes_string: A bytes string of audio encoded with int8,
            int16, or int32. No other formats will work with this.
        format_: A string signifying the format used to encode the audio.
    Returns:
        A number corresponding to the RMS of the audio string.
    """
    # Find how many bytes are being used to encode each sample of audio
    if format_ == 'int8':
        width = 1
    elif format_ == 'int16':
        width = 2
    elif format_ == 'int32':
        width = 4
    else:
        raise ValueError("'%s' is an invalid format here!" % format_)

    return audioop.rms(audio_bytes_string, width)

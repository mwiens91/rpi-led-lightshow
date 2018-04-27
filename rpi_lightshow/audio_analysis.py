"""Contains functions to analyze audio."""

import audioop
import numpy as np


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
    return data * np.hanning(len(data))

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
    low_bin_idx = int(np.ceil(low_freq / width))
    high_bin_idx = int(np.floor(high_freq / width))

    # Find the number of bins used
    num_bins = high_bin_idx - low_bin_idx + 1

    # Return the magnitude of the new bin
    return sum(frequencies[low_bin_idx:high_bin_idx + 1] / num_bins)

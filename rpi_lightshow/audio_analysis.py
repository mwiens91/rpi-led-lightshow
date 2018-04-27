"""Contains functions to analyze audio."""

import audioop
import numpy as np


def apply_window(data):
    """Applies a Hanning window to audio data.

    This reduces "spectral leakage" when performing an FFT. This link
    explains what this means and why windowing is useful:
    http://download.ni.com/evaluation/pxi/Understanding%20FFTs%20and%20Windowing.pdf.

    Arg:
        data: A numpy.array of numbers.
    Returns:
        The same array with a Hanning window applied.
    """
    return data * np.hanning(len(data))

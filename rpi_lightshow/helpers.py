"""Contains useful helper functions."""

import numpy as np
import pyaudio


def get_library_number_format(number_format, library):
    """Get a library's representation of a number format.

    This lets NumPy and PortAudio can play nicely together.

    Args:
        number_format: A string containing the number format. Must be
            either 'int8', 'int16', 'int32', 'float32', or 'uint8'.
        library: A string containing the library for which we must get
            the representation of the number format. Must be either
            'portaudio' or 'numpy'.
    """
    # Build format dictionaries for each library
    numpy_format_dict = {'int8': np.int8,
                         'int16': np.int16,
                         'int32': np.int32,
                         'float32': np.float32,
                         'uint8': np.uint8,}
    portaudio_format_dict = {'int8': pyaudio.paInt8,
                             'int16': pyaudio.paInt16,
                             'int32': pyaudio.paInt32,
                             'float32': pyaudio.paFloat32,
                             'uint8': pyaudio.paUInt8,}

    # Return the format type for the specified library
    try:
        if library == 'numpy':
            return numpy_format_dict[number_format]
        elif library == 'portaudio':
            return portaudio_format_dict[number_format]
        else:
            raise ValueError(("'%s' is an invalid library!"
                              " Library must be 'numpy' or 'portaudio'."
                              % library))
    except KeyError:
        # Invalid format
        raise ValueError("'%s' is an invalid format!" % number_format)

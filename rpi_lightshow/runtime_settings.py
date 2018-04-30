"""Contains functions to determine runtime settings."""

import argparse
from rpi_lightshow.constants import GPIO_PINS
from rpi_lightshow.version import NAME, VERSION, DESCRIPTION


def parse_runtime_args():
    """Parse runtime args using argparse.

    Returns:
        An object of type 'argparse.Namespace' containing the runtime
        arguments as attributes. See argparse documentation for more
        details.
    """
    parser = argparse.ArgumentParser(
            prog=NAME,
            description="%(prog)s - " + DESCRIPTION,)
    parser.add_argument(
            "-p", "--pin-numbers",
            help=("which 5 (exactly) GPIO pins to use."
                  " Defaults to 12, 18, 22, 36, 38."),
            type=int,
            nargs=5,
            default=GPIO_PINS,
            )
    parser.add_argument(
            "--show-duty-cycles",
            help="print the duty cycles to the terminal",
            action="store_true")
    parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s " + VERSION)

    return parser.parse_args()

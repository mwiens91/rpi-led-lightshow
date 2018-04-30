# rpi-led-lightshow

Perform a sexy light show with your Raspberry Pi and some LEDs!

## How do I run this?

You're going to need a Raspberry Pi (RPi) 3 Model B, a breadboard, 5
through-hole LEDs, and 5 through-hole ~270Ω resistors. The program is
unlikely to meet performance requirements on older RPis due to high
processing needs; that said, it might still work on older models if you
tweak some settings in [constants.py](rpi_lightshow/constants.py).

### Setting up the LEDs

The hardware setup for this program is *very* similar to that of
[rpi-volume-led](https://github.com/mwiens91/rpi-volume-led). The readme
for that project has all the instructions you'll need to set up one
LED to your RPi, and the program itself comes with tests which make
troubleshooting easy if anything goes wrong.

Once you're comfortable setting up one LED, set up five for this
project. The default pins used are 12, 18, 22, 36, and 38; and the LEDs
should be placed in that order.

### Running the program

In order for Python to use the RPi's GPIO pins, you need to run this
program as root:

```
sudo ./start_rpi_led_lightshow.py
```

If you want to use different GPIO pins than the ones listed in the
previous section you can specify exactly 5 pins using

```
sudo ./start_rpi_led_lightshow.py -p 1 2 3 4 5
```

where 1, 2, 3, 4, and 5 are example GPIO pin numbers.

If you're changing settings in
[constants.py](rpi_lightshow/constants.py) and want another
visualization of what's happening in the program, you can print the
un-averaged duty cycles to the terminal using

```
sudo ./start_rpi_led_lightshow.py --show-duty-cycles
```

## How does it work?

The core of the lightshow is based on frequency analysis (and the core
of *that* is the Fast Fourier Transform), which is supplemented by a few
other techniques to make the light show as tight as possible ("hit"
thresholds, averaging).

There are 5 LEDs: The lowest frequency LED is designed to follow the
beat by listening for sounds similar to a kick drum. The second lowest
frequency LED is meant to capture a snare drum, but depending on the
production of the song, might pick up something else; the criteria we
followed for this LED is that it supported the lowest frequency LED as
well as possible.

Most of the variation is meant to happen in the two lowest frequency
LEDs. The next three LEDs capture overlapping regions of the midrange.
They are not meant to track any specific instrument or sound but more-so
light up with the general midrange intensity of the song.

## How does it look?

Click the Youtube thumbnail below to find out!

[![Youtube thumbnail](https://img.youtube.com/vi/0hyedCX0OAA/0.jpg)](http://www.youtube.com/watch?v=0hyedCX0OAA "Raspberry Pi Dynamic LED Lightshow")

## Who are you?

[Tyler Trinh](https://github.com/bvtrinh) and [Matt
Wiens](https://github.com/mwiens91)

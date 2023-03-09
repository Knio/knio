# SPDX-FileCopyrightText: 2021 Sandy Macdonald
#
# SPDX-License-Identifier: MIT

# A simple example of how to set up a keymap and HID keyboard on Keybow 2040.

# You'll need to connect Keybow 2040 to a computer, as you would with a regular
# USB keyboard.

# Drop the keybow2040.py file into your `lib` folder on your `CIRCUITPY` drive.

# NOTE! Requires the adafruit_hid CircuitPython library also!

import sys
from collections import namedtuple

import board
import busio
import supervisor

from keybow2040 import Keybow2040

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode as CCC
from adafruit_hid.keycode import Keycode

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard and layout
kb = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
layout = KeyboardLayoutUS(kb)
# uart = busio.UART(board.TX, board.RX, baudrate=9600)




_key_fields = ['controller', 'arg', 'color']
KeyType = namedtuple('Key', _key_fields)
def Key(controller=None, arg=None, color=None):
    return KeyType(controller, arg, color)


class COLORS:
    PRESSED = (255, 255, 128)
    OFF = (32, 8, 0)


class KEYMAP:
    MAIN = [
        [
            Key(),
            Key(),
            Key(),
            Key(cc, CCC.VOLUME_INCREMENT, (64, 128, 0)),
        ], [
            Key(),
            Key(),
            Key(),
            Key(cc, CCC.VOLUME_DECREMENT, (128, 32, 0)),
        ], [
            Key(),
            Key(),
            Key(),
            Key(),
        ], [
            Key(),
            Key(),
            Key(),
            Key(),
        ],
    ]

    @staticmethod
    def iter(map):
        for x in range(4):
            for y in range(3, -1, -1):
                yield map[y][x]

    @staticmethod
    def get_num(map, number):
        # keys look like:

        #  3  7 11 15
        #  2  6 10 14
        #  1  5  9 13
        #  0  4  8 12

        x = number // 4
        y = 3 - (number % 4)
        return map[y][x]


# A map of keycodes that will be mapped sequentially to each of the keys, 0-15
keymap =    [(kb, Keycode.ZERO),
             (kb, Keycode.ONE),
             (kb, Keycode.TWO),
             (kb, Keycode.THREE),
             (kb, Keycode.FOUR),
             (kb, Keycode.FIVE),
             (kb, Keycode.SIX),
             (kb, Keycode.SEVEN),
             (kb, Keycode.EIGHT),
             (kb, Keycode.NINE),
             (kb, Keycode.A),
             (kb, Keycode.B),
             (cc, CCC.STOP),
             (cc, CCC.VOLUME_DECREMENT),
             (cc, CCC.VOLUME_INCREMENT),
             (kb, Keycode.F)]

# The colour to set the keys when pressed, yellow.

active_map = KEYMAP.MAIN

def set_map(map):
    global active_map
    active_map = map
    for key, h in zip(keybow.keys, KEYMAP.iter(map)):
        if h.color:
            key.set_led(*h.color)
        else:
            key.led_off()

# Attach handler functions to all of the keys
for key in keys:
    # key.set_led(*COLORS.OFF)

    # A press handler that sends the keycode and turns on the LED
    @keybow.on_press(key)
    def press_handler(key):
        print(f'key: {key.number}')
        h = KEYMAP.get_num(active_map, key.number)
        if h.controller in (kb, cc):
            print("Sending {}".format(h.arg))
            r = h.controller.send(h.arg)
            print("Sent. {}".format(r))
            key.set_led(*COLORS.PRESSED)
        else:
            print('E: unknown config {!r}'.format(h))

    # A release handler that turns off the LED
    @keybow.on_release(key)
    def release_handler(key):
        h = KEYMAP.get_num(active_map, key.number)
        key.set_led(*COLORS.OFF)


set_map(KEYMAP.MAIN)

def process(command):
    print(repr(command))

def main():
    data = []
    while True:
        # Always remember to call keybow.update()!
        keybow.update()

        # Poll serial console
        if supervisor.runtime.serial_bytes_available:
            c = sys.stdin.read(supervisor.runtime.serial_bytes_available)
            if c == '\n':
                process(''.join(data))
                data = []
            else:
                data.extend(c)

main()


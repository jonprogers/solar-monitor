#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MORSE - A morse code generator for the Raspberry Pi GPIO OK LED.
EN: Morse code generated from a dichotomic tree.
FR: On génère une séquence de code Morse, a partir d'un arbre dichotomique.
ES: Generador de codigo Morse, por medio de un árbol dicotómico.
RU: Создание последовательности кода Морзе (дихотомической валом).
PT: Codigo Morse criado a partir de uma árvore dicotômica.
"""
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
from time import sleep

__author__ = "Francois Dion"
__email__ = "francois.dion@gmail.com"
__copyright__ = "Copyright 2012, Francois Dion"

WPM = 5  # average words per minute, based on standard word PARIS
TIMEUNIT = 1.2 / WPM  # we can force a different unit, in seconds

# Activity/OK LED GPIO pin
OK_LED = 16

# We are going to be signaling on OUTPORT.
# If you are using another GPIO pin, assign it here.
OUTPORT = OK_LED

# Our famous dichotomic tree, as 6 strings to represent the 6 levels
TREE = (
    """            ?_    "  .    @   '  -        ;! (     ,    :""",
    u"54ŝ3é ð2 è+ þàĵ16=/ ç ĥ 7 ĝñ8 90",
    u"hvfüläpjbxcyzqöš",
    "surwdkgo",
    "ianm",
    "et",
)

DT = DD = '-.'


def letter2morse(letter):
    """ We take a letter and convert it to a morse code sequence.
    Since we are going down our dichotomic tree from the leaf to the trunk,
    we will end up with a reversed sequence, so we simply return the
    reverse of that ([::-1]) to get it in the right order.
    """
    if letter == ' ':  # No conversion needed, just a pause marker
        return letter
    found = False
    morse = ''
    position = 0
    for i in range(6):
        if found:
            position += position % 2
            position /= 2
            morse += DD[position % 2]
        elif letter in TREE[i]:
            position = (TREE[i].find(letter)) + 1
            morse = DT[position % 2]
            found = True
    return morse[::-1]


def morse2gpio(morse):
    """ Signal a morse letter (a morse code sequence for 1 alphanumeric).
    Also handles the pause between marks, letters and words.
    """
    for mark in morse:
        delay = TIMEUNIT
        # support for the dash as - or dah
        if mark in ('-', 'dah'):
            delay *= 3  # dash is 3 x longer than dot

        # dot or dash depending on the delay
        if mark == ' ':  # word separator
            sleep(delay * 4)  # stay off 4 + 1 + 2 below, total 7 TIMEUNITs
        else:
            GPIO.output(OUTPORT, GPIO.LOW)
        sleep(delay)
        # 1 TIMEUNIT pause between each mark
        GPIO.output(OUTPORT, GPIO.HIGH)
        sleep(TIMEUNIT)
    # end of letter pause
    sleep(TIMEUNIT * 2)  # already paused TIMEUNIT, 3 in total between letters


def main():
    """Get a string from the user and send the converted morse code sequence
    to a GPIO pin
    """

    # First, we have to setup the pin to output.
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(OUTPORT, GPIO.OUT)

    words = raw_input("Type sentence to send in morse code:")

    for letter in words.lower():
        morsecode = letter2morse(letter)
        print morsecode
        morse2gpio(morsecode)
    GPIO.cleanup()

if __name__ == "__main__":
    main()

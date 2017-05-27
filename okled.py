#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OKLED - Turn on then off the OK / Activity LED.
"""
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
from time import sleep

OKLED = 16

# setup GPIO, use Broadcom pin numbering.The only way to access pin 16
# on the BCM chip.
GPIO.setmode(GPIO.BCM)

# setup BCM pin 16 as an output
GPIO.setup(OKLED, GPIO.OUT)

# Turn on LED
GPIO.output(OKLED, GPIO.LOW)
sleep(5)

# Turn off LED
GPIO.output(OKLED, GPIO.HIGH)

# We are done, let's clean up after ourselves.
GPIO.cleanup()

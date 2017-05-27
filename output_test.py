#! /usr/bin/env python

import cp2
import time

cp2.init()

cp2.dig_out(11,True)
time.sleep(2)
cp2.dig_out(12,True)
time.sleep(2)
cp2.dig_out(11,False)
time.sleep(2)
cp2.dig_out(12,False)
time.sleep(2)

cp2.close()

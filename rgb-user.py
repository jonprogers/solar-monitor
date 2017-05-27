#! /usr/bin/env python

import rgb_ctrl
import time
import sys

rgb_ctrl.init()
rgb_ctrl.rgb(10,0,0,1,600)
rgb_ctrl.rgb(0,0,10,1,600)
rgb_ctrl.rgb(10,0,10,10,600)
rgb_ctrl.rgb(10,0,0,1,600)
rgb_ctrl.rgb(0,10,0,1,600)
rgb_ctrl.rgb(0,0,10,1,600)
rgb_ctrl.closedown()

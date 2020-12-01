#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: tc_from_frames.py
"""
## Expects frame number and fps as input

import math
import sys

framenum, fps = sys.argv[1:]

fps = math.ceil(float(fps))  # example: to round 29.976 up to 30.
framenum = int(framenum)
frHour = fps * 3600
frSec = fps * 60

hours = math.floor(framenum / frHour)
minutes = math.floor(framenum % (hours * frHour) / frSec)
seconds = math.floor(framenum % ((hours * frHour) + (minutes * frSec)) / fps)
frames = math.floor(framenum % fps)
'''
# alternate method used by Igor R.
hours = int(framenum // frHour)
minutes = int((framenum - hours * frHour) // frSec)
seconds = int((framenum - (hours * frHour) - (minutes * frSec)) // fps)
frames = int(round(framenum - (hours * frHour) - (minutes * frSec) - (seconds * fps)))
'''
print('{0} frames = {1:0>2}:{2:0>2}:{3:0>2}:{4:0>2} at {5} fps'.format(framenum, hours, minutes, seconds, frames, fps))

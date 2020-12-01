#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: tc_to_frames.py
"""
## Expects TC and fps as input

import math
import sys

timecode, fps = sys.argv[1:]

def validatetc(timecode, fps):
        """Validates SMPTE timecode"""
        if len(timecode) != 11:
                raise ValueError ('Malformed SMPTE timecode', timecode)
        if int(timecode[9:]) > fps:
                raise ValueError ('SMPTE timecode to frame rate mismatch', timecode, fps)

fps = math.ceil(float(fps))

hours, minutes, seconds, frames = timecode.split(':')
# there must be a cleaner, easier way to split() into integers
hours = int(hours)
minutes = int(minutes)
seconds = int(seconds)
frames = int(frames)

framecount = (hours * 3600 * fps) + (minutes * 60 * fps) + (seconds * fps) + frames

print('timecode {0} at {1} fps is frame# {2}'.format(timecode, fps, framecount))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: EDL_to_OTIO_0.1.py
"""

import opentimelineio as otio
import sys
import re

inputEDL, outputOTIO = sys.argv[1:]

print('reading {}'.format(inputEDL))
timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)

print('writing {}'.format(outputOTIO))
otio.adapters.write_to_file(timeline, outputOTIO)

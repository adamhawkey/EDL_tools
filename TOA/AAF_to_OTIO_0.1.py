#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: AAF_to_OTIO_0.1.py
"""

import opentimelineio as otio
import sys
import re

inputAAF, outputOTIO = sys.argv[1:]

print('reading {}'.format(inputAAF))
timeline = otio.adapters.read_from_file(inputAAF)

print('writing {}'.format(outputOTIO))
otio.adapters.write_to_file(timeline, outputOTIO)

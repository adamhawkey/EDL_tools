#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
version: Convert_to_OTIO_0.1.py
"""

import opentimelineio as otio
import sys
import re

inputFile, outputOTIO = sys.argv[1:]

print('reading {}'.format(inputFile))
timeline = otio.adapters.read_from_file(inputFile)

print('writing {}'.format(outputOTIO))
otio.adapters.write_to_file(timeline, outputOTIO)

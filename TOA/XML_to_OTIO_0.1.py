#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: XML_to_OTIO_0.1.py
"""

import opentimelineio as otio
import sys
import re

inputXML, outputOTIO = sys.argv[1:]

print('reading {}'.format(inputXML))
timeline = otio.adapters.read_from_file(inputXML)

print('writing {}'.format(outputOTIO))
otio.adapters.write_to_file(timeline, outputOTIO)

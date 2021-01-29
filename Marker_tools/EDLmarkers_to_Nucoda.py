#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: EDLMarkers_to_Nucoda.py
"""
# This works for importing an EDL Marker List
# as a single event EDL, with markers preceding it.  Import EDL and select:
# Import Bookmarks from EDL.

import sys
import csv
import re

print(sys.argv[0])
inputEDL, outputEDL = sys.argv[1:]

header1 = ('TITLE: (Markers grabbed from) {} \n').format(inputEDL)
header2 = ('FCM: FILM \n')
footer1 = ('001  Bars   V     C        00:58:00:00 00:58:30:00 00:58:00:00 00:58:30:00\n')
footer2 = ('* LOC: 00:58:20:00 green   Dummy clip that can be deleted\n')

markerwriter = open(outputEDL, 'w')
markerwriter.write(header1)
markerwriter.write(header2)

with open(inputEDL, newline = '') as openEDL:
    for line in openEDL:
        if '* LOC:' in line:
            print(line)
            markerwriter.write(line)

markerwriter.write(footer1)
markerwriter.write(footer2)
markerwriter.close()

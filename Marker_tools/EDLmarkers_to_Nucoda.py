#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: EDLMarkers_to_Nucoda.py
"""
# This works for importing an EDL Marker List
# as a single event EDL, with markers preceding it.  Import and select 
# Import Bookmarks from EDL.

# import opentimelineio as otio
import sys
import csv
import re

print(sys.argv[0])
inputEDL, outputEDL = sys.argv[1:]

header1 = ('TITLE: (Markers grabbed from) {} \n').format(inputEDL)
header2 = ('FCM: FILM \n')
footer1 = ('001  Bars   V     C        00:58:00:00 00:58:30:00 00:58:00:00 00:58:30:00\n')
footer2 = ('* LOC: 00:58:20:00 green   Dummy clip that can be deleted\n')

timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)
# ignore_timecode_mismatch=True deals with the source timecode and duration 
# not matching the timebase.

markerwriter = open(outputEDL, 'w')
markerwriter.write(header1)
markerwriter.write(header2)

with open(inputEDL, newline = '') as openEDL:
    #lines = csv.reader(markers, delimiter='\t')
    for line in openEDL:
        if '* LOC:' in line:
            print(line)
#            name, timecode, layer, color, comment = line[:5]
#            print('* LOC: {0} {1}   {2}'.format(timecode, color, comment))
#            edl_line = ('* LOC: {0} {1}   {2}\n'.format(timecode, color, comment))
            markerwriter.write(line)

markerwriter.write(footer1)
markerwriter.write(footer2)
markerwriter.close()

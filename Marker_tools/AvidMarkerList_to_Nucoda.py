#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version: AvidMarkerList_to_Nucoda_0.2.py
"""
# This works for importing an Avid Marker List (text file), tab delimited,
# as a single event EDL, with markers preceding it.  Select "Import Locators as Bookmarks" in the EDL import dialogue.

# 20220210 - revision for Nucoda version 2021.2 no longer allowing import of timeline markers.  Need to research this more.
# Now we will make a single event of BL (Black) with all the VFX Markers on it.  Probably better this way, as it can be rippled and moved.

# import opentimelineio as otio
import sys
import csv
import re
import os
import time

print(sys.argv[0])
marker_list, outputEDL = sys.argv[1:]
date = time.ctime()

header1 = ('TITLE: converted on {0} from {1} \n').format(date, marker_list)
header2 = ('FCM: FILM \n')
header3 = ('001  BL   V     C        00:00:00:00 00:49:00:00 00:00:00:00 00:49:00:00\n')

markerwriter = open(outputEDL, 'w')
markerwriter.write(header1)
markerwriter.write(header2)
markerwriter.write(header3)

with open(marker_list, newline = '') as markers:
    lines = csv.reader(markers, delimiter='\t')
    for line in lines:
        try:
            name, timecode, layer, color, comment = line[:5]
            edl_line = ('* LOC: {0} {1}   {2}\n'.format(timecode, color, comment))
        except:
            edl_line = ('')
        markerwriter.write(edl_line)

# markerwriter.write(footer1)
# markerwriter.write(footer2)
markerwriter.close()

'''
# Unfortunately, Nucoda doesn't support markers at the end of an EDL, like some others.
# Turns out it reads them perfectly from before the first event as * LOC: style markers.  See README.md
'''
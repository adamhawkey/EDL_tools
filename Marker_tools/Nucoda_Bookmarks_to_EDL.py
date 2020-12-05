#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: Nucoda_Bookmarks_to_EDL.py
"""
# This works for importing a Nucoda Bookmark list (csv text file), comma delimited,
# as a single event EDL, with markers preceding it.  Import and select 
# Import Bookmarks from EDL.

# For future use in some way of rippling bookmarks also. 

# import opentimelineio as otio
import sys
import csv
import re

print(sys.argv[0])
nucoda_marker_list, outputEDL = sys.argv[1:]
#file1 = open(nucoda_marker_list, 'r')

header1 = ('TITLE: (converted from) {} \n').format(nucoda_marker_list)
header2 = ('FCM: FILM \n')
footer1 = ('001  Bars   V     C        00:58:00:00 00:58:30:00 00:58:00:00 00:58:30:00\n')
footer2 = ('* LOC: 00:58:20:00 green   These are bars that can be deleted\n')

markerwriter = open(outputEDL, 'w')
markerwriter.write(header1)
markerwriter.write(header2)

with open(nucoda_marker_list, newline = '') as markers:
    # clean_markers = re.sub(r"[\x]", '_', markers) # trying to remove extra \x newline character.
    lines = csv.reader(markers, delimiter=',')
    next(lines) #skips the "Timeline Bookmarks" line.
    next(lines) #skips the "Date, Time, Position, Description, Colour, Type, TimeCode" line.
    for line in lines:
        date, time, position, description, colour_number, marker_type, timecode = line[:7]
        colour = colour_number
        print('* LOC: {0} {1}   {2}'.format(timecode, colour, description))
        edl_line = ('* LOC: {0} {1}   {2}\n'.format(timecode, colour, description))
        markerwriter.write(edl_line)
markerwriter.write(footer1)
markerwriter.write(footer2)
markerwriter.close()


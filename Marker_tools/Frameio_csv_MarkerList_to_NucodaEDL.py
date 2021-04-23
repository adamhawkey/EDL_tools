#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: Frameio_csv_MarkerList_to_NucodaEDL.py
"""
# This works for importing a Frame.io csv type marker list, comma delimited,
# as a single event EDL, with markers preceding it.  Import and select 
# Import Bookmarks from EDL.

# import opentimelineio as otio
import sys
import csv
import re
import os

print(sys.argv[0])
marker_list, outputEDL = sys.argv[1:]
#file1 = open(marker_list, 'r')

header1 = ('TITLE: (converted from) {} \n').format(marker_list)
header2 = ('FCM: FILM \n')
footer1 = ('001  Bars   V     C        00:58:00:00 00:58:30:00 00:58:00:00 00:58:30:00\n')
footer2 = ('* LOC: 00:58:20:00 green   These are bars that can be deleted\n')

markerwriter = open(outputEDL, 'w')
markerwriter.write(header1)
markerwriter.write(header2)

with open(marker_list, newline = '') as markers:
    #clean_markers = re.sub(r"[\x]", '_', markers) # trying to remove extra \x newline character.
    #clean_markers = os.linesep.join([s for s in markers.splitlines() if s])
    #re.sub(r'\n\s*\n', '\n', markers, flags=re.MULTILINE)
    lines = csv.reader(markers, delimiter=',')
    for line in lines:
        try:
            Team, Project, File, FileURL, Version, Commenter, CommentID, Comment, Reply, CommentedAt, Complete, Annotation, Frame, Duration, Timecode, TimecodeIn, TimecodeOut, TimecodeSrc, TimecodeSrcIn, TimecodeSrcOut = line[:20]
            #prod, title, filename, link, timecode, layer, color, comment = line[:5]
            print('* LOC: {0} {1} {2} - {3} {4}'.format(Timecode, Commenter, Comment, Reply, Frame))
            edl_line = ('* LOC: {0} {1} {2} - {3} {4}\n'.format(Timecode, Commenter, Comment, Reply, Frame))
        except:
            print('except')
            edl_line = ('')
        markerwriter.write(edl_line)

markerwriter.write(footer1)
markerwriter.write(footer2)
markerwriter.close()

'''
# Unfortunately, Nucoda doesn't support markers at the end of an EDL, like some others.
# Turns out it reads them perfectly from before the first event as * LOC: style markers.  See README.md
'''
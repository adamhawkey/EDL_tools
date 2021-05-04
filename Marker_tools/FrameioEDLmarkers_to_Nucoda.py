#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: FrameioEDLMarkers_to_Nucoda.py
"""
# This should convert a frame.io / Resolve EDL Marker List
# to a single event EDL, with markers preceding it.  Import EDL and select:
# Import Bookmarks from EDL.

import sys
import csv
import re
import opentimelineio as otio

print(sys.argv[0])
inputEDL, outputEDL = sys.argv[1:]

num = 0

print('reading {}'.format(inputEDL))
timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)

for clip in timeline.each_clip():
    clipname = clip.name
    print(clipname)
    #start = otio.opentime.to_seconds(clip.source_range.start_time)
    #duration = otio.opentime.to_seconds(clip.source_range.duration)
    try:
        markers = clip.metadata.get("cmx_3600").get("comments")
        print(markers)
        #if markers.find('ResolveColorYellow') > 0:
        #    print(markers[0].split('|'))
        print(markers[0].find('ResolveColorYellow'))
    except:
        continue
        '''markers = 'None{0}_{1}'.format(clipname, num)  #this is only if there is no locator present.  will not help if there are multiple clips with same clipname.
        num = num + 1   #this increments the value after the name incase there is a duplicate.  Would be better if I checked if an identical filename exists, and only increment then.
        print('2',' {}'.format(markers))
    try:
        comments = clip.metadata.get("cmx_3600").get("comments")
        resolveMarkerColor = comments.get('ResolveColorYellow')
        print('3', 'resolveMarkerColor: {}'.format(resolveMarkerColor))
    except:
        print('4', 'exception on 3')
'''
    #print('clipname: {0}, start: {1}, duration {2}'.format(clipname, start, duration))

colours = 'ResolveColorRed', 'ResolveColorGreen', 'ResolveColorBlue', 'ResolveColorCyan', 'ResolveColorMagenta', 'ResolveColorYellow', 'ResolveColorBlack', 'ResolveColorWhite'
#this indexes the colour_number to the name of the colour
print(colours[0], '0', colours[1], '1', colours[2], '2', colours[3], '3', colours[4], '4', colours[5], '5', colours[6], '6', colours[7], '7')

'''
header1 = ('TITLE: (Markers grabbed from) {} \n').format(inputEDL)
header2 = ('FCM: FILM \n')
footer1 = ('001  Bars   V     C        00:58:00:00 00:58:30:00 00:58:00:00 00:58:30:00\n')
footer2 = ('* LOC: 00:58:20:00 green   Dummy clip that can be deleted\n')

markerwriter = open(outputEDL, 'w')
markerwriter.write(header1)
markerwriter.write(header2)

with open(inputEDL, newline = '') as openEDL:
    for line in openEDL:
        if ' |' in line:
            if ' |C:ResolveColorYellow' in line:
                print(line)
            #print(line)
            markerwriter.write(line)

markerwriter.write(footer1)
markerwriter.write(footer2)
markerwriter.close()
'''
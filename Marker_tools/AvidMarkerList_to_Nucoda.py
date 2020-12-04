#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: AvidMarkerList_to_Nucoda.py
"""
import opentimelineio as otio
import sys
import csv
import re

print(sys.argv[0])
marker_list, outputEDL = sys.argv[1:]
#file1 = open(marker_list, 'r')

markerwriter = open(outputEDL, 'w')

with open(marker_list, newline = '') as markers:
    # clean_markers = re.sub(r"[\x]", '_', markers) # trying to remove extra \x newline character.
    lines = csv.reader(markers, delimiter='\t')
    for line in lines:
        name, timecode, layer, color, comment = line[:5]
        print('* LOC: {0} {1}   {2}'.format(timecode, color, comment))
        edl_line = ('* LOC: {0} {1}   {2}\n'.format(timecode, color, comment))
        markerwriter.write(edl_line)
    
markerwriter.close()

'''
# Unfortunately, Nucoda doesn't support markers at the end of an EDL, like some others.
# Turns out it reads them perfectly from before the first event as * LOC: style markers.  See README.md

# other methods I tried
lines = tuple(open(marker_list))
for line in lines:
    #print(line)
    name, timecode, layer, color, comment = line.split("\t", maxsplit = 5)
    print(name)
###
with open(marker_list) as markers:
    lines = markers.read().splitlines()
    #lines = [line.rstrip() for line in markers]
    
print(lines)
'''
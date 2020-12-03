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

with open(marker_list, newline = '') as markers:
    # clean_markers = re.sub(r"[\x]", '_', markers) # trying to remove extra \x newline character.
    lines = csv.reader(markers, delimiter='\t')
    for line in lines:
        #print(', '.join(line))
        name, timecode, layer, color, comment = line[:5]
        #print(name, timecode, layer, color, comment)
        print("* LOC:", timecode, color,' ', comment) #need to figure out the timeline vs. segment locator in Nucoda.

'''  # potentially, markers could be at the end of the EDL in the following structure...  Need to test in Nucoda.
* ============================================================
* Marker Metadata
* ------------------------------------------------------------
* 
* Sequence name: KMP-4K_and_CTM_Test_DNxHR444
* Number  Color   Marker Name              Start TC    End TC      Duration    Track  Part        Comment
*      1  Red     GTS3_Dylan               01:00:25:10                         V1                 This is a marker
*      2  Red     GTS3_Dylan               01:01:24:01                         V1                 This is also a marker
*      3  Red     GTS3_Dylan               01:02:44:09                         V1                 This is still a marker
*      4  Red     GTS3_Dylan               01:03:14:01                         V1                 This is a marker indicating where GH5 footage starts
'''
'''
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
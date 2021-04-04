#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Usage:  DolbyXML_parse.py {XML name}
"""

# The idea is to parse through a DolbyVision XML and report back certain things.
# To start, I am trying to search for Level 1 high level analysis over a certain value.

import sys
import re
import os
import xml.etree.ElementTree as ET

if len(sys.argv) < 2:
    print('Not enough arguments.', __doc__)
    sys.exit()
inputXML = sys.argv[1]

# Seems DolbyVision XML is structured (DolbyLabsMDF/Outputs/Output/Video/Track/Shot/PluginNode/DVDynamicData/Level1)

tree = ET.parse(inputXML)
root = tree.getroot()

l1ul = 0.762 # Level1 Upper Limit that I would like to check if any shot exceeds.

# Ideally, I would use the .find() or .findall(), but for some reason I can't get it to work on Dolby XML.
# Seems to only return "None".

for Shot in root.findall('.//Shot'):
    print(Shot.tag, Shot.text, Shot.attrib)

"""
for Shot in root.findall():
    print(Shot.tag, Shot.text, Shot.attrib)


for Shot in root.findall('.Outputs/Output/Video/Track/Shot'):
    frameNum = Shot.find('.Record/In').text
    l1 = Shot.get('Level1').text
    print(Shot, frameNum, l1)
    if l1[2] > l1ul:
        print('Shot at frame# ', frameNum, 'has an L1 high value of: ', L1[2])

# But if I manually force my way down the tree, I can get there.

for Outputs in root:
    for Output in Outputs:
        for Video in Output:
            for Track in Video:
                for Shot in Track:
                    Level1 = Shot.find('.PluginNode/DVDynamicData/Level1')
                    #print(Shot.tag, Level1)
                    l1 = Shot.find(".PluginNode/DVDynamicData/Level1").text
                    frameNum = Shot.find(".Record/In").text
                    print(Shot.tag, frameNum, l1)
"""
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Usage:  DolbyXML_parse.py {XML name} {Max Nits}
"""
# The idea is to parse through a DolbyVision XML and report back certain things.
# To start, I am trying to search for Level 1 high level analysis over a certain value.
import sys
import re
import os
import colour
import xml.etree.ElementTree as ET

inputXML = sys.argv[1]
maxNits = sys.argv[2]

# DolbyVision 4.0 and 2.9 XMLs are the same up to the 'Shot' ( DolbyLabsMDF/Outputs/Output/Video/Track/Shot )
# DolbyVision 4.0 XML 'Shot' tree is: ( Shot/PluginNode/DVDynamicData/Level1 )
# DolbyVision 2.9 XML 'Shot' tree is: ( Shot/PluginNode/DolbyEDR/ImageCharacter )

# ns = {"xmlns": "http://www.dolby.com/schemas/dvmd/4_0_2"}

with open(inputXML) as f:
    xmlstring=f.read()
    xmlstring=re.sub(r'\sxmlns="[^"]+"','',xmlstring,count=1)
root=ET.fromstring(xmlstring)

# tree = ET.parse(inputXML)
# root = tree.getroot()
# print(root)

l1ul = round(colour.models.eotf_inverse_ST2084(maxNits), 4) # Level1 Upper Limit that I would like to check if any shot exceeds.

# I cannot get the .find() and .findall() commands to work on DolbyVision 4.0 XMLs due to some problem in the xmlns namespace.
# So I can either remove the xmlns, or append :xsd to it, like "<DolbyLabsMDF xmlns:xsd="http://w..."

for Shot in root.findall('.Outputs/Output/Video/Track/Shot'):
    frameNum = Shot.find('.Record/In').text
#    l1_29 = Shot.find('.PluginNode/DolbyEDR/ImageCharacter').text
    l1_40 = Shot.find('.PluginNode/DVDynamicData/Level1/ImageCharacter').text
    l1high = float(l1_40.split(' ')[2])
    if l1high > l1ul:
        print('Shot at frame# ', frameNum, 'has a level1 high value of: ', l1high)

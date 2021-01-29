#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
version: GT_prep_0.3.py
"""

# This script is very specific to the show Good Trouble.

import opentimelineio as otio
import sys
import re

inputEDL, outputEDL = sys.argv[1:]

lut_path = ('T:\\luts\\GoodTrouble\\Season_3\\Season_03_VLog\\') # this is the local root path to the luts.
lut_space = ('VLog') # other option is SDR
lut_version = ('v2')
lut_ext = ('cube')
'''
EDIT_RATE = 24
HOUR = 3600 * EDIT_RATE
'''
timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)
# ignore_timecode_mismatch=True deals with the source timecode and duration 
# not matching the timebase.

for clip in timeline.each_clip():
    
    edl_meta = clip.metadata.get('cmx_3600',{})
    
    nucoda_stack = [
        'NUCODA_LAYER Log',
        'NUCODA_LAYER Log2',
        'NUCODA_LAYER Log3',
        'NUCODA_LAYER Log4',
        'NUCODA_LAYER Log5',
        'NUCODA_LAYER Log6',
    ]
    
    comments = edl_meta.get('comments', [])

    for comment in comments:
        if 'REEL: GT_' in comment:
            _, lut_string = comment.split(": ")
            #print(lut_string)
            lut_string_split = re.split(r'_SDR', lut_string)
            #print(lut_string_split)
            lut_string_chars = re.split(r'[^A-Za-z0-9_]+', lut_string_split[0])
            #print(lut_string_chars[0])
            lut_root = lut_string_chars[0]
            #print(lut_root)
            print('{0} becomes {1}_{2}_{3}.{4}'.format(lut_string, lut_root, lut_space, lut_version, lut_ext))
            lut_layer = 'NUCODA_LAYER GT_LUT -effect NucodaCMSPath -lut {0}{1}_{2}_{3}.{4}'.format(lut_path, lut_root, lut_space, lut_version, lut_ext)
            nucoda_stack.append(lut_layer)

    comments.extend(nucoda_stack)
    
otio.adapters.write_to_file(timeline, outputEDL, adapter_name='cmx_3600', style='nucoda')
#print(otio.adapters.write_to_string(timeline, adapter_name='cmx_3600'))
